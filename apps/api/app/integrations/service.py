from datetime import UTC, datetime
from time import perf_counter
from uuid import UUID
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.integrations.connectors import ConnectorContext, connector_registry
from app.integrations.credentials import create_secret_ref, credential_fingerprint, redact_credential_metadata
from app.integrations.models import ConnectedAccount, ConnectionLog, ConnectorAnalyticsRecord, ConnectorDefinition, ConnectorInstallation, ConnectorMarketplaceMetadata, ConnectorPlaygroundRun, ConnectorSyncJob, ConnectorVersion, ExternalIntegration, IntegrationCategory, IntegrationCredential, IntegrationHealthCheck
from app.notifications.service import publish_domain_event

INTEGRATION_CATEGORIES = [
    ("communication", "Communication", "Email, chat, and collaboration platforms."),
    ("crm", "CRM", "Customer relationship management systems."),
    ("calendar", "Calendars", "Scheduling and calendar platforms."),
    ("storage", "Storage", "Cloud file and document storage."),
    ("automation", "Automation", "Workflow automation platforms."),
    ("messaging", "Messaging", "SMS, WhatsApp, and messaging providers."),
    ("payments", "Payments", "Payment gateways and billing providers."),
    ("ai", "AI Providers", "LLM, speech, and AI infrastructure providers."),
    ("database", "Databases", "Databases and structured data systems."),
    ("project_management", "Project Management", "Tasks, docs, and project collaboration."),
    ("support", "Support", "Help desk and customer support systems."),
    ("productivity", "Productivity", "Workspace, docs, and knowledge productivity tools."),
    ("development", "Development", "Source control, issue tracking, and engineering workflows."),
]

MARKETPLACE_SEEDS = [
    ("gmail", "Gmail", "communication", ["oauth2", "oauth_pkce"], ["send_email", "new_email"]),
    ("slack", "Slack", "communication", ["oauth2"], ["send_message", "new_message"]),
    ("hubspot", "HubSpot", "crm", ["oauth2", "api_key"], ["create_contact", "contact_updated"]),
    ("google-calendar", "Google Calendar", "calendar", ["oauth2", "oauth_pkce"], ["schedule_meeting", "event_created"]),
    ("google-drive", "Google Drive", "storage", ["oauth2"], ["upload_file", "file_uploaded"]),
    ("stripe", "Stripe", "payments", ["api_key", "webhook"], ["create_customer", "payment_received"]),
    ("openai", "OpenAI", "ai", ["api_key"], ["generate_response", "usage_recorded"]),
    ("postgresql", "PostgreSQL", "database", ["basic", "custom_headers"], ["query", "row_created"]),
    ("notion", "Notion", "project_management", ["oauth2", "bearer"], ["create_page", "database_updated"]),
    ("salesforce", "Salesforce", "crm", ["oauth2", "jwt"], ["create_lead", "account_updated"]),
    ("zendesk", "Zendesk", "support", ["oauth2", "api_key"], ["create_ticket", "ticket_updated"]),
    ("github", "GitHub", "development", ["oauth2", "app"], ["create_issue", "pull_request_opened"]),
]


def integration_out(item: ExternalIntegration) -> dict:
    return {"id": item.id, "provider": item.provider, "slug": item.slug, "name": item.name, "category": item.category, "description": item.description, "version": item.version, "auth_methods": item.auth_methods, "capabilities": item.capabilities, "featured": item.featured, "status": item.status}


def connection_out(item: ConnectedAccount) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "external_integration_id": item.external_integration_id, "name": item.name, "status": item.status, "auth_method": item.auth_method, "scopes": item.scopes, "last_validated_at": item.last_validated_at, "last_health_status": item.last_health_status, "expires_at": item.expires_at, "created_at": item.created_at}


async def ensure_marketplace_seed(db: AsyncSession) -> None:
    existing = (await db.execute(select(func.count()).select_from(ExternalIntegration))).scalar_one()
    if existing:
        return
    for index, (slug, name, category, auth_methods, capabilities) in enumerate(MARKETPLACE_SEEDS):
        integration = ExternalIntegration(provider=slug, slug=slug, name=name, category=category, description=f"Provider-agnostic foundation record for {name}.", version="1.0.0", auth_methods=auth_methods, capabilities=capabilities, featured=index < 4, status="available", config_schema={"required": []}, compatibility={"voicesense": ">=0.1.0"})
        db.add(integration)
        await db.flush()
        db.add(ConnectorDefinition(external_integration_id=integration.id, connector_key=f"{slug}.placeholder", handler_ref="app.integrations.connectors.PlaceholderConnector", interface_version="1", auth_schema={"methods": auth_methods}, retry_policy={"max_attempts": 3, "backoff": "exponential"}, health_check_config={"mode": "placeholder"}))
    for order, (slug, name, description) in enumerate(INTEGRATION_CATEGORIES):
        db.add(IntegrationCategory(slug=slug, name=name, description=description, sort_order=order))
    await db.flush()


async def emit_integration_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, aggregate_type: str, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(name=name, organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, aggregate_type=aggregate_type, aggregate_id=aggregate_id, payload=payload, source="integrations"))


async def create_connection(db: AsyncSession, current: CurrentUser, payload) -> ConnectedAccount:
    integration = await db.get(ExternalIntegration, payload.external_integration_id)
    if integration is None or integration.deleted_at is not None:
        raise ValueError("Integration not found")
    connector_def = (await db.execute(select(ConnectorDefinition).where(ConnectorDefinition.external_integration_id == integration.id, ConnectorDefinition.status == "active"))).scalar_one_or_none()
    secret_ref = create_secret_ref()
    connection = ConnectedAccount(organization_id=current.organization_id, workspace_id=payload.workspace_id, external_integration_id=integration.id, connector_definition_id=connector_def.id if connector_def else None, name=payload.name, status="active", auth_method=payload.auth_method, credentials_ref=secret_ref, settings=payload.settings, scopes=payload.scopes, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(connection)
    await db.flush()
    db.add(IntegrationCredential(organization_id=current.organization_id, workspace_id=payload.workspace_id, connected_account_id=connection.id, auth_method=payload.auth_method, secret_fingerprint=credential_fingerprint(payload.credentials), secret_ref=secret_ref, secret_provider="external_secret_manager", metadata_json={"redacted": redact_credential_metadata(payload.credentials)}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id))
    await log_connection(db, connection, "connection.created", "success", "Connection created.")
    await emit_integration_event(db, current, "integration.connection.created", payload.workspace_id, "connected_account", connection.id, {"integration": integration.slug or integration.provider, "connection_name": connection.name})
    return connection


async def log_connection(db: AsyncSession, connection: ConnectedAccount, event_type: str, status: str, message: str | None = None, latency_ms: int | None = None) -> None:
    db.add(ConnectionLog(organization_id=connection.organization_id, workspace_id=connection.workspace_id, connected_account_id=connection.id, event_type=event_type, status=status, message=message, latency_ms=latency_ms))


async def test_connection(db: AsyncSession, connection: ConnectedAccount) -> IntegrationHealthCheck:
    started = perf_counter()
    connector = connector_registry.get(None)
    result = await connector.test_connection(ConnectorContext(organization_id=str(connection.organization_id), workspace_id=str(connection.workspace_id), connection_id=str(connection.id), settings=connection.settings))
    latency = int((perf_counter() - started) * 1000)
    connection.last_validated_at = datetime.now(UTC)
    connection.last_health_status = result.status
    health = IntegrationHealthCheck(organization_id=connection.organization_id, workspace_id=connection.workspace_id, connected_account_id=connection.id, status=result.status, checked_at=datetime.now(UTC), latency_ms=latency, error_message=None if result.ok else result.message)
    db.add(health)
    await log_connection(db, connection, "connection.tested", result.status, result.message, latency)
    return health

def installation_out(item: ConnectorInstallation) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "connected_account_id": item.connected_account_id, "external_integration_id": item.external_integration_id, "connector_definition_id": item.connector_definition_id, "version_id": item.version_id, "lifecycle_state": item.lifecycle_state, "install_stage": item.install_stage, "permission_state": item.permission_state, "configuration_state": item.configuration_state, "health_summary": item.health_summary, "created_at": item.created_at, "updated_at": item.updated_at}


def sync_job_out(item: ConnectorSyncJob) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "connected_account_id": item.connected_account_id, "job_type": item.job_type, "status": item.status, "cursor": item.cursor, "conflict_count": item.conflict_count, "records_processed": item.records_processed, "retry_count": item.retry_count, "started_at": item.started_at, "finished_at": item.finished_at, "error_message": item.error_message, "metadata_json": item.metadata_json, "created_at": item.created_at}


def playground_out(item: ConnectorPlaygroundRun) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "connected_account_id": item.connected_account_id, "connector_definition_id": item.connector_definition_id, "run_type": item.run_type, "status": item.status, "request_payload": item.request_payload, "response_payload": item.response_payload, "latency_ms": item.latency_ms, "created_at": item.created_at}


async def install_connector(db: AsyncSession, current: CurrentUser, payload) -> ConnectorInstallation:
    connection_payload = type("ConnectionPayload", (), {"workspace_id": payload.workspace_id, "external_integration_id": payload.external_integration_id, "name": payload.name, "auth_method": payload.auth_method, "credentials": payload.credentials, "settings": payload.settings, "scopes": payload.scopes})
    connection = await create_connection(db, current, connection_payload)
    version = None
    if connection.connector_definition_id:
        version = (await db.execute(select(ConnectorVersion).where(ConnectorVersion.connector_definition_id == connection.connector_definition_id, ConnectorVersion.status == "published").order_by(ConnectorVersion.created_at.desc()).limit(1))).scalar_one_or_none()
    installation = ConnectorInstallation(organization_id=current.organization_id, workspace_id=payload.workspace_id, connected_account_id=connection.id, external_integration_id=payload.external_integration_id, connector_definition_id=connection.connector_definition_id, version_id=version.id if version else None, lifecycle_state="ready", install_stage="ready_confirmation", permission_state=payload.permission_state or {"validated": True}, configuration_state={"wizard": "completed", "settings": payload.settings}, health_summary={"status": "pending_test"}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(installation)
    await db.flush()
    await emit_integration_event(db, current, "integration.connector.installed", payload.workspace_id, "connector_installation", installation.id, {"connection_id": str(connection.id)})
    return installation


async def trigger_sync_job(db: AsyncSession, current: CurrentUser, payload) -> ConnectorSyncJob:
    connection = await db.get(ConnectedAccount, payload.connected_account_id)
    if connection is None or connection.organization_id != current.organization_id:
        raise ValueError("Connection not found")
    now = datetime.now(UTC)
    job = ConnectorSyncJob(organization_id=current.organization_id, workspace_id=payload.workspace_id, connected_account_id=connection.id, job_type=payload.job_type, status="completed", cursor=payload.cursor, records_processed=0, started_at=now, finished_at=now, metadata_json=payload.metadata_json)
    db.add(job)
    await log_connection(db, connection, "sync.completed", "success", "Sync framework job recorded.")
    await emit_integration_event(db, current, "integration.sync.completed", payload.workspace_id, "connector_sync_job", job.id, {"job_type": payload.job_type})
    return job