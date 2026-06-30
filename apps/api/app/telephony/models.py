from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class TelephonyProviderConfig(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "telephony_provider_configs"
    __table_args__ = (UniqueConstraint("workspace_id", "provider", "name", name="uq_telephony_provider_name"),)
    name: Mapped[str] = mapped_column(String(160))
    provider: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    region: Mapped[str | None] = mapped_column(String(80), index=True)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    failover_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    health_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)


class PhoneNumber(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "phone_numbers"
    __table_args__ = (UniqueConstraint("workspace_id", "e164", name="uq_phone_number_workspace_e164"),)
    provider_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("telephony_provider_configs.id", ondelete="SET NULL"), index=True)
    assigned_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    queue_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("call_queues.id", ondelete="SET NULL"), index=True)
    e164: Mapped[str] = mapped_column(String(32), index=True)
    label: Mapped[str | None] = mapped_column(String(160))
    number_type: Mapped[str] = mapped_column(String(40), default="local", index=True)
    country: Mapped[str | None] = mapped_column(String(8), index=True)
    region: Mapped[str | None] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    routing_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    compliance_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SipEndpoint(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "sip_endpoints"
    provider_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("telephony_provider_configs.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    domain: Mapped[str] = mapped_column(String(180), index=True)
    endpoint_type: Mapped[str] = mapped_column(String(60), default="trunk", index=True)
    auth_type: Mapped[str] = mapped_column(String(60), default="digest")
    secret_ref: Mapped[str | None] = mapped_column(Text)
    allowed_ips: Mapped[list[str]] = mapped_column(JSONB, default=list)
    headers: Mapped[dict] = mapped_column(JSONB, default=dict)
    routing_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)


class CallQueue(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "call_queues"
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    overflow_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    assignment_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    estimated_wait_seconds: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    analytics_state: Mapped[dict] = mapped_column(JSONB, default=dict)


class CallRoutingRule(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "call_routing_rules"
    phone_number_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("phone_numbers.id", ondelete="CASCADE"), index=True)
    queue_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("call_queues.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    priority: Mapped[int] = mapped_column(Integer, default=100, index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    conditions: Mapped[dict] = mapped_column(JSONB, default=dict)
    destination_type: Mapped[str] = mapped_column(String(60), default="agent", index=True)
    destination_ref: Mapped[str | None] = mapped_column(String(180))
    business_hours: Mapped[dict] = mapped_column(JSONB, default=dict)
    failover: Mapped[dict] = mapped_column(JSONB, default=dict)


class TelephonyCall(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "telephony_calls"
    provider_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("telephony_provider_configs.id", ondelete="SET NULL"), index=True)
    phone_number_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("phone_numbers.id", ondelete="SET NULL"), index=True)
    queue_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("call_queues.id", ondelete="SET NULL"), index=True)
    voice_session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_sessions.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    workflow_run_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    provider_call_id: Mapped[str | None] = mapped_column(String(180), index=True)
    direction: Mapped[str] = mapped_column(String(40), default="inbound", index=True)
    call_type: Mapped[str] = mapped_column(String(40), default="pstn", index=True)
    status: Mapped[str] = mapped_column(String(40), default="created", index=True)
    from_number: Mapped[str | None] = mapped_column(String(40), index=True)
    to_number: Mapped[str | None] = mapped_column(String(40), index=True)
    customer_ref: Mapped[str | None] = mapped_column(String(180), index=True)
    routing_result: Mapped[dict] = mapped_column(JSONB, default=dict)
    timeline_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    cost_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    answered_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    ended_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    end_reason: Mapped[str | None] = mapped_column(Text)


class TelephonyCallEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "telephony_call_events"
    call_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("telephony_calls.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    sequence_number: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(80), default="telephony", index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)


class CallRecording(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "call_recordings"
    call_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("telephony_calls.id", ondelete="CASCADE"), index=True)
    storage_object_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="metadata_only", index=True)
    recording_type: Mapped[str] = mapped_column(String(40), default="full")
    retention_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    access_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    stopped_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class CallMetric(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "call_metrics"
    call_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("telephony_calls.id", ondelete="CASCADE"), index=True)
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 3))
    unit: Mapped[str] = mapped_column(String(32), default="count")
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_telephony_providers_workspace_status", TelephonyProviderConfig.workspace_id, TelephonyProviderConfig.status, TelephonyProviderConfig.priority)
Index("ix_phone_numbers_workspace_status", PhoneNumber.workspace_id, PhoneNumber.status, PhoneNumber.country)
Index("ix_telephony_calls_workspace_status", TelephonyCall.workspace_id, TelephonyCall.status, TelephonyCall.started_at)
Index("ix_telephony_calls_numbers", TelephonyCall.from_number, TelephonyCall.to_number, TelephonyCall.started_at)
Index("ix_telephony_call_events_call_sequence", TelephonyCallEvent.call_id, TelephonyCallEvent.sequence_number)
Index("ix_call_metrics_workspace_name", CallMetric.workspace_id, CallMetric.metric_name, CallMetric.captured_at)
