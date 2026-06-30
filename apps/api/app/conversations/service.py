from datetime import UTC, datetime, timedelta
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.conversations.models import Conversation, ConversationAnalytics, ConversationContextSnapshot, ConversationEngineEvent, ConversationGoal, ConversationSession, ConversationTurn, Message
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event


def conversation_dict(item: Conversation) -> dict:
    return {"id": item.id, "organization_id": item.organization_id, "workspace_id": item.workspace_id, "project_id": item.project_id, "agent_id": item.agent_id, "agent_version_id": item.agent_version_id, "channel": item.channel, "status": item.status, "lifecycle_stage": item.lifecycle_stage, "priority": item.priority, "current_topic": item.current_topic, "active_intent": item.active_intent, "subject": item.subject, "customer_ref": item.customer_ref, "external_thread_id": item.external_thread_id, "handoff_status": item.handoff_status, "summary": item.summary, "started_at": item.started_at, "ended_at": item.ended_at, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


def session_dict(item: ConversationSession) -> dict:
    return {"id": item.id, "conversation_id": item.conversation_id, "workspace_id": item.workspace_id, "channel": item.channel, "adapter": item.adapter, "status": item.status, "state_version": item.state_version, "current_speaker": item.current_speaker, "active_turn_id": item.active_turn_id, "active_intent": item.active_intent, "pending_questions": item.pending_questions, "tool_state": item.tool_state, "workflow_state": item.workflow_state, "memory_refs": item.memory_refs, "session_state": item.session_state, "recovery_state": item.recovery_state, "started_at": item.started_at, "last_activity_at": item.last_activity_at, "paused_at": item.paused_at, "resumed_at": item.resumed_at, "expires_at": item.expires_at, "ended_at": item.ended_at, "end_reason": item.end_reason}


def turn_dict(item: ConversationTurn) -> dict:
    return {"id": item.id, "conversation_id": item.conversation_id, "session_id": item.session_id, "message_id": item.message_id, "sequence_number": item.sequence_number, "speaker_type": item.speaker_type, "turn_type": item.turn_type, "status": item.status, "content": item.content, "intent": item.intent, "entities": item.entities, "context_delta": item.context_delta, "response_plan": item.response_plan, "latency_ms": item.latency_ms, "interrupted": item.interrupted, "metadata_json": item.metadata_json, "created_at": item.created_at}


def goal_dict(item: ConversationGoal) -> dict:
    return {"id": item.id, "conversation_id": item.conversation_id, "name": item.name, "goal_type": item.goal_type, "status": item.status, "priority": item.priority, "success_criteria": item.success_criteria, "progress": item.progress, "completed_at": item.completed_at}


def context_dict(item: ConversationContextSnapshot) -> dict:
    return {"id": item.id, "conversation_id": item.conversation_id, "session_id": item.session_id, "snapshot_type": item.snapshot_type, "token_budget": item.token_budget, "sources": item.sources, "prioritized_context": item.prioritized_context, "omitted_context": item.omitted_context, "model_limits": item.model_limits, "created_at": item.created_at}


def event_dict(item: ConversationEngineEvent) -> dict:
    return {"id": item.id, "conversation_id": item.conversation_id, "session_id": item.session_id, "turn_id": item.turn_id, "event_type": item.event_type, "stage": item.stage, "sequence_number": item.sequence_number, "payload": item.payload, "latency_ms": item.latency_ms, "trace_id": item.trace_id, "created_at": item.created_at}


def analytics_dict(item: ConversationAnalytics) -> dict:
    return {"id": item.id, "conversation_id": item.conversation_id, "session_id": item.session_id, "duration_seconds": item.duration_seconds, "turn_count": item.turn_count, "average_response_time_ms": item.average_response_time_ms, "completion_status": item.completion_status, "escalation_status": item.escalation_status, "goal_achievement": item.goal_achievement, "sentiment": item.sentiment, "satisfaction": item.satisfaction, "metadata_json": item.metadata_json}


async def emit_conversation_event(db: AsyncSession, current: CurrentUser, name: str, conversation: Conversation, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=conversation.workspace_id, actor_user_id=current.user.id, name=name, aggregate_type="conversation", aggregate_id=conversation.id, source="conversation-engine", payload=payload, metadata={"channel": conversation.channel, "status": conversation.status}))


async def append_engine_event(db: AsyncSession, current: CurrentUser, conversation: Conversation, event_type: str, stage: str | None, payload: dict, session_id=None, turn_id=None, latency_ms=None, trace_id=None) -> ConversationEngineEvent:
    max_sequence = (await db.execute(select(func.max(ConversationEngineEvent.sequence_number)).where(ConversationEngineEvent.conversation_id == conversation.id))).scalar_one_or_none() or 0
    event = ConversationEngineEvent(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, session_id=session_id, turn_id=turn_id, event_type=event_type, stage=stage, sequence_number=int(max_sequence) + 1, payload=payload, latency_ms=latency_ms, trace_id=trace_id)
    db.add(event)
    return event


async def get_owned_conversation(db: AsyncSession, conversation_id: UUID, current: CurrentUser) -> Conversation | None:
    return (await db.execute(select(Conversation).where(Conversation.id == conversation_id, Conversation.organization_id == current.organization_id, Conversation.deleted_at.is_(None)))).scalar_one_or_none()


async def create_conversation(db: AsyncSession, current: CurrentUser, payload) -> Conversation:
    now = datetime.now(UTC)
    conversation = Conversation(organization_id=current.organization_id, workspace_id=payload.workspace_id, project_id=payload.project_id, agent_id=payload.agent_id, agent_version_id=payload.agent_version_id, channel=payload.channel, status="open", lifecycle_stage="created", priority="normal", subject=payload.subject, customer_ref=payload.customer_ref, external_thread_id=payload.external_thread_id, handoff_status="none", started_at=now, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(conversation)
    await db.flush()
    for goal in payload.goals:
        db.add(ConversationGoal(organization_id=current.organization_id, workspace_id=payload.workspace_id, conversation_id=conversation.id, name=goal.get("name", "Conversation goal"), goal_type=goal.get("goal_type", "general"), priority=goal.get("priority", 100), success_criteria=goal.get("success_criteria", {}), progress=goal.get("progress", {})))
    await append_engine_event(db, current, conversation, "conversation.started", "lifecycle", {"channel": conversation.channel})
    return conversation


async def start_session(db: AsyncSession, current: CurrentUser, conversation: Conversation, payload) -> ConversationSession:
    now = datetime.now(UTC)
    session = ConversationSession(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, voice_session_id=payload.voice_session_id, channel=payload.channel, adapter=payload.adapter, status="active", current_speaker="none", pending_questions=[], tool_state={}, workflow_state={}, memory_refs=[], session_state=payload.session_state, recovery_state={"resume_supported": True}, started_at=now, last_activity_at=now, expires_at=now + timedelta(minutes=payload.expires_in_minutes))
    db.add(session)
    conversation.lifecycle_stage = "session_initialized"
    await db.flush()
    await append_engine_event(db, current, conversation, "conversation.session.started", "session", {"adapter": session.adapter}, session_id=session.id)
    return session


async def add_turn(db: AsyncSession, current: CurrentUser, conversation: Conversation, payload) -> ConversationTurn:
    max_sequence = (await db.execute(select(func.max(ConversationTurn.sequence_number)).where(ConversationTurn.conversation_id == conversation.id))).scalar_one_or_none() or 0
    message = Message(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, sender_type=payload.speaker_type, sender_id=current.user.id if payload.speaker_type == "user" else None, role=payload.speaker_type, content=payload.content, sequence_number=int(max_sequence) + 1, metadata_json=payload.metadata_json)
    db.add(message)
    await db.flush()
    turn = ConversationTurn(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, session_id=payload.session_id, message_id=message.id, sequence_number=int(max_sequence) + 1, speaker_type=payload.speaker_type, turn_type=payload.turn_type, status="completed", content=payload.content, intent=payload.intent, entities=payload.entities, context_delta=payload.context_delta, response_plan=payload.response_plan, latency_ms=payload.latency_ms, interrupted=payload.interrupted, metadata_json=payload.metadata_json)
    db.add(turn)
    conversation.active_intent = payload.intent.get("name") if payload.intent else conversation.active_intent
    conversation.current_topic = payload.context_delta.get("topic", conversation.current_topic) if payload.context_delta else conversation.current_topic
    if payload.session_id:
        session = await db.get(ConversationSession, payload.session_id)
        if session:
            session.current_speaker = payload.speaker_type
            session.active_turn_id = turn.id
            session.active_intent = conversation.active_intent
            session.last_activity_at = datetime.now(UTC)
            session.state_version += 1
    await db.flush()
    await append_engine_event(db, current, conversation, "conversation.turn.recorded", "turn", {"speaker_type": payload.speaker_type, "turn_type": payload.turn_type, "intent": payload.intent}, session_id=payload.session_id, turn_id=turn.id, latency_ms=payload.latency_ms)
    return turn


async def collect_analytics(db: AsyncSession, current: CurrentUser, conversation: Conversation, session_id=None) -> ConversationAnalytics:
    turn_count = (await db.execute(select(func.count()).select_from(ConversationTurn).where(ConversationTurn.conversation_id == conversation.id))).scalar_one()
    avg_latency = (await db.execute(select(func.avg(ConversationTurn.latency_ms)).where(ConversationTurn.conversation_id == conversation.id, ConversationTurn.latency_ms.is_not(None)))).scalar_one_or_none()
    duration = 0
    if conversation.started_at:
        end = conversation.ended_at or datetime.now(UTC)
        duration = int((end - conversation.started_at).total_seconds())
    analytics = (await db.execute(select(ConversationAnalytics).where(ConversationAnalytics.conversation_id == conversation.id))).scalar_one_or_none()
    if analytics is None:
        analytics = ConversationAnalytics(organization_id=current.organization_id, workspace_id=conversation.workspace_id, conversation_id=conversation.id, session_id=session_id)
        db.add(analytics)
    analytics.duration_seconds = duration
    analytics.turn_count = int(turn_count or 0)
    analytics.average_response_time_ms = int(avg_latency) if avg_latency else None
    analytics.completion_status = "completed" if conversation.status == "completed" else "in_progress"
    analytics.escalation_status = conversation.handoff_status
    analytics.goal_achievement = {"status": "placeholder", "scored_by": "future_goal_engine"}
    analytics.sentiment = {"status": "placeholder"}
    analytics.satisfaction = {"status": "placeholder"}
    return analytics