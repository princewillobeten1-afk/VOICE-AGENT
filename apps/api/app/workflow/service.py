import re
from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event
from app.workflow.models import Workflow, WorkflowExecutionLog, WorkflowRun, WorkflowVersion
from app.workflow.registry import node_registry


def workflow_dict(item: Workflow) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "project_id": item.project_id, "name": item.name, "slug": item.slug, "status": item.status, "category": item.category, "description": item.description, "trigger_type": item.trigger_type, "execution_mode": item.execution_mode, "current_version_id": item.current_version_id, "definition": item.definition, "settings": item.settings, "canvas_state": item.canvas_state, "published_at": item.published_at, "last_run_at": item.last_run_at, "run_count": item.run_count, "failure_count": item.failure_count, "created_at": item.created_at, "updated_at": item.updated_at}


def version_dict(item: WorkflowVersion) -> dict:
    return {"id": item.id, "workflow_id": item.workflow_id, "version_number": item.version_number, "status": item.status, "change_summary": item.change_summary, "definition": item.definition, "canvas_state": item.canvas_state, "validation_state": item.validation_state, "published_at": item.published_at, "rolled_back_from_version_id": item.rolled_back_from_version_id, "created_at": item.created_at}


def run_dict(item: WorkflowRun) -> dict:
    return {"id": item.id, "workflow_id": item.workflow_id, "version_id": item.version_id, "conversation_id": item.conversation_id, "agent_id": item.agent_id, "trigger_type": item.trigger_type, "trigger_ref": item.trigger_ref, "status": item.status, "current_node_key": item.current_node_key, "execution_mode": item.execution_mode, "started_at": item.started_at, "paused_at": item.paused_at, "resumed_at": item.resumed_at, "finished_at": item.finished_at, "next_run_at": item.next_run_at, "attempt": item.attempt, "retry_count": item.retry_count, "duration_ms": item.duration_ms, "input_payload": item.input_payload, "output_payload": item.output_payload, "variables": item.variables, "execution_state": item.execution_state, "error_message": item.error_message, "created_at": item.created_at}


def log_dict(item: WorkflowExecutionLog) -> dict:
    return {"id": item.id, "workflow_id": item.workflow_id, "workflow_run_id": item.workflow_run_id, "node_key": item.node_key, "node_type": item.node_type, "event_type": item.event_type, "level": item.level, "message": item.message, "input_snapshot": item.input_snapshot, "output_snapshot": item.output_snapshot, "latency_ms": item.latency_ms, "retry_count": item.retry_count, "metadata_json": item.metadata_json, "created_at": item.created_at}


async def emit_workflow_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"workflow.{name}", aggregate_type="workflow", aggregate_id=aggregate_id, source="workflow-engine", payload=payload, metadata={"engine": "visual-workflows"}))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "workflow"


def resolve_expression(expression: str, context: dict) -> str:
    def repl(match):
        value = context
        for part in match.group(1).split("."):
            value = value.get(part) if isinstance(value, dict) else None
        return "" if value is None else str(value)
    return re.sub(r"\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}", repl, expression)


async def next_version_number(db: AsyncSession, workflow_id: UUID) -> int:
    value = (await db.execute(select(func.max(WorkflowVersion.version_number)).where(WorkflowVersion.workflow_id == workflow_id))).scalar_one_or_none()
    return int(value or 0) + 1


async def snapshot_version(db: AsyncSession, current: CurrentUser, workflow: Workflow, status: str, change_summary: str | None) -> WorkflowVersion:
    version = WorkflowVersion(organization_id=current.organization_id, workspace_id=workflow.workspace_id, workflow_id=workflow.id, version_number=await next_version_number(db, workflow.id), status=status, change_summary=change_summary, definition=workflow.definition, canvas_state=workflow.canvas_state, validation_state={"valid": True, "node_count": len((workflow.definition or {}).get("nodes", []))}, published_at=datetime.now(UTC) if status == "published" else None, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    await db.flush()
    return version

async def execute_workflow(db: AsyncSession, current: CurrentUser, workflow: Workflow, payload) -> WorkflowRun:
    now = datetime.now(UTC)
    run = WorkflowRun(organization_id=current.organization_id, workspace_id=workflow.workspace_id, workflow_id=workflow.id, version_id=workflow.current_version_id, conversation_id=payload.conversation_id, agent_id=payload.agent_id, trigger_type=payload.trigger_type, trigger_ref=payload.trigger_ref, status="running", execution_mode=payload.execution_mode or workflow.execution_mode, started_at=now, input_payload=payload.input_payload, variables=payload.variables, execution_state={"queue": "local-simulation", "fault_tolerant_resume": True})
    db.add(run)
    await db.flush()
    nodes = (workflow.definition or {}).get("nodes", []) or [{"key": "start", "type": "start", "label": "Start"}, {"key": "end", "type": "end", "label": "End"}]
    context = {"input": payload.input_payload, "variables": payload.variables, "workflow": {"id": str(workflow.id), "name": workflow.name}}
    for node in nodes[:50]:
        node_key = node.get("key") or node.get("id") or node.get("type")
        node_type = node.get("type", "log")
        definition = node_registry.get(node_type)
        message = resolve_expression(node.get("message", f"Executed {node.get('label') or node_type}"), context)
        db.add(WorkflowExecutionLog(organization_id=current.organization_id, workspace_id=workflow.workspace_id, workflow_id=workflow.id, workflow_run_id=run.id, node_key=node_key, node_type=node_type, event_type="node.executed", level="info", message=message, input_snapshot={"node": node}, output_snapshot={"status": "simulated", "adapter": definition.group if definition else "custom"}, latency_ms=8, metadata_json={"real_provider_called": False}))
        run.current_node_key = node_key
        if node_type in {"human_approval", "wait", "delay"} and payload.allow_pause:
            run.status = "paused"
            run.paused_at = datetime.now(UTC)
            run.execution_state = {**run.execution_state, "pause_reason": node_type, "resume_supported": True}
            break
    if run.status != "paused":
        run.status = "completed"
        run.finished_at = datetime.now(UTC)
        run.duration_ms = max(1, int((run.finished_at - now).total_seconds() * 1000))
        run.output_payload = {"status": "completed", "simulated": True, "nodes_executed": len(nodes[:50])}
    workflow.run_count += 1
    workflow.last_run_at = now
    await emit_workflow_event(db, current, "started", workflow.workspace_id, workflow.id, {"run_id": str(run.id), "trigger_type": payload.trigger_type})
    await emit_workflow_event(db, current, run.status, workflow.workspace_id, workflow.id, {"run_id": str(run.id), "status": run.status})
    return run


async def monitoring_summary(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    workflows = (await db.execute(select(func.count()).select_from(Workflow).where(Workflow.organization_id == current.organization_id, Workflow.workspace_id == workspace_id, Workflow.deleted_at.is_(None)))).scalar_one()
    running = (await db.execute(select(func.count()).select_from(WorkflowRun).where(WorkflowRun.organization_id == current.organization_id, WorkflowRun.workspace_id == workspace_id, WorkflowRun.status == "running"))).scalar_one()
    completed = (await db.execute(select(func.count()).select_from(WorkflowRun).where(WorkflowRun.organization_id == current.organization_id, WorkflowRun.workspace_id == workspace_id, WorkflowRun.status == "completed"))).scalar_one()
    failed = (await db.execute(select(func.count()).select_from(WorkflowRun).where(WorkflowRun.organization_id == current.organization_id, WorkflowRun.workspace_id == workspace_id, WorkflowRun.status == "failed"))).scalar_one()
    avg_duration = (await db.execute(select(func.avg(WorkflowRun.duration_ms)).where(WorkflowRun.organization_id == current.organization_id, WorkflowRun.workspace_id == workspace_id, WorkflowRun.duration_ms.is_not(None)))).scalar_one_or_none()
    return {"workflows": int(workflows or 0), "running": int(running or 0), "completed": int(completed or 0), "failed": int(failed or 0), "average_duration_ms": int(avg_duration) if avg_duration else None, "node_catalog_size": len(node_registry.catalog()), "queue_mode": "local-simulation", "fault_tolerance": {"resume_after_restart": "modeled", "long_running": "paused_state", "background_jobs": "future_worker"}}
