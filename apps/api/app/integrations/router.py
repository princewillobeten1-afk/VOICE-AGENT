from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.integrations.connectors import ConnectorContext, connector_registry
from app.integrations.credentials import create_secret_ref, credential_fingerprint, redact_credential_metadata
from app.integrations.models import ConnectedAccount, ConnectionLog, ConnectorAnalyticsRecord, ConnectorInstallation, ConnectorMarketplaceMetadata, ConnectorPlaygroundRun, ConnectorSyncJob, ExternalIntegration, IntegrationCredential, IntegrationHealthCheck
from app.integrations.schemas import ActionExecute, ConnectionCreate, ConnectionLogOut, ConnectionOut, ConnectionTestResult, ConnectionUpdate, ConnectorAnalyticsSummary, ConnectorInstallRequest, ConnectorInstallationOut, CredentialRotate, EnterpriseMarketplaceSummary, ExecutionResult, HealthOut, IntegrationOut, MarketplaceSummary, PlaygroundRunCreate, PlaygroundRunOut, SyncJobCreate, SyncJobOut, TriggerExecute
from app.integrations.service import connection_out, create_connection, emit_integration_event, ensure_marketplace_seed, install_connector, installation_out, integration_out, log_connection, playground_out, sync_job_out, test_connection, trigger_sync_job

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/marketplace", response_model=MarketplaceSummary)
async def marketplace(workspace_id: UUID | None = None, q: str | None = None, category: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    await ensure_marketplace_seed(db)
    query = select(ExternalIntegration).where(ExternalIntegration.deleted_at.is_(None), ExternalIntegration.status == "available")
    if category:
        query = query.where(ExternalIntegration.category == category)
    if q:
        query = query.where(or_(ExternalIntegration.name.ilike(f"%{q}%"), ExternalIntegration.provider.ilike(f"%{q}%"), ExternalIntegration.category.ilike(f"%{q}%")))
    integrations = (await db.execute(query.order_by(ExternalIntegration.featured.desc(), ExternalIntegration.name.asc()))).scalars().all()
    featured = [item for item in integrations if item.featured][:6]
    installed_count = 0
    if workspace_id:
        installed_count = (await db.execute(select(func.count()).select_from(ConnectedAccount).where(ConnectedAccount.organization_id == current.organization_id, ConnectedAccount.workspace_id == workspace_id, ConnectedAccount.deleted_at.is_(None)))).scalar_one()
    categories = sorted({item.category for item in integrations})
    await db.commit()
    return MarketplaceSummary(categories=[{"slug": item, "name": item.replace("_", " ").title()} for item in categories], featured=[IntegrationOut(**integration_out(item)) for item in featured], available_count=len(integrations), installed_count=int(installed_count))


@router.get("/available", response_model=list[IntegrationOut])
async def available_integrations(q: str | None = None, category: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    await ensure_marketplace_seed(db)
    query = select(ExternalIntegration).where(ExternalIntegration.deleted_at.is_(None))
    if category:
        query = query.where(ExternalIntegration.category == category)
    if q:
        query = query.where(or_(ExternalIntegration.name.ilike(f"%{q}%"), ExternalIntegration.provider.ilike(f"%{q}%")))
    rows = (await db.execute(query.order_by(ExternalIntegration.featured.desc(), ExternalIntegration.name.asc()))).scalars().all()
    await db.commit()
    return [IntegrationOut(**integration_out(item)) for item in rows]


@router.get("/connections", response_model=list[ConnectionOut])
async def list_connections(workspace_id: UUID, status_filter: str | None = Query(default=None, alias="status"), current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(ConnectedAccount).where(ConnectedAccount.organization_id == current.organization_id, ConnectedAccount.workspace_id == workspace_id, ConnectedAccount.deleted_at.is_(None))
    if status_filter:
        query = query.where(ConnectedAccount.status == status_filter)
    rows = (await db.execute(query.order_by(ConnectedAccount.created_at.desc()))).scalars().all()
    return [ConnectionOut(**connection_out(item)) for item in rows]


@router.post("/connections", response_model=ConnectionOut, status_code=status.HTTP_201_CREATED)
async def create_connected_account(payload: ConnectionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    try:
        connection = await create_connection(db, current, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    await audit(db, "integration.connection.created", current.user.id, current.organization_id, "connected_account", connection.id)
    await db.commit()
    return ConnectionOut(**connection_out(connection))


@router.patch("/connections/{connection_id}", response_model=ConnectionOut)
async def update_connection(connection_id: UUID, payload: ConnectionUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await db.get(ConnectedAccount, connection_id)
    if connection is None or connection.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Connection not found")
    if payload.name is not None:
        connection.name = payload.name
    if payload.settings is not None:
        connection.settings = payload.settings
    if payload.scopes is not None:
        connection.scopes = payload.scopes
    connection.updated_by_user_id = current.user.id
    await log_connection(db, connection, "connection.updated", "success", "Connection updated.")
    await emit_integration_event(db, current, "integration.connection.updated", connection.workspace_id, "connected_account", connection.id, {"connection_name": connection.name})
    await audit(db, "integration.connection.updated", current.user.id, current.organization_id, "connected_account", connection.id)
    await db.commit()
    return ConnectionOut(**connection_out(connection))


@router.delete("/connections/{connection_id}", status_code=204)
async def delete_connection(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await db.get(ConnectedAccount, connection_id)
    if connection is None or connection.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Connection not found")
    connection.deleted_at = datetime.now(UTC)
    connection.status = "deleted"
    await log_connection(db, connection, "connection.deleted", "success", "Connection deleted.")
    await emit_integration_event(db, current, "integration.connection.deleted", connection.workspace_id, "connected_account", connection.id, {"connection_name": connection.name})
    await audit(db, "integration.connection.deleted", current.user.id, current.organization_id, "connected_account", connection.id)
    await db.commit()


@router.post("/connections/{connection_id}/enable", response_model=ConnectionOut)
async def enable_connection(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    connection.status = "active"
    connection.disabled_at = None
    await log_connection(db, connection, "connection.enabled", "success", "Connection enabled.")
    await db.commit()
    return ConnectionOut(**connection_out(connection))


@router.post("/connections/{connection_id}/disable", response_model=ConnectionOut)
async def disable_connection(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    connection.status = "disabled"
    connection.disabled_at = datetime.now(UTC)
    await log_connection(db, connection, "connection.disabled", "success", "Connection disabled.")
    await db.commit()
    return ConnectionOut(**connection_out(connection))


@router.post("/connections/{connection_id}/test", response_model=ConnectionTestResult)
async def test_connected_account(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    health = await test_connection(db, connection)
    await db.commit()
    return ConnectionTestResult(connection_id=connection.id, status=health.status, message="Connection test completed.", latency_ms=health.latency_ms)


@router.post("/connections/{connection_id}/reconnect", response_model=ConnectionOut)
async def reconnect_connection(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    connection.status = "active"
    await log_connection(db, connection, "connection.reconnected", "success", "Reconnect requested.")
    await emit_integration_event(db, current, "integration.connection.reconnected", connection.workspace_id, "connected_account", connection.id, {"connection_name": connection.name})
    await db.commit()
    return ConnectionOut(**connection_out(connection))


@router.post("/connections/{connection_id}/credentials/rotate", response_model=ConnectionOut)
async def rotate_credentials(connection_id: UUID, payload: CredentialRotate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    result = await db.execute(select(IntegrationCredential).where(IntegrationCredential.connected_account_id == connection.id, IntegrationCredential.status == "active"))
    for credential in result.scalars().all():
        credential.status = "rotated"
    secret_ref = create_secret_ref()
    connection.credentials_ref = secret_ref
    db.add(IntegrationCredential(organization_id=current.organization_id, workspace_id=connection.workspace_id, connected_account_id=connection.id, auth_method=connection.auth_method, secret_fingerprint=credential_fingerprint(payload.credentials), secret_ref=secret_ref, secret_provider="external_secret_manager", rotation_version=1, expires_at=payload.expires_at, last_rotated_at=datetime.now(UTC), metadata_json={"redacted": redact_credential_metadata(payload.credentials)}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id))
    await log_connection(db, connection, "credentials.rotated", "success", "Credentials rotated.")
    await emit_integration_event(db, current, "integration.credentials.rotated", connection.workspace_id, "connected_account", connection.id, {"connection_name": connection.name})
    await audit(db, "integration.credentials.rotated", current.user.id, current.organization_id, "connected_account", connection.id)
    await db.commit()
    return ConnectionOut(**connection_out(connection))


@router.get("/connections/{connection_id}/health", response_model=list[HealthOut])
async def connection_health(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    rows = (await db.execute(select(IntegrationHealthCheck).where(IntegrationHealthCheck.connected_account_id == connection.id).order_by(IntegrationHealthCheck.checked_at.desc()).limit(20))).scalars().all()
    return [HealthOut(connection_id=row.connected_account_id, status=row.status, checked_at=row.checked_at, latency_ms=row.latency_ms, error_message=row.error_message) for row in rows]


@router.get("/connections/{connection_id}/logs", response_model=list[ConnectionLogOut])
async def connection_logs(connection_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    rows = (await db.execute(select(ConnectionLog).where(ConnectionLog.connected_account_id == connection.id).order_by(ConnectionLog.created_at.desc()).limit(50))).scalars().all()
    return [ConnectionLogOut(id=row.id, connected_account_id=row.connected_account_id, event_type=row.event_type, status=row.status, message=row.message, latency_ms=row.latency_ms, retry_count=row.retry_count, created_at=row.created_at) for row in rows]


@router.post("/connections/{connection_id}/actions", response_model=ExecutionResult)
async def execute_action(connection_id: UUID, payload: ActionExecute, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    result = await connector_registry.get(None).execute_action(ConnectorContext(str(connection.organization_id), str(connection.workspace_id), str(connection.id), connection.settings), payload.action_key, payload.payload)
    await log_connection(db, connection, "action.executed", result.status, result.message)
    await emit_integration_event(db, current, "integration.action.executed", connection.workspace_id, "connected_account", connection.id, {"action_key": payload.action_key, "status": result.status})
    await db.commit()
    return ExecutionResult(status=result.status, message=result.message, data=result.data)


@router.post("/connections/{connection_id}/triggers", response_model=ExecutionResult)
async def execute_trigger(connection_id: UUID, payload: TriggerExecute, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    connection = await get_connection_or_404(db, connection_id, current)
    result = await connector_registry.get(None).execute_trigger(ConnectorContext(str(connection.organization_id), str(connection.workspace_id), str(connection.id), connection.settings), payload.trigger_key, payload.payload)
    await log_connection(db, connection, "trigger.fired", result.status, result.message)
    await emit_integration_event(db, current, "integration.trigger.fired", connection.workspace_id, "connected_account", connection.id, {"trigger_key": payload.trigger_key, "status": result.status})
    await db.commit()
    return ExecutionResult(status=result.status, message=result.message, data=result.data)




@router.get("/enterprise-marketplace", response_model=EnterpriseMarketplaceSummary)
async def enterprise_marketplace(workspace_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    base = await marketplace(workspace_id=workspace_id, q=None, category=None, current=current, db=db)
    return EnterpriseMarketplaceSummary(categories=base.categories, featured=base.featured, available_count=base.available_count, installed_count=base.installed_count, sdk={"templates": ["oauth2", "api_key", "webhook", "sync"], "contract_version": "1", "testing": "fixture_ready"}, lifecycle=["draft", "published", "installed", "ready", "syncing", "degraded", "deprecated", "rollback_ready"], health_center={"tracks": ["availability", "auth", "sync", "latency", "rate_limits", "version_compatibility"]})


@router.post("/installations", response_model=ConnectorInstallationOut, status_code=status.HTTP_201_CREATED)
async def install_marketplace_connector(payload: ConnectorInstallRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    try:
        installation = await install_connector(db, current, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    await audit(db, "integration.connector.installed", current.user.id, current.organization_id, "connector_installation", installation.id)
    await db.commit()
    return ConnectorInstallationOut(**installation_out(installation))


@router.get("/installations", response_model=list[ConnectorInstallationOut])
async def list_connector_installations(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ConnectorInstallation).where(ConnectorInstallation.organization_id == current.organization_id, ConnectorInstallation.workspace_id == workspace_id, ConnectorInstallation.deleted_at.is_(None)).order_by(ConnectorInstallation.created_at.desc()))).scalars().all()
    return [ConnectorInstallationOut(**installation_out(item)) for item in rows]


@router.post("/sync-jobs", response_model=SyncJobOut, status_code=status.HTTP_201_CREATED)
async def create_sync_job(payload: SyncJobCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    try:
        job = await trigger_sync_job(db, current, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    await db.commit()
    return SyncJobOut(**sync_job_out(job))


@router.get("/sync-jobs", response_model=list[SyncJobOut])
async def list_sync_jobs(workspace_id: UUID, connected_account_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(ConnectorSyncJob).where(ConnectorSyncJob.organization_id == current.organization_id, ConnectorSyncJob.workspace_id == workspace_id)
    if connected_account_id:
        query = query.where(ConnectorSyncJob.connected_account_id == connected_account_id)
    rows = (await db.execute(query.order_by(ConnectorSyncJob.created_at.desc()).limit(100))).scalars().all()
    return [SyncJobOut(**sync_job_out(item)) for item in rows]


@router.post("/playground-runs", response_model=PlaygroundRunOut, status_code=status.HTTP_201_CREATED)
async def create_playground_run(payload: PlaygroundRunCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    run = ConnectorPlaygroundRun(organization_id=current.organization_id, workspace_id=payload.workspace_id, connected_account_id=payload.connected_account_id, connector_definition_id=payload.connector_definition_id, run_type=payload.run_type, status="completed", request_payload=payload.request_payload, response_payload={"ok": True, "mode": "simulated", "message": "Connector playground run recorded."}, latency_ms=24)
    db.add(run)
    await db.commit()
    return PlaygroundRunOut(**playground_out(run))


@router.get("/analytics", response_model=ConnectorAnalyticsSummary)
async def connector_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    installs = int((await db.execute(select(func.count()).select_from(ConnectorInstallation).where(ConnectorInstallation.organization_id == current.organization_id, ConnectorInstallation.workspace_id == workspace_id, ConnectorInstallation.deleted_at.is_(None)))).scalar_one() or 0)
    sync_jobs = int((await db.execute(select(func.count()).select_from(ConnectorSyncJob).where(ConnectorSyncJob.organization_id == current.organization_id, ConnectorSyncJob.workspace_id == workspace_id))).scalar_one() or 0)
    playground_runs = int((await db.execute(select(func.count()).select_from(ConnectorPlaygroundRun).where(ConnectorPlaygroundRun.organization_id == current.organization_id, ConnectorPlaygroundRun.workspace_id == workspace_id))).scalar_one() or 0)
    active_connections = int((await db.execute(select(func.count()).select_from(ConnectedAccount).where(ConnectedAccount.organization_id == current.organization_id, ConnectedAccount.workspace_id == workspace_id, ConnectedAccount.status == "active", ConnectedAccount.deleted_at.is_(None)))).scalar_one() or 0)
    return ConnectorAnalyticsSummary(workspace_id=workspace_id, installs=installs, sync_jobs=sync_jobs, playground_runs=playground_runs, active_connections=active_connections, lifecycle=["installed", "ready", "syncing", "degraded", "deprecated"], metrics={"sdk_contract": "v1", "health_center": "ready", "marketplace": "enterprise"})

async def get_connection_or_404(db: AsyncSession, connection_id: UUID, current: CurrentUser) -> ConnectedAccount:
    connection = await db.get(ConnectedAccount, connection_id)
    if connection is None or connection.organization_id != current.organization_id or connection.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return connection