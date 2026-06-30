from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class IntegrationCategory(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "integration_categories"
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class ExternalIntegration(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "external_integrations"
    provider: Mapped[str] = mapped_column(String(80), index=True)
    slug: Mapped[str | None] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    category: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(40), default="1.0.0")
    auth_methods: Mapped[list[str]] = mapped_column(JSONB, default=list)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    config_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    compatibility: Mapped[dict] = mapped_column(JSONB, default=dict)
    documentation_url: Mapped[str | None] = mapped_column(Text)
    icon_url: Mapped[str | None] = mapped_column(Text)
    featured: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(40), default="available", index=True)


class ConnectorDefinition(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "connector_definitions"
    external_integration_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="CASCADE"), index=True)
    connector_key: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    handler_ref: Mapped[str] = mapped_column(String(240))
    interface_version: Mapped[str] = mapped_column(String(40), default="1")
    auth_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    config_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    rate_limit_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    health_check_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class ConnectedAccount(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "connected_accounts"
    external_integration_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="RESTRICT"), index=True)
    connector_definition_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connector_definitions.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    auth_method: Mapped[str] = mapped_column(String(60), default="api_key")
    credentials_ref: Mapped[str | None] = mapped_column(Text)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    last_validated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    last_health_status: Mapped[str | None] = mapped_column(String(40))
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    disabled_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class IntegrationCredential(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "integration_credentials"
    connected_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="CASCADE"), index=True)
    auth_method: Mapped[str] = mapped_column(String(60), index=True)
    secret_fingerprint: Mapped[str] = mapped_column(String(128), index=True)
    secret_ref: Mapped[str] = mapped_column(Text)
    secret_provider: Mapped[str] = mapped_column(String(80), default="external_secret_manager")
    rotation_version: Mapped[int] = mapped_column(Integer, default=1)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    last_rotated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class IntegrationActionDefinition(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "integration_action_definitions"
    external_integration_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="CASCADE"), index=True)
    key: Mapped[str] = mapped_column(String(160), index=True)
    name: Mapped[str] = mapped_column(String(180))
    description: Mapped[str | None] = mapped_column(Text)
    input_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class IntegrationTriggerDefinition(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "integration_trigger_definitions"
    external_integration_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="CASCADE"), index=True)
    key: Mapped[str] = mapped_column(String(160), index=True)
    name: Mapped[str] = mapped_column(String(180))
    description: Mapped[str | None] = mapped_column(Text)
    payload_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    subscription_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class ConnectionLog(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "connection_logs"
    connected_account_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    message: Mapped[str | None] = mapped_column(Text)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class IntegrationHealthCheck(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "integration_health_checks"
    connected_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    checked_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class APIKey(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "api_keys"
    __table_args__ = (UniqueConstraint("key_hash", name="uq_api_key_hash"),)
    name: Mapped[str] = mapped_column(String(180))
    key_prefix: Mapped[str] = mapped_column(String(24), index=True)
    key_hash: Mapped[str] = mapped_column(String(128))
    environment: Mapped[str] = mapped_column(String(40), default="development")
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    usage_count: Mapped[int] = mapped_column(BigInteger, default=0)
    last_used_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class WebhookEndpoint(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "webhook_endpoints"
    url: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    event_types: Mapped[list[str]] = mapped_column(JSONB, default=list)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active")


Index("ix_connected_accounts_workspace_status", ConnectedAccount.workspace_id, ConnectedAccount.status, ConnectedAccount.deleted_at)
Index("ix_connected_accounts_integration_status", ConnectedAccount.external_integration_id, ConnectedAccount.status)
Index("ix_integration_credentials_account_status", IntegrationCredential.connected_account_id, IntegrationCredential.status)
Index("ix_connection_logs_account_created", ConnectionLog.connected_account_id, ConnectionLog.created_at)
Index("ix_health_checks_account_checked", IntegrationHealthCheck.connected_account_id, IntegrationHealthCheck.checked_at)
Index("ix_api_keys_workspace_active", APIKey.workspace_id, APIKey.revoked_at, APIKey.deleted_at)
Index("ix_api_keys_workspace_env", APIKey.workspace_id, APIKey.environment, APIKey.deleted_at)
Index("ix_webhooks_workspace_status", WebhookEndpoint.workspace_id, WebhookEndpoint.status, WebhookEndpoint.deleted_at)

class ConnectorVersion(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, Base):
    __tablename__ = "connector_versions"
    connector_definition_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("connector_definitions.id", ondelete="CASCADE"), index=True)
    version: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    changelog: Mapped[str | None] = mapped_column(Text)
    migration_guide: Mapped[str | None] = mapped_column(Text)
    sdk_contract: Mapped[dict] = mapped_column(JSONB, default=dict)
    release_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)


class ConnectorInstallation(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "connector_installations"
    connected_account_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="SET NULL"), index=True)
    external_integration_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="RESTRICT"), index=True)
    connector_definition_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connector_definitions.id", ondelete="SET NULL"), index=True)
    version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connector_versions.id", ondelete="SET NULL"), index=True)
    lifecycle_state: Mapped[str] = mapped_column(String(40), default="installed", index=True)
    install_stage: Mapped[str] = mapped_column(String(60), default="permission_review")
    permission_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    configuration_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    health_summary: Mapped[dict] = mapped_column(JSONB, default=dict)


class ConnectorSyncJob(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "connector_sync_jobs"
    connected_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="CASCADE"), index=True)
    job_type: Mapped[str] = mapped_column(String(60), default="manual", index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    cursor: Mapped[str | None] = mapped_column(Text)
    conflict_count: Mapped[int] = mapped_column(Integer, default=0)
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ConnectorMarketplaceMetadata(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "connector_marketplace_metadata"
    external_integration_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="CASCADE"), index=True)
    developer_name: Mapped[str | None] = mapped_column(String(160))
    listing_status: Mapped[str] = mapped_column(String(40), default="published", index=True)
    rating_average: Mapped[str | None] = mapped_column(String(20))
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    download_count: Mapped[int] = mapped_column(Integer, default=0)
    install_count: Mapped[int] = mapped_column(Integer, default=0)
    documentation: Mapped[dict] = mapped_column(JSONB, default=dict)
    screenshots: Mapped[list[str]] = mapped_column(JSONB, default=list)
    dependency_map: Mapped[dict] = mapped_column(JSONB, default=dict)


class ConnectorPlaygroundRun(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "connector_playground_runs"
    connected_account_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="SET NULL"), index=True)
    connector_definition_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connector_definitions.id", ondelete="SET NULL"), index=True)
    run_type: Mapped[str] = mapped_column(String(60), default="action", index=True)
    status: Mapped[str] = mapped_column(String(40), default="completed", index=True)
    request_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    response_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)


class ConnectorAnalyticsRecord(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "connector_analytics_records"
    external_integration_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("external_integrations.id", ondelete="SET NULL"), index=True)
    connected_account_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="SET NULL"), index=True)
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[str] = mapped_column(String(80))
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_connector_versions_definition_status", ConnectorVersion.connector_definition_id, ConnectorVersion.status, ConnectorVersion.version)
Index("ix_connector_installations_workspace_state", ConnectorInstallation.workspace_id, ConnectorInstallation.lifecycle_state, ConnectorInstallation.deleted_at)
Index("ix_connector_sync_jobs_connection_status", ConnectorSyncJob.connected_account_id, ConnectorSyncJob.status, ConnectorSyncJob.created_at)
Index("ix_connector_marketplace_listing", ConnectorMarketplaceMetadata.listing_status, ConnectorMarketplaceMetadata.install_count)
Index("ix_connector_playground_workspace", ConnectorPlaygroundRun.workspace_id, ConnectorPlaygroundRun.run_type, ConnectorPlaygroundRun.created_at)
Index("ix_connector_analytics_workspace_metric", ConnectorAnalyticsRecord.workspace_id, ConnectorAnalyticsRecord.metric_name, ConnectorAnalyticsRecord.captured_at)