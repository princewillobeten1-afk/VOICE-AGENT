from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.models import Agent
from app.collaboration.models import AiTeam, AiTeamMember, CollaborationLog, CollaborationMessage, CollaborationPolicy, CollaborationSession, DelegationEvent, SharedContext
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event


def team_dict(item: AiTeam) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "parent_team_id": item.parent_team_id, "supervisor_agent_id": item.supervisor_agent_id, "name": item.name, "slug": item.slug, "department": item.department, "description": item.description, "responsibilities": item.responsibilities, "routing_policy": item.routing_policy, "collaboration_rules": item.collaboration_rules, "status": item.status, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


def member_dict(item: AiTeamMember) -> dict:
    return {"id": item.id, "team_id": item.team_id, "agent_id": item.agent_id, "role_id": item.role_id, "membership_type": item.membership_type, "responsibilities": item.responsibilities, "availability_state": item.availability_state, "workload_score": item.workload_score, "status": item.status, "created_at": item.created_at}


def session_dict(item: CollaborationSession) -> dict:
    return {"id": item.id, "team_id": item.team_id, "conversation_id": item.conversation_id, "workflow_run_id": item.workflow_run_id, "supervisor_agent_id": item.supervisor_agent_id, "objective": item.objective, "status": item.status, "priority": item.priority, "shared_state": item.shared_state, "success_criteria": item.success_criteria, "started_at": item.started_at, "completed_at": item.completed_at, "created_at": item.created_at}


def delegation_dict(item: DelegationEvent) -> dict:
    return {"id": item.id, "session_id": item.session_id, "source_agent_id": item.source_agent_id, "target_agent_id": item.target_agent_id, "team_id": item.team_id, "task_title": item.task_title, "task_payload": item.task_payload, "routing_reason": item.routing_reason, "confidence_score": float(item.confidence_score) if item.confidence_score is not None else None, "depth": item.depth, "status": item.status, "due_at": item.due_at, "completed_at": item.completed_at, "created_at": item.created_at}


def log_dict(item: CollaborationLog) -> dict:
    return {"id": item.id, "session_id": item.session_id, "event_type": item.event_type, "actor_agent_id": item.actor_agent_id, "level": item.level, "message": item.message, "payload": item.payload, "created_at": item.created_at}


async def emit_collab_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"collaboration.{name}", aggregate_type="collaboration", aggregate_id=aggregate_id, source="multi-agent-engine", payload=payload, metadata={"engine": "multi-agent"}))


async def route_agent(db: AsyncSession, current: CurrentUser, workspace_id: UUID, team_id: UUID | None, required_role: str | None) -> tuple[Agent | None, str, float]:
    query = select(Agent).where(Agent.organization_id == current.organization_id, Agent.workspace_id == workspace_id, Agent.deleted_at.is_(None), Agent.status.in_(["live", "testing", "draft"]))
    if required_role:
        query = query.where(Agent.role.ilike(f"%{required_role}%"))
    if team_id:
        member_ids = select(AiTeamMember.agent_id).where(AiTeamMember.team_id == team_id, AiTeamMember.status == "active", AiTeamMember.deleted_at.is_(None))
        query = query.where(Agent.id.in_(member_ids))
    agent = (await db.execute(query.order_by(Agent.updated_at.desc()).limit(1))).scalar_one_or_none()
    if agent:
        return agent, f"Matched role '{required_role or 'any'}' with active team membership and current availability placeholder.", 0.86
    fallback = (await db.execute(select(Agent).where(Agent.organization_id == current.organization_id, Agent.workspace_id == workspace_id, Agent.deleted_at.is_(None)).order_by(Agent.updated_at.desc()).limit(1))).scalar_one_or_none()
    return fallback, "Fallback routing selected the most recently updated eligible AI employee.", 0.52 if fallback else 0


async def create_delegation(db: AsyncSession, current: CurrentUser, payload) -> DelegationEvent:
    target, reason, confidence = await route_agent(db, current, payload.workspace_id, payload.team_id, payload.required_role)
    session = None
    if payload.session_id:
        session = await db.get(CollaborationSession, payload.session_id)
    if session is None:
        session = CollaborationSession(organization_id=current.organization_id, workspace_id=payload.workspace_id, team_id=payload.team_id, supervisor_agent_id=payload.supervisor_agent_id, objective=payload.objective or payload.task_title, status="active", priority=payload.priority, shared_state=payload.shared_state, success_criteria=payload.success_criteria, started_at=datetime.now(UTC))
        db.add(session)
        await db.flush()
    event = DelegationEvent(organization_id=current.organization_id, workspace_id=payload.workspace_id, session_id=session.id, source_agent_id=payload.source_agent_id, target_agent_id=target.id if target else None, team_id=payload.team_id, task_title=payload.task_title, task_payload=payload.task_payload, routing_reason=reason, confidence_score=confidence, depth=payload.depth, status="assigned" if target else "unassigned", due_at=payload.due_at)
    db.add(event)
    await db.flush()
    db.add(CollaborationLog(organization_id=current.organization_id, workspace_id=payload.workspace_id, session_id=session.id, event_type="delegation.assigned", actor_agent_id=payload.source_agent_id, message=f"Delegated task '{payload.task_title}'", payload={"target_agent_id": str(target.id) if target else None, "confidence": confidence, "reason": reason}))
    db.add(CollaborationMessage(organization_id=current.organization_id, workspace_id=payload.workspace_id, session_id=session.id, sender_agent_id=payload.source_agent_id, recipient_agent_id=target.id if target else None, message_type="task_request", subject=payload.task_title, body=payload.message, payload=payload.task_payload, status="sent" if target else "unrouted"))
    for key, value in (payload.shared_state or {}).items():
        db.add(SharedContext(organization_id=current.organization_id, workspace_id=payload.workspace_id, session_id=session.id, context_type="variable", key=key, value_json={"value": value}, visibility="team", source_agent_id=payload.source_agent_id))
    await emit_collab_event(db, current, "delegation.assigned", payload.workspace_id, session.id, {"delegation_id": str(event.id), "target_agent_id": str(target.id) if target else None})
    return event


async def analytics(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    teams = (await db.execute(select(func.count()).select_from(AiTeam).where(AiTeam.organization_id == current.organization_id, AiTeam.workspace_id == workspace_id, AiTeam.deleted_at.is_(None)))).scalar_one()
    members = (await db.execute(select(func.count()).select_from(AiTeamMember).where(AiTeamMember.organization_id == current.organization_id, AiTeamMember.workspace_id == workspace_id, AiTeamMember.deleted_at.is_(None)))).scalar_one()
    sessions = (await db.execute(select(func.count()).select_from(CollaborationSession).where(CollaborationSession.organization_id == current.organization_id, CollaborationSession.workspace_id == workspace_id))).scalar_one()
    delegations = (await db.execute(select(func.count()).select_from(DelegationEvent).where(DelegationEvent.organization_id == current.organization_id, DelegationEvent.workspace_id == workspace_id))).scalar_one()
    active = (await db.execute(select(func.count()).select_from(CollaborationSession).where(CollaborationSession.organization_id == current.organization_id, CollaborationSession.workspace_id == workspace_id, CollaborationSession.status == "active"))).scalar_one()
    return {"teams": int(teams or 0), "members": int(members or 0), "sessions": int(sessions or 0), "active_sessions": int(active or 0), "delegations": int(delegations or 0), "success_rate": "modeled", "average_resolution_time": "future", "routing_strategy": "role + team + availability placeholder + workload placeholder"}
