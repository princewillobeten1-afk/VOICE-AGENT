from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class ChannelConfiguration(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "channel_configurations"
    __table_args__ = (UniqueConstraint("workspace_id", "channel_type", "name", name="uq_channel_config_workspace_type_name"),)
    name: Mapped[str] = mapped_column(String(160))
    channel_type: Mapped[str] = mapped_column(String(60), index=True)
    provider: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    region: Mapped[str | None] = mapped_column(String(80), index=True)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    capabilities: Mapped[dict] = mapped_column(JSONB, default=dict)
    formatter_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    health_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)


class CustomerIdentity(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "customer_identities"
    __table_args__ = (UniqueConstraint("workspace_id", "identity_type", "identity_value", name="uq_customer_identity_workspace_value"),)
    display_name: Mapped[str | None] = mapped_column(String(180))
    identity_type: Mapped[str] = mapped_column(String(60), index=True)
    identity_value: Mapped[str] = mapped_column(String(320), index=True)
    canonical_customer_ref: Mapped[str | None] = mapped_column(String(180), index=True)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 3))
    source: Mapped[str] = mapped_column(String(80), default="omnichannel")
    merge_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    profile: Mapped[dict] = mapped_column(JSONB, default=dict)
    preferences: Mapped[dict] = mapped_column(JSONB, default=dict)


class ChannelSession(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "channel_sessions"
    channel_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("channel_configurations.id", ondelete="SET NULL"), index=True)
    customer_identity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("customer_identities.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    external_thread_id: Mapped[str | None] = mapped_column(String(220), index=True)
    channel_type: Mapped[str] = mapped_column(String(60), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    subject: Mapped[str | None] = mapped_column(String(260))
    context_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    workflow_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    last_message_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class OmnichannelMessage(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "omnichannel_messages"
    channel_session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("channel_sessions.id", ondelete="SET NULL"), index=True)
    channel_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("channel_configurations.id", ondelete="SET NULL"), index=True)
    customer_identity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("customer_identities.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    direction: Mapped[str] = mapped_column(String(40), default="inbound", index=True)
    channel_type: Mapped[str] = mapped_column(String(60), index=True)
    message_type: Mapped[str] = mapped_column(String(60), default="text", index=True)
    provider_message_id: Mapped[str | None] = mapped_column(String(220), index=True)
    sender_ref: Mapped[str | None] = mapped_column(String(220), index=True)
    recipient_ref: Mapped[str | None] = mapped_column(String(220), index=True)
    subject: Mapped[str | None] = mapped_column(String(260))
    text_body: Mapped[str | None] = mapped_column(Text)
    normalized_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    formatted_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="received", index=True)
    sent_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    delivered_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    read_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class MessageAttachment(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "message_attachments"
    message_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("omnichannel_messages.id", ondelete="CASCADE"), index=True)
    storage_object_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    attachment_type: Mapped[str] = mapped_column(String(60), index=True)
    filename: Mapped[str | None] = mapped_column(String(260))
    content_type: Mapped[str | None] = mapped_column(String(120), index=True)
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    scan_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    access_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DeliveryEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "delivery_events"
    message_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("omnichannel_messages.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    provider: Mapped[str | None] = mapped_column(String(80), index=True)
    provider_event_id: Mapped[str | None] = mapped_column(String(220), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    error_code: Mapped[str | None] = mapped_column(String(120))
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class CustomerTimelineEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "customer_timeline_events"
    customer_identity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("customer_identities.id", ondelete="SET NULL"), index=True)
    channel_session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("channel_sessions.id", ondelete="SET NULL"), index=True)
    message_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("omnichannel_messages.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    channel_type: Mapped[str | None] = mapped_column(String(60), index=True)
    title: Mapped[str] = mapped_column(String(220))
    summary: Mapped[str | None] = mapped_column(Text)
    event_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    occurred_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class ChannelAnalytics(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "channel_analytics"
    channel_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("channel_configurations.id", ondelete="SET NULL"), index=True)
    channel_type: Mapped[str] = mapped_column(String(60), index=True)
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 3))
    unit: Mapped[str] = mapped_column(String(32), default="count")
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_channel_config_workspace_status", ChannelConfiguration.workspace_id, ChannelConfiguration.channel_type, ChannelConfiguration.status)
Index("ix_customer_identity_workspace_ref", CustomerIdentity.workspace_id, CustomerIdentity.canonical_customer_ref)
Index("ix_channel_sessions_workspace_status", ChannelSession.workspace_id, ChannelSession.channel_type, ChannelSession.status, ChannelSession.last_message_at)
Index("ix_omnichannel_messages_workspace_channel", OmnichannelMessage.workspace_id, OmnichannelMessage.channel_type, OmnichannelMessage.created_at)
Index("ix_delivery_events_message_status", DeliveryEvent.message_id, DeliveryEvent.status, DeliveryEvent.created_at)
Index("ix_customer_timeline_workspace_customer", CustomerTimelineEvent.workspace_id, CustomerTimelineEvent.customer_identity_id, CustomerTimelineEvent.occurred_at)
Index("ix_channel_analytics_workspace_metric", ChannelAnalytics.workspace_id, ChannelAnalytics.channel_type, ChannelAnalytics.metric_name, ChannelAnalytics.captured_at)
