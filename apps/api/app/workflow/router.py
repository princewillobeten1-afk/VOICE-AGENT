from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.workflow.models import Workflow, WorkflowExecutionLog, WorkflowRun, WorkflowVersion
from app.workflow.registry import node_registry
from app.workflow.schemas import MonitoringOut, WorkflowCreate, WorkflowExecuteRequest, WorkflowLogOut, WorkflowOut, WorkflowRunOut, WorkflowUpdate, WorkflowVersionOut
from app.workflow.service import emit_workflow_event, execute_workflow, log_dict, monitoring_summary, run_dict, slugify, snapshot_version, version_dict, workflow_dict

router = APIRouter(prefix="/workflows", tags=["workflow-engine"])


@router.get("/nodes")
async def node_catalog(current: CurrentUser = Depends(require_permission(Permission.ORG_READ))):
    return {"nodes": node_registry.catalog(), "note": "Registry only. Real provider and AI execution adapters are intentionally deferred."}


@router.get("", response_model=list[WorkflowOut])
async def list_workflows(workspace_id: UUID, status_filter: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Workflow).where(Workflow.organization_id == current.organization_id, Workflow.workspace_id == workspace_id, Workflow.deleted_at.is_(None))
    if status_filter:
        query = query.where(Workflow.status == status_filter)
    rows = (await db.execute(query.order_by(Workflow.updated_at.desc()).limit(100))).scalars().all()
    return [WorkflowOut(**workflow_dict(item)) for item in rows]


@router.post("", response_model=WorkflowOut, status_code=status.HTTP_201_CREATED)
async def create_workflow(payload: WorkflowCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    workflow = Workflow(organization_id=current.organization_id, workspace_id=payload.workspace_id, project_id=payload.project_id, name=payload.name, slug=slugify(payload.name), status="draft", category=payload.category, description=payload.description, trigger_type=payload.trigger_type, execution_mode=payload.execution_mode, definition=payload.definition, settings=payload.settings, canvas_state=payload.canvas_state, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(workflow)
    await db.flush()
    version = await snapshot_version(db, current, workflow, "draft", "Initial draft")
    workflow.current_version_id = version.id
    await audit(db, "workflow.created", current.user.id, current.organization_id, "workflow", workflow.id)
    await emit_workflow_event(db, current, "created", payload.workspace_id, workflow.id, {"name": workflow.name})
    await db.commit()
    return WorkflowOut(**workflow_dict(workflow))


@router.patch("/{workflow_id}", response_model=WorkflowOut)
async def update_workflow(workflow_id: UUID, payload: WorkflowUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if workflow is None or workflow.organization_id != current.organization_id or workflow.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    for field in ["name", "status", "category", "description", "trigger_type", "execution_mode", "definition", "settings", "canvas_state"]:
        value = getattr(payload, field)
        if value is not None:
            setattr(workflow, field, value)
    workflow.updated_by_user_id = current.user.id
    version = await snapshot_version(db, current, workflow, "draft", payload.change_summary or "Workflow updated")
    workflow.current_version_id = version.id
    await emit_workflow_event(db, current, "updated", workflow.workspace_id, workflow.id, {"version_id": str(version.id)})
    await db.commit()
    return WorkflowOut(**workflow_dict(workflow))


@router.post("/{workflow_id}/publish", response_model=WorkflowVersionOut)
async def publish_workflow(workflow_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if workflow is None or workflow.organization_id != current.organization_id or workflow.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    version = await snapshot_version(db, current, workflow, "published", "Published workflow")
    workflow.status = "published"
    workflow.current_version_id = version.id
    workflow.published_at = datetime.now(UTC)
    await emit_workflow_event(db, current, "published", workflow.workspace_id, workflow.id, {"version_number": version.version_number})
    await db.commit()
    return WorkflowVersionOut(**version_dict(version))


@router.get("/{workflow_id}/versions", response_model=list[WorkflowVersionOut])
async def list_versions(workflow_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if workflow is None or workflow.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    rows = (await db.execute(select(WorkflowVersion).where(WorkflowVersion.workflow_id == workflow_id).order_by(WorkflowVersion.version_number.desc()))).scalars().all()
    return [WorkflowVersionOut(**version_dict(item)) for item in rows]


@router.post("/{workflow_id}/execute", response_model=WorkflowRunOut, status_code=status.HTTP_201_CREATED)
async def run_workflow(workflow_id: UUID, payload: WorkflowExecuteRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if workflow is None or workflow.organization_id != current.organization_id or workflow.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    run = await execute_workflow(db, current, workflow, payload)
    await audit(db, "workflow.executed", current.user.id, current.organization_id, "workflow_run", run.id)
    await db.commit()
    return WorkflowRunOut(**run_dict(run))


@router.post("/runs/{run_id}/pause", response_model=WorkflowRunOut)
async def pause_run(run_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    run = await db.get(WorkflowRun, run_id)
    if run is None or run.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Run not found")
    run.status = "paused"
    run.paused_at = datetime.now(UTC)
    run.execution_state = {**(run.execution_state or {}), "manual_pause": True}
    await db.commit()
    return WorkflowRunOut(**run_dict(run))


@router.post("/runs/{run_id}/resume", response_model=WorkflowRunOut)
async def resume_run(run_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    run = await db.get(WorkflowRun, run_id)
    if run is None or run.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Run not found")
    run.status = "completed"
    run.resumed_at = datetime.now(UTC)
    run.finished_at = datetime.now(UTC)
    run.output_payload = {"status": "completed", "resumed": True}
    await db.commit()
    return WorkflowRunOut(**run_dict(run))


@router.get("/runs", response_model=list[WorkflowRunOut])
async def list_runs(workspace_id: UUID, workflow_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(WorkflowRun).where(WorkflowRun.organization_id == current.organization_id, WorkflowRun.workspace_id == workspace_id)
    if workflow_id:
        query = query.where(WorkflowRun.workflow_id == workflow_id)
    rows = (await db.execute(query.order_by(WorkflowRun.created_at.desc()).limit(100))).scalars().all()
    return [WorkflowRunOut(**run_dict(item)) for item in rows]


@router.get("/runs/{run_id}/logs", response_model=list[WorkflowLogOut])
async def run_logs(run_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(WorkflowExecutionLog).where(WorkflowExecutionLog.organization_id == current.organization_id, WorkflowExecutionLog.workflow_run_id == run_id).order_by(WorkflowExecutionLog.created_at.asc()))).scalars().all()
    return [WorkflowLogOut(**log_dict(item)) for item in rows]


@router.get("/monitoring", response_model=MonitoringOut)
async def monitoring(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return MonitoringOut(**await monitoring_summary(db, current, workspace_id))
