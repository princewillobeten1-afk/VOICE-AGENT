from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ProviderCreate(BaseModel):
    workspace_id: UUID
    name: str
    provider: str
    status: str = "enabled"
    priority: int = 100
    region: str | None = None
    secret_ref: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    failover_policy: dict = Field(default_factory=dict)
    config: dict = Field(default_factory=dict)


class ProviderOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    provider: str
    status: str
    priority: int
    region: str | None
    secret_ref: str | None
    capabilities: list[str]
    failover_policy: dict
    health_state: dict
    config: dict
    created_at: datetime
    updated_at: datetime


class NumberCreate(BaseModel):
    workspace_id: UUID
    provider_config_id: UUID | None = None
    assigned_agent_id: UUID | None = None
    queue_id: UUID | None = None
    e164: str
    label: str | None = None
    number_type: str = "local"
    country: str | None = None
    region: str | None = None
    routing_config: dict = Field(default_factory=dict)
    compliance_config: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class NumberOut(BaseModel):
    id: UUID
    workspace_id: UUID
    provider_config_id: UUID | None
    assigned_agent_id: UUID | None
    queue_id: UUID | None
    e164: str
    label: str | None
    number_type: str
    country: str | None
    region: str | None
    status: str
    routing_config: dict
    compliance_config: dict
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


class QueueCreate(BaseModel):
    workspace_id: UUID
    name: str
    slug: str
    priority: int = 100
    overflow_policy: dict = Field(default_factory=dict)
    assignment_policy: dict = Field(default_factory=dict)
    estimated_wait_seconds: int | None = None


class QueueOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    slug: str
    priority: int
    overflow_policy: dict
    assignment_policy: dict
    estimated_wait_seconds: int | None
    status: str
    analytics_state: dict
    created_at: datetime
    updated_at: datetime


class CallCreate(BaseModel):
    workspace_id: UUID
    direction: str = "inbound"
    call_type: str = "pstn"
    from_number: str | None = None
    to_number: str | None = None
    customer_ref: str | None = None
    agent_id: UUID | None = None
    region: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class CallOut(BaseModel):
    id: UUID
    workspace_id: UUID
    provider_config_id: UUID | None
    phone_number_id: UUID | None
    queue_id: UUID | None
    voice_session_id: UUID | None
    conversation_id: UUID | None
    workflow_run_id: UUID | None
    agent_id: UUID | None
    provider_call_id: str | None
    direction: str
    call_type: str
    status: str
    from_number: str | None
    to_number: str | None
    customer_ref: str | None
    routing_result: dict
    timeline_state: dict
    cost_state: dict
    started_at: datetime | None
    answered_at: datetime | None
    ended_at: datetime | None
    duration_seconds: int | None
    end_reason: str | None
    created_at: datetime


class CallEventOut(BaseModel):
    id: UUID
    call_id: UUID
    event_type: str
    sequence_number: int
    source: str
    payload: dict
    latency_ms: int | None
    created_at: datetime
