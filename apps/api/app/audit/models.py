from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import IdMixin, OrganizationScopedMixin, TimestampMixin, WorkspaceScopedMixin


class SecurityEvent(IdMixin, TimestampMixin, Base):
    __tablename__ = "security_events"
    organization_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(120), index=True)
    risk_level: Mapped[str] = mapped_column(String(40), default="low")
    ip_address: Mapped[str | None] = mapped_column(INET)
    user_agent: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DomainEventRecord(IdMixin, TimestampMixin, Base):
    __tablename__ = "domain_event_records"
    organization_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    workspace_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="SET NULL"), index=True)
    actor_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    aggregate_type: Mapped[str] = mapped_column(String(80), index=True)
    aggregate_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True)
    occurred_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_security_events_org_type_created", SecurityEvent.organization_id, SecurityEvent.event_type, SecurityEvent.created_at)
Index("ix_domain_events_aggregate", DomainEventRecord.aggregate_type, DomainEventRecord.aggregate_id, DomainEventRecord.occurred_at)