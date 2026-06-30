from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class IntegrationOut(BaseModel):
    id: UUID
    provider: str
    slug: str | None = None
    name: str
    category: str
    description: str | None = None
    version: str
    auth_methods: list[str]
    capabilities: list[str]
    featured: bool
    status: str


class ConnectionCreate(BaseModel):
    workspace_id: UUID
    external_integration_id: UUID
    name: str = Field(min_length=1, max_length=180)
    auth_method: str = Field(default="api_key", max_length=60)
    credentials: dict = Field(default_factory=dict)
    settings: dict = Field(default_factory=dict)
    scopes: list[str] = Field(default_factory=list)


class ConnectionUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=180)
    settings: dict | None = None
    scopes: list[str] | None = None


class ConnectionOut(BaseModel):
    id: UUID
    workspace_id: UUID
    external_integration_id: UUID
    name: str
    status: str
    auth_method: str
    scopes: list[str]
    last_validated_at: datetime | None = None
    last_health_status: str | None = None
    expires_at: datetime | None = None
    created_at: datetime


class CredentialRotate(BaseModel):
    credentials: dict = Field(default_factory=dict)
    expires_at: datetime | None = None


class ConnectionTestResult(BaseModel):
    connection_id: UUID
    status: str
    message: str
    latency_ms: int | None = None


class HealthOut(BaseModel):
    connection_id: UUID
    status: str
    checked_at: datetime
    latency_ms: int | None = None
    error_message: str | None = None


class ActionExecute(BaseModel):
    action_key: str
    payload: dict = Field(default_factory=dict)


class TriggerExecute(BaseModel):
    trigger_key: str
    payload: dict = Field(default_factory=dict)


class ExecutionResult(BaseModel):
    status: str
    message: str
    data: dict


class ConnectionLogOut(BaseModel):
    id: UUID
    connected_account_id: UUID | None = None
    event_type: str
    status: str
    message: str | None = None
    latency_ms: int | None = None
    retry_count: int
    created_at: datetime


class MarketplaceSummary(BaseModel):
    categories: list[dict]
    featured: list[IntegrationOut]
    available_count: int
    installed_count: int

class ConnectorInstallRequest(BaseModel):
    workspace_id: UUID
    external_integration_id: UUID
    connector_definition_id: UUID | None = None
    name: str = Field(min_length=1, max_length=180)
    auth_method: str = "api_key"
    credentials: dict = Field(default_factory=dict)
    settings: dict = Field(default_factory=dict)
    scopes: list[str] = Field(default_factory=list)
    permission_state: dict = Field(default_factory=dict)


class ConnectorInstallationOut(BaseModel):
    id: UUID
    workspace_id: UUID
    connected_account_id: UUID | None
    external_integration_id: UUID
    connector_definition_id: UUID | None
    version_id: UUID | None
    lifecycle_state: str
    install_stage: str
    permission_state: dict
    configuration_state: dict
    health_summary: dict
    created_at: datetime
    updated_at: datetime


class SyncJobCreate(BaseModel):
    workspace_id: UUID
    connected_account_id: UUID
    job_type: str = "manual"
    cursor: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class SyncJobOut(BaseModel):
    id: UUID
    workspace_id: UUID
    connected_account_id: UUID
    job_type: str
    status: str
    cursor: str | None
    conflict_count: int
    records_processed: int
    retry_count: int
    started_at: datetime | None
    finished_at: datetime | None
    error_message: str | None
    metadata_json: dict
    created_at: datetime


class PlaygroundRunCreate(BaseModel):
    workspace_id: UUID
    connected_account_id: UUID | None = None
    connector_definition_id: UUID | None = None
    run_type: str = "action"
    request_payload: dict = Field(default_factory=dict)


class PlaygroundRunOut(BaseModel):
    id: UUID
    workspace_id: UUID
    connected_account_id: UUID | None
    connector_definition_id: UUID | None
    run_type: str
    status: str
    request_payload: dict
    response_payload: dict
    latency_ms: int | None
    created_at: datetime


class EnterpriseMarketplaceSummary(BaseModel):
    categories: list[dict]
    featured: list[IntegrationOut]
    available_count: int
    installed_count: int
    sdk: dict
    lifecycle: list[str]
    health_center: dict


class ConnectorAnalyticsSummary(BaseModel):
    workspace_id: UUID
    installs: int
    sync_jobs: int
    playground_runs: int
    active_connections: int
    lifecycle: list[str]
    metrics: dict