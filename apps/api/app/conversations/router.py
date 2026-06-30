from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.conversations.models import Conversation, ConversationAnalytics, ConversationContextSnapshot, ConversationEngineEvent, ConversationGoal, ConversationSession, ConversationTurn
from app.conversations.schemas import ContextSnapshotCreate, ContextSnapshotOut, ConversationAnalyticsOut, ConversationCreate, ConversationDetail, ConversationEventOut, ConversationGoalOut, ConversationOut, ConversationSessionCreate, ConversationSessionOut, ConversationTurnOut, EndSessionRequest, GoalCreate, HandoffRequest, PauseSessionRequest, TurnCreate
from app.conversations.service import add_turn, analytics_dict, append_engine_event, collect_analytics, context_dict, conversation_dict, create_conversation, emit_conversation_event, event_dict, get_owned_conversation, goal_dict, session_dict, start_session, turn_dict
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission

router = APIRouter(prefix="/conversations", tags=["conversation-engine"])


@router.get("", response_model=list[ConversationOut])
async def list_conversations(workspace_id: UUID, status_filter: str | None = Query(default=None, alias="status"), channel: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Conversation).where(Conversation.organization_id == current.organization_id, Conversation.workspace_id == workspace_id, Conversation.deleted_at.is_(None))
    if status_filter:
        query = query.where(Conversation.status == status_filter)
    if channel:
        query = query.where(Conversation.channel == channel)
    rows = (await db.execute(query.order_by(Conversation.updated_at.desc()).limit(100))).scalars().all()
    return [ConversationOut(**conversation_dict(item)) for item in rows]


@router.post("", response_model=ConversationDetail, status_code=status.HTTP_201_CREATED)
async def create(payload: ConversationCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await create_conversation(db, current, payload)
    session = await start_session(db, current, conversation, ConversationSessionCreate(channel=payload.channel, adapter=f"{payload.channel}_adapter"))
    await collect_analytics(db, current, conversation, session.id)
    await emit_conversation_event(db, current, "conversation.started", conversation, {"channel": conversation.channel})
    await audit(db, "conversation.created", current.user.id, current.organization_id, "conversation", conversation.id)
    await db.commit()
    return await detail_response(db, conversation)


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get(conversation_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return await detail_response(db, conversation)


@router.post("/{conversation_id}/sessions", response_model=ConversationSessionOut, status_code=status.HTTP_201_CREATED)
async def create_session(conversation_id: UUID, payload: ConversationSessionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    session = await start_session(db, current, conversation, payload)
    await emit_conversation_event(db, current, "conversation.session.started", conversation, {"session_id": str(session.id)})
    await db.commit()
    return ConversationSessionOut(**session_dict(session))


@router.post("/{conversation_id}/sessions/{session_id}/pause", response_model=ConversationSessionOut)
async def pause_session(conversation_id: UUID, session_id: UUID, payload: PauseSessionRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    session = await db.get(ConversationSession, session_id)
    if conversation is None or session is None or session.conversation_id != conversation.id:
        raise HTTPException(status_code=404, detail="Conversation session not found")
    session.status = "paused"
    session.paused_at = datetime.now(UTC)
    conversation.lifecycle_stage = "paused"
    await append_engine_event(db, current, conversation, "conversation.paused", "session", {"reason": payload.reason}, session_id=session.id)
    await emit_conversation_event(db, current, "conversation.paused", conversation, {"reason": payload.reason})
    await db.commit()
    return ConversationSessionOut(**session_dict(session))


@router.post("/{conversation_id}/sessions/{session_id}/resume", response_model=ConversationSessionOut)
async def resume_session(conversation_id: UUID, session_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    session = await db.get(ConversationSession, session_id)
    if conversation is None or session is None or session.conversation_id != conversation.id:
        raise HTTPException(status_code=404, detail="Conversation session not found")
    session.status = "active"
    session.resumed_at = datetime.now(UTC)
    session.recovery_state = {**(session.recovery_state or {}), "last_resume": session.resumed_at.isoformat(), "state_preserved": True}
    conversation.lifecycle_stage = "resumed"
    await append_engine_event(db, current, conversation, "conversation.resumed", "session", {"state_preserved": True}, session_id=session.id)
    await db.commit()
    return ConversationSessionOut(**session_dict(session))


@router.post("/{conversation_id}/sessions/{session_id}/end", response_model=ConversationSessionOut)
async def end_session(conversation_id: UUID, session_id: UUID, payload: EndSessionRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    session = await db.get(ConversationSession, session_id)
    if conversation is None or session is None or session.conversation_id != conversation.id:
        raise HTTPException(status_code=404, detail="Conversation session not found")
    session.status = "ended"
    session.ended_at = datetime.now(UTC)
    session.end_reason = payload.reason
    await append_engine_event(db, current, conversation, "conversation.session.ended", "session", {"reason": payload.reason}, session_id=session.id)
    await collect_analytics(db, current, conversation, session.id)
    await db.commit()
    return ConversationSessionOut(**session_dict(session))


@router.post("/{conversation_id}/turns", response_model=ConversationTurnOut, status_code=status.HTTP_201_CREATED)
async def record_turn(conversation_id: UUID, payload: TurnCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    turn = await add_turn(db, current, conversation, payload)
    await emit_conversation_event(db, current, "conversation.user_message_received" if payload.speaker_type == "user" else "conversation.ai_response_generated", conversation, {"turn_id": str(turn.id), "speaker_type": payload.speaker_type})
    await collect_analytics(db, current, conversation, payload.session_id)
    await db.commit()
    return ConversationTurnOut(**turn_dict(turn))


@router.post("/{conversation_id}/goals", response_model=ConversationGoalOut, status_code=status.HTTP_201_CREATED)
async def create_goal(conversation_id: UUID, payload: GoalCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    goal = ConversationGoal(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, name=payload.name, goal_type=payload.goal_type, priority=payload.priority, success_criteria=payload.success_criteria, progress=payload.progress)
    db.add(goal)
    await append_engine_event(db, current, conversation, "conversation.goal.created", "goal", {"goal_type": goal.goal_type})
    await db.commit()
    return ConversationGoalOut(**goal_dict(goal))


@router.post("/{conversation_id}/context-snapshots", response_model=ContextSnapshotOut, status_code=status.HTTP_201_CREATED)
async def create_context_snapshot(conversation_id: UUID, payload: ContextSnapshotCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    snapshot = ConversationContextSnapshot(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, session_id=payload.session_id, snapshot_type=payload.snapshot_type, token_budget=payload.token_budget, sources=payload.sources, prioritized_context=payload.prioritized_context, omitted_context=payload.omitted_context, model_limits=payload.model_limits)
    db.add(snapshot)
    await append_engine_event(db, current, conversation, "conversation.context.loaded", "context", {"source_count": len(payload.sources)}, session_id=payload.session_id)
    await db.commit()
    return ContextSnapshotOut(**context_dict(snapshot))


@router.post("/{conversation_id}/handoff", response_model=ConversationOut)
async def request_handoff(conversation_id: UUID, payload: HandoffRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation.handoff_status = "requested"
    conversation.priority = payload.priority
    conversation.summary = payload.summary or conversation.summary
    conversation.lifecycle_stage = "handoff_requested"
    await append_engine_event(db, current, conversation, "conversation.handoff.requested", "handoff", {"reason": payload.reason, "summary": payload.summary})
    await emit_conversation_event(db, current, "conversation.handoff.requested", conversation, {"reason": payload.reason})
    await audit(db, "conversation.handoff.requested", current.user.id, current.organization_id, "conversation", conversation.id)
    await db.commit()
    return ConversationOut(**conversation_dict(conversation))


@router.post("/{conversation_id}/complete", response_model=ConversationOut)
async def complete_conversation(conversation_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation.status = "completed"
    conversation.lifecycle_stage = "completed"
    conversation.ended_at = datetime.now(UTC)
    await append_engine_event(db, current, conversation, "conversation.completed", "lifecycle", {})
    await collect_analytics(db, current, conversation)
    await emit_conversation_event(db, current, "conversation.completed", conversation, {})
    await db.commit()
    return ConversationOut(**conversation_dict(conversation))


@router.get("/{conversation_id}/analytics", response_model=ConversationAnalyticsOut)
async def get_analytics(conversation_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    conversation = await get_owned_conversation(db, conversation_id, current)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    analytics = await collect_analytics(db, current, conversation)
    await db.commit()
    return ConversationAnalyticsOut(**analytics_dict(analytics))


async def detail_response(db: AsyncSession, conversation: Conversation) -> ConversationDetail:
    sessions = (await db.execute(select(ConversationSession).where(ConversationSession.conversation_id == conversation.id).order_by(ConversationSession.created_at.desc()).limit(20))).scalars().all()
    turns = (await db.execute(select(ConversationTurn).where(ConversationTurn.conversation_id == conversation.id).order_by(ConversationTurn.sequence_number.asc()).limit(100))).scalars().all()
    goals = (await db.execute(select(ConversationGoal).where(ConversationGoal.conversation_id == conversation.id).order_by(ConversationGoal.priority.asc()))).scalars().all()
    snapshots = (await db.execute(select(ConversationContextSnapshot).where(ConversationContextSnapshot.conversation_id == conversation.id).order_by(ConversationContextSnapshot.created_at.desc()).limit(10))).scalars().all()
    events = (await db.execute(select(ConversationEngineEvent).where(ConversationEngineEvent.conversation_id == conversation.id).order_by(ConversationEngineEvent.sequence_number.asc()).limit(100))).scalars().all()
    analytics = (await db.execute(select(ConversationAnalytics).where(ConversationAnalytics.conversation_id == conversation.id))).scalar_one_or_none()
    return ConversationDetail(conversation=ConversationOut(**conversation_dict(conversation)), sessions=[ConversationSessionOut(**session_dict(item)) for item in sessions], turns=[ConversationTurnOut(**turn_dict(item)) for item in turns], goals=[ConversationGoalOut(**goal_dict(item)) for item in goals], context_snapshots=[ContextSnapshotOut(**context_dict(item)) for item in snapshots], events=[ConversationEventOut(**event_dict(item)) for item in events], analytics=ConversationAnalyticsOut(**analytics_dict(analytics)) if analytics else None)