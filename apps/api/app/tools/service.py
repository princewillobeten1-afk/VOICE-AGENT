from datetime import UTC, datetime
from time import perf_counter
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event
from app.tools.models import McpServerDefinition, ToolDefinition, ToolExecution, ToolExecutionLog, ToolPermission, ToolVersion


def tool_dict(item: ToolDefinition) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "category_id": item.category_id, "name": item.name, "slug": item.slug, "description": item.description, "category": item.category, "provider_type": item.provider_type, "runtime_type": item.runtime_type, "status": item.status, "version": item.version, "input_schema": item.input_schema, "output_schema": item.output_schema, "auth_requirements": item.auth_requirements, "permission_requirements": item.permission_requirements, "retry_policy": item.retry_policy, "timeout_ms": item.timeout_ms, "cost_hint": item.cost_hint, "health_state": item.health_state, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


def version_dict(item: ToolVersion) -> dict:
    return {"id": item.id, "tool_id": item.tool_id, "version": item.version, "status": item.status, "change_summary": item.change_summary, "input_schema": item.input_schema, "output_schema": item.output_schema, "runtime_config": item.runtime_config, "published_at": item.published_at, "created_at": item.created_at}


def execution_dict(item: ToolExecution) -> dict:
    return {"id": item.id, "tool_id": item.tool_id, "tool_version_id": item.tool_version_id, "agent_id": item.agent_id, "conversation_id": item.conversation_id, "workflow_run_id": item.workflow_run_id, "chain_id": item.chain_id, "requested_by_user_id": item.requested_by_user_id, "status": item.status, "execution_mode": item.execution_mode, "input_payload": item.input_payload, "output_payload": item.output_payload, "validation_result": item.validation_result, "permission_result": item.permission_result, "retry_count": item.retry_count, "latency_ms": item.latency_ms, "cost_estimate": item.cost_estimate, "error_code": item.error_code, "error_message": item.error_message, "started_at": item.started_at, "finished_at": item.finished_at, "created_at": item.created_at}


def log_dict(item: ToolExecutionLog) -> dict:
    return {"id": item.id, "execution_id": item.execution_id, "event_type": item.event_type, "stage": item.stage, "level": item.level, "message": item.message, "payload": item.payload, "latency_ms": item.latency_ms, "created_at": item.created_at}


def mcp_dict(item: McpServerDefinition) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "slug": item.slug, "status": item.status, "transport_type": item.transport_type, "endpoint_ref": item.endpoint_ref, "auth_requirements": item.auth_requirements, "capabilities": item.capabilities, "session_policy": item.session_policy, "resource_discovery": item.resource_discovery, "prompt_discovery": item.prompt_discovery, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


async def emit_tool_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"tool.{name}", aggregate_type="tool", aggregate_id=aggregate_id, source="tool-runtime", payload=payload, metadata={"runtime": "universal-tool-platform"}))


def validate_payload(schema: dict, payload: dict) -> dict:
    required = schema.get("required", []) if schema else []
    missing = [field for field in required if field not in payload]
    errors = [{"code": "missing_required", "fields": missing}] if missing else []
    properties = schema.get("properties", {}) if schema else {}
    for key, config in properties.items():
        expected = config.get("type")
        if key not in payload:
            continue
        if expected == "string" and not isinstance(payload[key], str):
            errors.append({"code": "type_error", "field": key, "expected": expected})
        if expected == "object" and not isinstance(payload[key], dict):
            errors.append({"code": "type_error", "field": key, "expected": expected})
        if expected == "array" and not isinstance(payload[key], list):
            errors.append({"code": "type_error", "field": key, "expected": expected})
        if expected == "number" and not isinstance(payload[key], int | float):
            errors.append({"code": "type_error", "field": key, "expected": expected})
    return {"valid": not errors, "errors": errors}


async def permission_check(db: AsyncSession, current: CurrentUser, tool: ToolDefinition, action: str) -> dict:
    rows = (await db.execute(select(ToolPermission).where(ToolPermission.organization_id == current.organization_id, ToolPermission.tool_id == tool.id, ToolPermission.action == action, ToolPermission.deleted_at.is_(None)))).scalars().all()
    if any(row.effect == "deny" for row in rows):
        return {"allowed": False, "reason": "explicit_deny"}
    if not rows:
        return {"allowed": True, "reason": "default_org_rbac"}
    return {"allowed": any(row.effect == "allow" for row in rows), "reason": "tool_permission"}

async def execute_tool(db: AsyncSession, current: CurrentUser, tool: ToolDefinition, payload) -> ToolExecution:
    started = perf_counter()
    now = datetime.now(UTC)
    validation = validate_payload(tool.input_schema, payload.input_payload)
    permission = await permission_check(db, current, tool, "execute")
    status = "running" if validation["valid"] and permission["allowed"] and tool.status == "enabled" else "rejected"
    execution = ToolExecution(organization_id=current.organization_id, workspace_id=tool.workspace_id, tool_id=tool.id, agent_id=payload.agent_id, conversation_id=payload.conversation_id, workflow_run_id=payload.workflow_run_id, chain_id=payload.chain_id, requested_by_user_id=current.user.id, status=status, execution_mode=payload.execution_mode, input_payload=payload.input_payload, validation_result=validation, permission_result=permission, started_at=now if status == "running" else None)
    db.add(execution)
    await db.flush()
    db.add(ToolExecutionLog(organization_id=current.organization_id, workspace_id=tool.workspace_id, execution_id=execution.id, event_type="tool.requested", stage="request", message="Tool execution requested", payload={"tool": tool.slug, "runtime_type": tool.runtime_type}))
    if status == "rejected":
        execution.error_code = "validation_permission_or_status_failed"
        execution.error_message = "Tool execution rejected before runtime."
        db.add(ToolExecutionLog(organization_id=current.organization_id, workspace_id=tool.workspace_id, execution_id=execution.id, event_type="tool.rejected", stage="guardrails", level="warning", message=execution.error_message, payload={"validation": validation, "permission": permission, "status": tool.status}))
        await emit_tool_event(db, current, "execution.rejected", tool.workspace_id, tool.id, {"execution_id": str(execution.id)})
        return execution
    output = {"ok": True, "simulated": True, "tool": tool.slug, "result": "No external provider was called in Task 018."}
    execution.status = "completed"
    execution.output_payload = output
    execution.finished_at = datetime.now(UTC)
    execution.latency_ms = int((perf_counter() - started) * 1000)
    execution.cost_estimate = {"amount": 0, "currency": "USD", "reason": "simulated"}
    db.add(ToolExecutionLog(organization_id=current.organization_id, workspace_id=tool.workspace_id, execution_id=execution.id, event_type="tool.completed", stage="result", message="Tool execution completed in simulated runtime", payload=output, latency_ms=execution.latency_ms))
    await emit_tool_event(db, current, "execution.completed", tool.workspace_id, tool.id, {"execution_id": str(execution.id), "latency_ms": execution.latency_ms})
    return execution


async def analytics(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    tools = (await db.execute(select(func.count()).select_from(ToolDefinition).where(ToolDefinition.organization_id == current.organization_id, ToolDefinition.workspace_id == workspace_id, ToolDefinition.deleted_at.is_(None)))).scalar_one()
    executions = (await db.execute(select(func.count()).select_from(ToolExecution).where(ToolExecution.organization_id == current.organization_id, ToolExecution.workspace_id == workspace_id))).scalar_one()
    completed = (await db.execute(select(func.count()).select_from(ToolExecution).where(ToolExecution.organization_id == current.organization_id, ToolExecution.workspace_id == workspace_id, ToolExecution.status == "completed"))).scalar_one()
    failed = (await db.execute(select(func.count()).select_from(ToolExecution).where(ToolExecution.organization_id == current.organization_id, ToolExecution.workspace_id == workspace_id, ToolExecution.status.in_(["failed", "rejected"])))).scalar_one()
    avg_latency = (await db.execute(select(func.avg(ToolExecution.latency_ms)).where(ToolExecution.organization_id == current.organization_id, ToolExecution.workspace_id == workspace_id, ToolExecution.latency_ms.is_not(None)))).scalar_one_or_none()
    return {"tools": int(tools or 0), "executions": int(executions or 0), "completed": int(completed or 0), "failed": int(failed or 0), "average_latency_ms": int(avg_latency) if avg_latency else None, "mcp_readiness": {"server_registration": True, "tool_discovery": "modeled", "resource_discovery": "modeled", "prompt_discovery": "modeled", "external_transport": "deferred"}}
