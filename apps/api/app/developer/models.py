from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class PersonalAccessToken(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "personal_access_tokens"
    __table_args__ = (UniqueConstraint("token_hash", name="uq_pat_token_hash"),)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    token_prefix: Mapped[str] = mapped_column(String(24), index=True)
    token_hash: Mapped[str] = mapped_column(String(128))
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class OAuthApplication(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "oauth_applications"
    __table_args__ = (UniqueConstraint("client_id", name="uq_oauth_application_client_id"),)
    name: Mapped[str] = mapped_column(String(180))
    client_id: Mapped[str] = mapped_column(String(80), index=True)
    client_secret_hash: Mapped[str] = mapped_column(String(128))
    redirect_uris: Mapped[list[str]] = mapped_column(JSONB, default=list)
    allowed_scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    environment: Mapped[str] = mapped_column(String(40), default="development")
    status: Mapped[str] = mapped_column(String(40), default="active")


class WebhookDelivery(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "webhook_deliveries"
    webhook_endpoint_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("webhook_endpoints.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(40), default="pending")
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    request_id: Mapped[str | None] = mapped_column(String(80), index=True)
    response_status_code: Mapped[int | None] = mapped_column(Integer)
    response_time_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class APIRequestLog(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "api_request_logs"
    api_key_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("api_keys.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    request_id: Mapped[str] = mapped_column(String(80), index=True)
    method: Mapped[str] = mapped_column(String(12))
    path: Mapped[str] = mapped_column(Text)
    status_code: Mapped[int] = mapped_column(index=True)
    response_time_ms: Mapped[int]
    ip_address: Mapped[str | None] = mapped_column(INET)
    error_code: Mapped[str | None] = mapped_column(String(120))
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class APIUsageBucket(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "api_usage_buckets"
    bucket_start: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    bucket_grain: Mapped[str] = mapped_column(String(20), default="day")
    environment: Mapped[str] = mapped_column(String(40), default="development")
    total_requests: Mapped[int] = mapped_column(Integer, default=0)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    rate_limited_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_latency_ms: Mapped[int] = mapped_column(Integer, default=0)


class SDKMetadata(IdMixin, TimestampMixin, Base):
    __tablename__ = "sdk_metadata"
    language: Mapped[str] = mapped_column(String(40), index=True)
    package_name: Mapped[str] = mapped_column(String(160))
    latest_version: Mapped[str | None] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), default="planned")
    repository_url: Mapped[str | None] = mapped_column(Text)
    docs_url: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DeveloperSetting(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "developer_settings"
    environment: Mapped[str] = mapped_column(String(40), default="development")
    default_scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    webhook_retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    rate_limit_policy: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_pats_user_active", PersonalAccessToken.user_id, PersonalAccessToken.revoked_at, PersonalAccessToken.deleted_at)
Index("ix_oauth_apps_workspace_status", OAuthApplication.workspace_id, OAuthApplication.status, OAuthApplication.deleted_at)
Index("ix_webhook_deliveries_endpoint_created", WebhookDelivery.webhook_endpoint_id, WebhookDelivery.created_at)
Index("ix_api_request_logs_workspace_created", APIRequestLog.workspace_id, APIRequestLog.created_at)
Index("ix_api_usage_buckets_workspace_bucket", APIUsageBucket.workspace_id, APIUsageBucket.bucket_grain, APIUsageBucket.bucket_start)
Index("ix_developer_settings_workspace_env", DeveloperSetting.workspace_id, DeveloperSetting.environment)

class APIVersion(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, Base):
    __tablename__ = "api_versions"
    version: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    release_channel: Mapped[str] = mapped_column(String(40), default="stable", index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    changelog: Mapped[str | None] = mapped_column(Text)
    migration_guide_url: Mapped[str | None] = mapped_column(Text)
    deprecation_notice: Mapped[str | None] = mapped_column(Text)
    sunset_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    openapi_ref: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class OAuthAccessToken(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "oauth_access_tokens"
    oauth_application_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("oauth_applications.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    token_hash: Mapped[str] = mapped_column(String(128), index=True)
    refresh_token_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class RateLimitPolicy(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "rate_limit_policies"
    name: Mapped[str] = mapped_column(String(180))
    environment: Mapped[str] = mapped_column(String(40), default="development", index=True)
    subject_type: Mapped[str] = mapped_column(String(60), default="organization", index=True)
    subject_ref: Mapped[str | None] = mapped_column(String(180), index=True)
    endpoint_pattern: Mapped[str | None] = mapped_column(Text)
    requests_per_minute: Mapped[int] = mapped_column(Integer, default=600)
    burst_limit: Mapped[int] = mapped_column(Integer, default=120)
    quota_limit: Mapped[int | None] = mapped_column(Integer)
    quota_window: Mapped[str] = mapped_column(String(40), default="month")
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SandboxResource(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "sandbox_resources"
    resource_type: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    fixture_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    reset_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class APIExplorerRun(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "api_explorer_runs"
    api_key_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("api_keys.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    method: Mapped[str] = mapped_column(String(12))
    path: Mapped[str] = mapped_column(Text)
    request_headers: Mapped[dict] = mapped_column(JSONB, default=dict)
    request_body: Mapped[dict] = mapped_column(JSONB, default=dict)
    response_status: Mapped[int] = mapped_column(Integer, default=200, index=True)
    response_headers: Mapped[dict] = mapped_column(JSONB, default=dict)
    response_body: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    timeline: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    code_samples: Mapped[dict] = mapped_column(JSONB, default=dict)


class CLIRelease(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, Base):
    __tablename__ = "cli_releases"
    version: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), default="planned", index=True)
    install_command: Mapped[str | None] = mapped_column(Text)
    supported_commands: Mapped[list[str]] = mapped_column(JSONB, default=list)
    changelog: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SDKRelease(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, Base):
    __tablename__ = "sdk_releases"
    language: Mapped[str] = mapped_column(String(40), index=True)
    package_name: Mapped[str] = mapped_column(String(160))
    version: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(40), default="planned", index=True)
    openapi_version: Mapped[str | None] = mapped_column(String(40), index=True)
    install_command: Mapped[str | None] = mapped_column(Text)
    docs_url: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_api_versions_status", APIVersion.release_channel, APIVersion.status, APIVersion.sunset_at)
Index("ix_oauth_tokens_app_status", OAuthAccessToken.oauth_application_id, OAuthAccessToken.status, OAuthAccessToken.expires_at)
Index("ix_rate_limit_policies_workspace_subject", RateLimitPolicy.workspace_id, RateLimitPolicy.subject_type, RateLimitPolicy.status)
Index("ix_sandbox_resources_workspace_type", SandboxResource.workspace_id, SandboxResource.resource_type, SandboxResource.status)
Index("ix_api_explorer_runs_workspace_created", APIExplorerRun.workspace_id, APIExplorerRun.created_at)
Index("ix_cli_releases_status", CLIRelease.status, CLIRelease.version)
Index("ix_sdk_releases_language_status", SDKRelease.language, SDKRelease.status, SDKRelease.version)