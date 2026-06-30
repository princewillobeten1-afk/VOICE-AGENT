from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.models import Agent
from app.collaboration.models import CollaborationSession, DelegationEvent
from app.conversations.models import Conversation
from app.identity.dependencies import CurrentUser
from app.identity.models import AuditLog
from app.knowledge.models import Document, KnowledgeBase
from app.memory.models import Memory
from app.retrieval.models import RetrievalRequest
from app.tools.models import ToolExecution
from app.voice.models import VoiceSession
from app.workflow.models import WorkflowRun
from app.analytics.models import OpsAlert, OpsAlertEvent, OpsCostRecord, OpsDashboard, OpsEvaluationResult, OpsHealthReport, OpsMetric


def dashboard_dict(item: OpsDashboard) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "scope": item.scope, "owner_user_id": item.owner_user_id, "layout": item.layout, "filters": item.filters, "widgets": item.widgets, "is_default": item.is_default, "status": item.status, "created_at": item.created_at, "updated_at": item.updated_at}


def alert_dict(item: OpsAlert) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "alert_type": item.alert_type, "severity": item.severity, "status": item.status, "condition": item.condition, "channels": item.channels, "last_triggered_at": item.last_triggered_at, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


def health_dict(item: OpsHealthReport) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "component": item.component, "status": item.status, "score": item.score, "checks": item.checks, "incidents": item.incidents, "measured_at": item.measured_at, "created_at": item.created_at}


def cost_dict(item: OpsCostRecord) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "cost_type": item.cost_type, "provider": item.provider, "entity_type": item.entity_type, "entity_id": item.entity_id, "amount": float(item.amount), "currency": item.currency, "quantity": float(item.quantity) if item.quantity is not None else None, "unit": item.unit, "occurred_at": item.occurred_at, "metadata_json": item.metadata_json}


def evaluation_dict(item: OpsEvaluationResult) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "agent_id": item.agent_id, "conversation_id": item.conversation_id, "evaluation_type": item.evaluation_type, "score": float(item.score) if item.score is not None else None, "status": item.status, "evaluator": item.evaluator, "criteria": item.criteria, "result": item.result, "reviewed_by_user_id": item.reviewed_by_user_id, "evaluated_at": item.evaluated_at, "created_at": item.created_at}


async def count_table(db: AsyncSession, model, current: CurrentUser, workspace_id: UUID, *conditions) -> int:
    query = select(func.count()).select_from(model).where(model.organization_id == current.organization_id, model.workspace_id == workspace_id, *conditions)
    return int((await db.execute(query)).scalar_one() or 0)


async def executive_summary(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    agents = await count_table(db, Agent, current, workspace_id, Agent.deleted_at.is_(None))
    conversations = await count_table(db, Conversation, current, workspace_id)
    voice_sessions = await count_table(db, VoiceSession, current, workspace_id)
    workflow_runs = await count_table(db, WorkflowRun, current, workspace_id)
    tool_executions = await count_table(db, ToolExecution, current, workspace_id)
    retrievals = await count_table(db, RetrievalRequest, current, workspace_id)
    memories = await count_table(db, Memory, current, workspace_id, Memory.deleted_at.is_(None))
    collab = await count_table(db, CollaborationSession, current, workspace_id)
    failed_tools = await count_table(db, ToolExecution, current, workspace_id, ToolExecution.status.in_(["failed", "rejected"]))
    completed_tools = await count_table(db, ToolExecution, current, workspace_id, ToolExecution.status == "completed")
    total_tools = max(1, completed_tools + failed_tools)
    costs = (await db.execute(select(func.coalesce(func.sum(OpsCostRecord.amount), 0)).where(OpsCostRecord.organization_id == current.organization_id, OpsCostRecord.workspace_id == workspace_id))).scalar_one()
    health_rows = (await db.execute(select(OpsHealthReport).where(OpsHealthReport.organization_id == current.organization_id, OpsHealthReport.workspace_id == workspace_id).order_by(OpsHealthReport.measured_at.desc()).limit(10))).scalars().all()
    health_score = int(sum(row.score for row in health_rows) / len(health_rows)) if health_rows else 100
    return {"active_ai_employees": agents, "active_conversations": conversations, "active_voice_sessions": voice_sessions, "running_workflows": workflow_runs, "tool_executions": tool_executions, "knowledge_queries": retrievals, "memory_usage": memories, "collaboration_sessions": collab, "success_rate": round((completed_tools / total_tools) * 100, 2), "error_rate": round((failed_tools / total_tools) * 100, 2), "customer_satisfaction": "framework", "average_response_time_ms": None, "ai_cost": float(costs), "system_health": health_score}


async def live_monitoring(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    return {"live_conversations": await count_table(db, Conversation, current, workspace_id), "voice_calls": await count_table(db, VoiceSession, current, workspace_id), "workflow_executions": await count_table(db, WorkflowRun, current, workspace_id, WorkflowRun.status.in_(["queued", "running", "paused"])), "tool_calls": await count_table(db, ToolExecution, current, workspace_id, ToolExecution.status.in_(["queued", "running"])), "collaboration_sessions": await count_table(db, CollaborationSession, current, workspace_id, CollaborationSession.status == "active"), "system_events": "event_stream_placeholder"}


async def analytics_breakdown(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    return {"conversations": {"count": await count_table(db, Conversation, current, workspace_id), "completion_rate": "framework", "sentiment": "placeholder"}, "ai_employees": {"count": await count_table(db, Agent, current, workspace_id, Agent.deleted_at.is_(None)), "accuracy_metrics": "framework"}, "workflows": {"runs": await count_table(db, WorkflowRun, current, workspace_id), "bottlenecks": "modeled"}, "tools": {"executions": await count_table(db, ToolExecution, current, workspace_id)}, "knowledge": {"retrievals": await count_table(db, RetrievalRequest, current, workspace_id), "documents": await count_table(db, Document, current, workspace_id, Document.deleted_at.is_(None))}, "memory": {"memories": await count_table(db, Memory, current, workspace_id, Memory.deleted_at.is_(None))}, "multi_agent": {"delegations": await count_table(db, DelegationEvent, current, workspace_id)}}
