from datetime import datetime
from uuid import UUID
from pydantic import AnyHttpUrl, BaseModel, Field


class APIKeyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    workspace_id: UUID
    environment: str = "development"
    scopes: list[str] = Field(default_factory=lambda: ["read"])
    expires_at: datetime | None = None


class APIKeyOut(BaseModel):
    id: UUID
    name: str
    key_prefix: str
    environment: str = "development"
    scopes: list[str]
    last_used_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    created_at: datetime


class APIKeyCreated(BaseModel):
    key: APIKeyOut
    secret_key: str
    message: str = "Store this secret now. VoiceSense will not show it again."


class APIKeyUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=180)


class WebhookCreate(BaseModel):
    workspace_id: UUID
    url: AnyHttpUrl
    description: str | None = None
    event_types: list[str] = Field(default_factory=list)


class WebhookOut(BaseModel):
    id: UUID
    url: str
    description: str | None = None
    event_types: list[str]
    status: str
    created_at: datetime


class WebhookCreated(BaseModel):
    webhook: WebhookOut
    signing_secret: str
    message: str = "Store this signing secret now. VoiceSense will not show it again."


class DeveloperSettingsOut(BaseModel):
    default_scopes: list[str]
    webhook_retry_policy: dict
    rate_limit_policy: dict


class UsageSummary(BaseModel):
    total_requests: int
    success_rate: float
    error_rate: float
    average_latency_ms: int
    rate_limit_usage: float

class OAuthApplicationCreate(BaseModel):
    workspace_id: UUID
    name: str = Field(min_length=2, max_length=180)
    redirect_uris: list[str] = Field(default_factory=list)
    allowed_scopes: list[str] = Field(default_factory=lambda: ["read"])
    environment: str = "development"


class OAuthApplicationOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    client_id: str
    redirect_uris: list[str]
    allowed_scopes: list[str]
    environment: str
    status: str
    created_at: datetime


class OAuthApplicationCreated(BaseModel):
    application: OAuthApplicationOut
    client_secret: str
    message: str = "Store this client secret now. VoiceSense will not show it again."


class RateLimitPolicyCreate(BaseModel):
    workspace_id: UUID
    name: str
    environment: str = "development"
    subject_type: str = "organization"
    subject_ref: str | None = None
    endpoint_pattern: str | None = None
    requests_per_minute: int = 600
    burst_limit: int = 120
    quota_limit: int | None = None
    quota_window: str = "month"
    metadata_json: dict = Field(default_factory=dict)


class RateLimitPolicyOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    environment: str
    subject_type: str
    subject_ref: str | None
    endpoint_pattern: str | None
    requests_per_minute: int
    burst_limit: int
    quota_limit: int | None
    quota_window: str
    status: str
    metadata_json: dict
    created_at: datetime


class APIExplorerRunCreate(BaseModel):
    workspace_id: UUID
    api_key_id: UUID | None = None
    method: str = "GET"
    path: str
    request_headers: dict = Field(default_factory=dict)
    request_body: dict = Field(default_factory=dict)


class APIExplorerRunOut(BaseModel):
    id: UUID
    workspace_id: UUID
    api_key_id: UUID | None
    user_id: UUID | None
    method: str
    path: str
    response_status: int
    response_headers: dict
    response_body: dict
    latency_ms: int | None
    timeline: list[dict]
    code_samples: dict
    created_at: datetime


class SandboxResourceCreate(BaseModel):
    workspace_id: UUID
    resource_type: str
    name: str
    fixture_payload: dict = Field(default_factory=dict)
    reset_policy: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class SandboxResourceOut(BaseModel):
    id: UUID
    workspace_id: UUID
    resource_type: str
    name: str
    status: str
    fixture_payload: dict
    reset_policy: dict
    metadata_json: dict
    created_at: datetime


class APIVersionOut(BaseModel):
    id: UUID
    version: str
    release_channel: str
    status: str
    changelog: str | None
    migration_guide_url: str | None
    deprecation_notice: str | None
    sunset_at: datetime | None
    openapi_ref: str | None
    metadata_json: dict
    created_at: datetime


class SDKReleaseOut(BaseModel):
    id: UUID
    language: str
    package_name: str
    version: str
    status: str
    openapi_version: str | None
    install_command: str | None
    docs_url: str | None
    metadata_json: dict
    created_at: datetime


class CLIReleaseOut(BaseModel):
    id: UUID
    version: str
    status: str
    install_command: str | None
    supported_commands: list[str]
    changelog: str | None
    metadata_json: dict
    created_at: datetime


class DeveloperPortalSummary(BaseModel):
    sections: list[str]
    sdk_languages: list[str]
    cli_commands: list[str]
    openapi: dict
    assistant_ready: bool


class DeveloperAnalyticsSummary(BaseModel):
    total_requests: int
    success_rate: float
    error_rate: float
    average_latency_ms: int
    rate_limit_usage: float
    explorer_runs: int
    sandbox_resources: int
    oauth_apps: int
    active_api_keys: int