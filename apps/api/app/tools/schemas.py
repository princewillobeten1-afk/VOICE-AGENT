from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ToolCreate(BaseModel):
    workspace_id: UUID
    category_id: UUID | None = None
    name: str = Field(min_length=2, max_length=180)
    slug: str = Field(min_length=2, max_length=140)
    description: str | None = None
    category: str = "custom"
    provider_type: str = "internal"
    runtime_type: str = "simulated"
    status: str = "enabled"
    version: str = "0.1.0"
    input_schema: dict = Field(default_factory=dict)
    output_schema: dict = Field(default_factory=dict)
    auth_requirements: dict = Field(default_factory=dict)
    permission_requirements: dict = Field(default_factory=dict)
    retry_policy: dict = Field(default_factory=dict)
    timeout_ms: int = 30000
    cost_hint: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class ToolUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    provider_type: str | None = None
    runtime_type: str | None = None
    status: str | None = None
    version: str | None = None
    input_schema: dict | None = None
    output_schema: dict | None = None
    auth_requirements: dict | None = None
    permission_requirements: dict | None = None
    retry_policy: dict | None = None
    timeout_ms: int | None = None
    cost_hint: dict | None = None
    health_state: dict | None = None
    metadata_json: dict | None = None


class ToolOut(BaseModel):
    id: UUID
    workspace_id: UUID
    category_id: UUID | None
    name: str
    slug: str
    description: str | None
    category: str
    provider_type: str
    runtime_type: str
    status: str
    version: str
    input_schema: dict
    output_schema: dict
    auth_requirements: dict
    permission_requirements: dict
    retry_policy: dict
    timeout_ms: int
    cost_hint: dict
    health_state: dict
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


class ToolVersionOut(BaseModel):
    id: UUID
    tool_id: UUID
    version: str
    status: str
    change_summary: str | None
    input_schema: dict
    output_schema: dict
    runtime_config: dict
    published_at: datetime | None
    created_at: datetime


class ToolExecuteRequest(BaseModel):
    agent_id: UUID | None = None
    conversation_id: UUID | None = None
    workflow_run_id: UUID | None = None
    chain_id: UUID | None = None
    execution_mode: str = "single"
    input_payload: dict = Field(default_factory=dict)


class ToolExecutionOut(BaseModel):
    id: UUID
    tool_id: UUID
    tool_version_id: UUID | None
    agent_id: UUID | None
    conversation_id: UUID | None
    workflow_run_id: UUID | None
    chain_id: UUID | None
    requested_by_user_id: UUID | None
    status: str
    execution_mode: str
    input_payload: dict
    output_payload: dict
    validation_result: dict
    permission_result: dict
    retry_count: int
    latency_ms: int | None
    cost_estimate: dict
    error_code: str | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime


class ToolExecutionLogOut(BaseModel):
    id: UUID
    execution_id: UUID
    event_type: str
    stage: str | None
    level: str
    message: str | None
    payload: dict
    latency_ms: int | None
    created_at: datetime


class McpServerCreate(BaseModel):
    workspace_id: UUID
    name: str
    slug: str
    status: str = "disabled"
    transport_type: str = "stdio"
    endpoint_ref: str | None = None
    auth_requirements: dict = Field(default_factory=dict)
    capabilities: dict = Field(default_factory=dict)
    session_policy: dict = Field(default_factory=dict)
    resource_discovery: dict = Field(default_factory=dict)
    prompt_discovery: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class McpServerOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    slug: str
    status: str
    transport_type: str
    endpoint_ref: str | None
    auth_requirements: dict
    capabilities: dict
    session_policy: dict
    resource_discovery: dict
    prompt_discovery: dict
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


class ToolAnalyticsOut(BaseModel):
    tools: int
    executions: int
    completed: int
    failed: int
    average_latency_ms: int | None
    mcp_readiness: dict
