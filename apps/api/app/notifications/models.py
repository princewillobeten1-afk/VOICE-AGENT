from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class PlatformEvent(IdMixin, TimestampMixin, Base):
    __tablename__ = "domain_event_records"
    organization_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    workspace_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="SET NULL"), index=True)
    actor_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    aggregate_type: Mapped[str] = mapped_column(String(80))
    aggregate_id: Mapped[str] = mapped_column(UUID(as_uuid=True))
    occurred_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    event_version: Mapped[int] = mapped_column(Integer, default=1)
    source: Mapped[str] = mapped_column(String(80), default="platform")
    correlation_id: Mapped[str | None] = mapped_column(String(120), index=True)
    causation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(160), unique=True)
    status: Mapped[str] = mapped_column(String(40), default="published", index=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    processed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class EventSubscriber(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "event_subscribers"
    name: Mapped[str] = mapped_column(String(160), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    event_types: Mapped[list[str]] = mapped_column(JSONB, default=list)
    handler_ref: Mapped[str] = mapped_column(String(240))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class EventLog(IdMixin, TimestampMixin, Base):
    __tablename__ = "event_logs"
    event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("domain_event_records.id", ondelete="CASCADE"), index=True)
    subscriber_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("event_subscribers.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Notification(IdMixin, TimestampMixin, SoftDeleteMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "notifications"
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    event_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("domain_event_records.id", ondelete="SET NULL"), index=True)
    type: Mapped[str] = mapped_column(String(80), index=True)
    category: Mapped[str] = mapped_column(String(80), default="system", index=True)
    title: Mapped[str] = mapped_column(String(240))
    body: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(40), default="info", index=True)
    status: Mapped[str] = mapped_column(String(40), default="unread", index=True)
    priority: Mapped[str] = mapped_column(String(40), default="normal")
    read_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    archived_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    action_url: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class NotificationPreference(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "notification_preferences"
    __table_args__ = (UniqueConstraint("organization_id", "user_id", name="uq_notification_preference_user_org"),)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    channel: Mapped[str] = mapped_column(String(40), default="all")
    type: Mapped[str] = mapped_column(String(80), default="all")
    enabled: Mapped[bool] = mapped_column(default=True)
    email_enabled: Mapped[bool] = mapped_column(default=False)
    in_app_enabled: Mapped[bool] = mapped_column(default=True)
    sms_enabled: Mapped[bool] = mapped_column(default=False)
    push_enabled: Mapped[bool] = mapped_column(default=False)
    webhook_enabled: Mapped[bool] = mapped_column(default=False)
    frequency: Mapped[str] = mapped_column(String(40), default="instant")
    quiet_hours: Mapped[dict] = mapped_column(JSONB, default=dict)
    category_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    team_notifications: Mapped[bool] = mapped_column(default=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class NotificationChannel(IdMixin, TimestampMixin, SoftDeleteMixin, OrganizationScopedMixin, Base):
    __tablename__ = "notification_channels"
    channel: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    provider: Mapped[str | None] = mapped_column(String(80))
    config_ref: Mapped[str | None] = mapped_column(Text)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class NotificationTemplate(IdMixin, TimestampMixin, SoftDeleteMixin, OrganizationScopedMixin, Base):
    __tablename__ = "notification_templates"
    __table_args__ = (UniqueConstraint("organization_id", "event_type", "channel", name="uq_notification_template_event_channel"),)
    event_type: Mapped[str] = mapped_column(String(120), index=True)
    channel: Mapped[str] = mapped_column(String(40), default="in_app")
    category: Mapped[str] = mapped_column(String(80), default="system")
    severity: Mapped[str] = mapped_column(String(40), default="info")
    title_template: Mapped[str] = mapped_column(String(240))
    body_template: Mapped[str | None] = mapped_column(Text)
    action_url_template: Mapped[str | None] = mapped_column(Text)
    variables: Mapped[list[str]] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class DeliveryAttempt(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "delivery_attempts"
    notification_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("notifications.id", ondelete="CASCADE"), index=True)
    event_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("domain_event_records.id", ondelete="CASCADE"), index=True)
    channel: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    provider: Mapped[str | None] = mapped_column(String(80))
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    next_retry_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    failed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_notifications_user_read", Notification.user_id, Notification.read_at, Notification.created_at)
Index("ix_notifications_org_user_status", Notification.organization_id, Notification.user_id, Notification.status, Notification.created_at)
Index("ix_notifications_org_category", Notification.organization_id, Notification.category, Notification.created_at)
Index("ix_events_name_time", PlatformEvent.name, PlatformEvent.occurred_at)
Index("ix_events_org_status_time", PlatformEvent.organization_id, PlatformEvent.status, PlatformEvent.occurred_at)
Index("ix_event_logs_event_status", EventLog.event_id, EventLog.status)
Index("ix_delivery_attempts_status_retry", DeliveryAttempt.status, DeliveryAttempt.next_retry_at)