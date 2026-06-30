from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ChannelCreate(BaseModel):
    workspace_id: UUID
    name: str
    channel_type: str
    provider: str
    status: str = "enabled"
    priority: int = 100
    region: str | None = None
    secret_ref: str | None = None
    capabilities: dict = Field(default_factory=dict)
    formatter_policy: dict = Field(default_factory=dict)
    config: dict = Field(default_factory=dict)


class ChannelOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    channel_type: str
    provider: str
    status: str
    priority: int
    region: str | None
    secret_ref: str | None
    capabilities: dict
    formatter_policy: dict
    health_state: dict
    config: dict
    created_at: datetime
    updated_at: datetime


class IdentityResolveRequest(BaseModel):
    workspace_id: UUID
    identity_type: str
    identity_value: str
    display_name: str | None = None
    canonical_customer_ref: str | None = None
    profile: dict = Field(default_factory=dict)
    preferences: dict = Field(default_factory=dict)


class IdentityOut(BaseModel):
    id: UUID
    workspace_id: UUID
    display_name: str | None
    identity_type: str
    identity_value: str
    canonical_customer_ref: str | None
    confidence_score: float | None
    source: str
    merge_state: dict
    profile: dict
    preferences: dict
    created_at: datetime
    updated_at: datetime


class SessionCreate(BaseModel):
    workspace_id: UUID
    channel_config_id: UUID | None = None
    customer_identity_id: UUID | None = None
    conversation_id: UUID | None = None
    agent_id: UUID | None = None
    external_thread_id: str | None = None
    channel_type: str
    subject: str | None = None
    context_state: dict = Field(default_factory=dict)
    workflow_state: dict = Field(default_factory=dict)


class SessionOut(BaseModel):
    id: UUID
    workspace_id: UUID
    channel_config_id: UUID | None
    customer_identity_id: UUID | None
    conversation_id: UUID | None
    agent_id: UUID | None
    external_thread_id: str | None
    channel_type: str
    status: str
    subject: str | None
    context_state: dict
    workflow_state: dict
    last_message_at: datetime | None
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    workspace_id: UUID
    channel_session_id: UUID | None = None
    channel_config_id: UUID | None = None
    customer_identity_id: UUID | None = None
    conversation_id: UUID | None = None
    agent_id: UUID | None = None
    direction: str = "outbound"
    channel_type: str
    message_type: str = "text"
    sender_ref: str | None = None
    recipient_ref: str | None = None
    subject: str | None = None
    text_body: str | None = None
    normalized_payload: dict = Field(default_factory=dict)
    formatted_payload: dict = Field(default_factory=dict)


class MessageOut(BaseModel):
    id: UUID
    workspace_id: UUID
    channel_session_id: UUID | None
    channel_config_id: UUID | None
    customer_identity_id: UUID | None
    conversation_id: UUID | None
    agent_id: UUID | None
    direction: str
    channel_type: str
    message_type: str
    provider_message_id: str | None
    sender_ref: str | None
    recipient_ref: str | None
    subject: str | None
    text_body: str | None
    normalized_payload: dict
    formatted_payload: dict
    status: str
    sent_at: datetime | None
    delivered_at: datetime | None
    read_at: datetime | None
    created_at: datetime
    updated_at: datetime


class DeliveryCreate(BaseModel):
    workspace_id: UUID
    message_id: UUID
    event_type: str
    provider: str | None = None
    provider_event_id: str | None = None
    status: str
    attempt: int = 1
    latency_ms: int | None = None
    error_code: str | None = None
    payload: dict = Field(default_factory=dict)


class DeliveryOut(BaseModel):
    id: UUID
    workspace_id: UUID
    message_id: UUID
    event_type: str
    provider: str | None
    provider_event_id: str | None
    status: str
    attempt: int
    latency_ms: int | None
    error_code: str | None
    payload: dict
    created_at: datetime


class TimelineOut(BaseModel):
    id: UUID
    workspace_id: UUID
    customer_identity_id: UUID | None
    channel_session_id: UUID | None
    message_id: UUID | None
    conversation_id: UUID | None
    event_type: str
    channel_type: str | None
    title: str
    summary: str | None
    event_payload: dict
    occurred_at: datetime | None
    created_at: datetime
