from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.tools.models import McpServerDefinition, ToolDefinition, ToolExecution, ToolExecutionLog, ToolVersion
from app.tools.schemas import McpServerCreate, McpServerOut, ToolAnalyticsOut, ToolCreate, ToolExecuteRequest, ToolExecutionLogOut, ToolExecutionOut, ToolOut, ToolUpdate, ToolVersionOut
from app.tools.service import analytics, execute_tool, execution_dict, log_dict, mcp_dict, tool_dict, validate_payload, version_dict

router = APIRouter(prefix="/tools", tags=["tool-runtime"])


@router.get("", response_model=list[ToolOut])
async def list_tools(workspace_id: UUID, category: str | None = None, q: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(ToolDefinition).where(ToolDefinition.organization_id == current.organization_id, ToolDefinition.workspace_id == workspace_id, ToolDefinition.deleted_at.is_(None))
    if category:
        query = query.where(ToolDefinition.category == category)
    if q:
        query = query.where(or_(ToolDefinition.name.ilike(f"%{q}%"), ToolDefinition.description.ilike(f"%{q}%")))
    rows = (await db.execute(query.order_by(ToolDefinition.updated_at.desc()).limit(100))).scalars().all()
    return [ToolOut(**tool_dict(item)) for item in rows]


@router.post("", response_model=ToolOut, status_code=status.HTTP_201_CREATED)
async def register_tool(payload: ToolCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    tool = ToolDefinition(organization_id=current.organization_id, workspace_id=payload.workspace_id, category_id=payload.category_id, name=payload.name, slug=payload.slug, description=payload.description, category=payload.category, provider_type=payload.provider_type, runtime_type=payload.runtime_type, status=payload.status, version=payload.version, input_schema=payload.input_schema, output_schema=payload.output_schema, auth_requirements=payload.auth_requirements, permission_requirements=payload.permission_requirements, retry_policy=payload.retry_policy, timeout_ms=payload.timeout_ms, cost_hint=payload.cost_hint, health_state={"status": "unknown"}, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(tool)
    await db.flush()
    version = ToolVersion(organization_id=current.organization_id, workspace_id=payload.workspace_id, tool_id=tool.id, version=payload.version, status="published" if payload.status == "enabled" else "draft", change_summary="Initial tool registration", input_schema=payload.input_schema, output_schema=payload.output_schema, runtime_config={"runtime_type": payload.runtime_type}, published_at=datetime.now(UTC) if payload.status == "enabled" else None, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    await audit(db, "tool.registered", current.user.id, current.organization_id, "tool", tool.id)
    await db.commit()
    return ToolOut(**tool_dict(tool))


@router.patch("/{tool_id}", response_model=ToolOut)
async def update_tool(tool_id: UUID, payload: ToolUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    tool = await db.get(ToolDefinition, tool_id)
    if tool is None or tool.organization_id != current.organization_id or tool.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Tool not found")
    for field in ["name", "description", "category", "provider_type", "runtime_type", "status", "version", "input_schema", "output_schema", "auth_requirements", "permission_requirements", "retry_policy", "timeout_ms", "cost_hint", "health_state", "metadata_json"]:
        value = getattr(payload, field)
        if value is not None:
            setattr(tool, field, value)
    tool.updated_by_user_id = current.user.id
    await db.commit()
    return ToolOut(**tool_dict(tool))


@router.post("/{tool_id}/enable", response_model=ToolOut)
async def enable_tool(tool_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    tool = await db.get(ToolDefinition, tool_id)
    if tool is None or tool.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Tool not found")
    tool.status = "enabled"
    await db.commit()
    return ToolOut(**tool_dict(tool))


@router.post("/{tool_id}/disable", response_model=ToolOut)
async def disable_tool(tool_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    tool = await db.get(ToolDefinition, tool_id)
    if tool is None or tool.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Tool not found")
    tool.status = "disabled"
    await db.commit()
    return ToolOut(**tool_dict(tool))


@router.post("/{tool_id}/validate")
async def validate_tool_call(tool_id: UUID, payload: ToolExecuteRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    tool = await db.get(ToolDefinition, tool_id)
    if tool is None or tool.organization_id != current.organization_id or tool.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return validate_payload(tool.input_schema, payload.input_payload)


@router.post("/{tool_id}/execute", response_model=ToolExecutionOut, status_code=status.HTTP_201_CREATED)
async def run_tool(tool_id: UUID, payload: ToolExecuteRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    tool = await db.get(ToolDefinition, tool_id)
    if tool is None or tool.organization_id != current.organization_id or tool.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Tool not found")
    execution = await execute_tool(db, current, tool, payload)
    await audit(db, "tool.executed", current.user.id, current.organization_id, "tool_execution", execution.id)
    await db.commit()
    return ToolExecutionOut(**execution_dict(execution))

@router.get("/{tool_id}/versions", response_model=list[ToolVersionOut])
async def list_versions(tool_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ToolVersion).where(ToolVersion.organization_id == current.organization_id, ToolVersion.tool_id == tool_id).order_by(ToolVersion.created_at.desc()))).scalars().all()
    return [ToolVersionOut(**version_dict(item)) for item in rows]


@router.get("/executions/history", response_model=list[ToolExecutionOut])
async def execution_history(workspace_id: UUID, tool_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(ToolExecution).where(ToolExecution.organization_id == current.organization_id, ToolExecution.workspace_id == workspace_id)
    if tool_id:
        query = query.where(ToolExecution.tool_id == tool_id)
    rows = (await db.execute(query.order_by(ToolExecution.created_at.desc()).limit(100))).scalars().all()
    return [ToolExecutionOut(**execution_dict(item)) for item in rows]


@router.get("/executions/{execution_id}/logs", response_model=list[ToolExecutionLogOut])
async def execution_logs(execution_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ToolExecutionLog).where(ToolExecutionLog.organization_id == current.organization_id, ToolExecutionLog.execution_id == execution_id).order_by(ToolExecutionLog.created_at.asc()))).scalars().all()
    return [ToolExecutionLogOut(**log_dict(item)) for item in rows]


@router.get("/analytics/summary", response_model=ToolAnalyticsOut)
async def tool_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return ToolAnalyticsOut(**await analytics(db, current, workspace_id))


@router.post("/mcp-servers", response_model=McpServerOut, status_code=status.HTTP_201_CREATED)
async def register_mcp_server(payload: McpServerCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    server = McpServerDefinition(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, slug=payload.slug, status=payload.status, transport_type=payload.transport_type, endpoint_ref=payload.endpoint_ref, auth_requirements=payload.auth_requirements, capabilities=payload.capabilities, session_policy=payload.session_policy, resource_discovery=payload.resource_discovery, prompt_discovery=payload.prompt_discovery, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(server)
    await db.commit()
    return McpServerOut(**mcp_dict(server))


@router.get("/mcp-servers", response_model=list[McpServerOut])
async def list_mcp_servers(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(McpServerDefinition).where(McpServerDefinition.organization_id == current.organization_id, McpServerDefinition.workspace_id == workspace_id, McpServerDefinition.deleted_at.is_(None)).order_by(McpServerDefinition.updated_at.desc()))).scalars().all()
    return [McpServerOut(**mcp_dict(item)) for item in rows]
