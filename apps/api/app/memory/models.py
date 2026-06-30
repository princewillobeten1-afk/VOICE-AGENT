from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class MemoryCategory(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_categories"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_memory_category_workspace_slug"),)
    name: Mapped[str] = mapped_column(String(120))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(String(40))
    retention_days: Mapped[int | None] = mapped_column(Integer)
    default_privacy_level: Mapped[str] = mapped_column(String(40), default="internal")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class MemoryPolicy(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_policies"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_memory_policy_workspace_name"),)
    name: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    scope: Mapped[str] = mapped_column(String(40), default="workspace", index=True)
    memory_types: Mapped[list[str]] = mapped_column(JSONB, default=list)
    retention_days: Mapped[int | None] = mapped_column(Integer)
    expiration_rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    auto_cleanup_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    max_memory_size: Mapped[int | None] = mapped_column(Integer)
    privacy_rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Memory(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memories"
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    category_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("memory_categories.id", ondelete="SET NULL"), index=True)
    policy_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("memory_policies.id", ondelete="SET NULL"), index=True)
    memory_type: Mapped[str] = mapped_column(String(60), index=True)
    title: Mapped[str] = mapped_column(String(240))
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    privacy_level: Mapped[str] = mapped_column(String(40), default="internal", index=True)
    visibility: Mapped[str] = mapped_column(String(40), default="workspace", index=True)
    source_type: Mapped[str] = mapped_column(String(80), default="manual", index=True)
    source_ref: Mapped[str | None] = mapped_column(String(180), index=True)
    importance_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    confidence_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    recency_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    retrieval_count: Mapped[int] = mapped_column(Integer, default=0)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    encrypted: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    facts: Mapped[dict] = mapped_column(JSONB, default=dict)
    evaluation: Mapped[dict] = mapped_column(JSONB, default=dict)
    index_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    archived_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    forgotten_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class MemoryVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_versions"
    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(240))
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    change_type: Mapped[str] = mapped_column(String(60), default="created", index=True)
    change_summary: Mapped[str | None] = mapped_column(Text)
    evaluation: Mapped[dict] = mapped_column(JSONB, default=dict)


class MemoryLink(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_links"
    source_memory_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    target_memory_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    link_type: Mapped[str] = mapped_column(String(60), default="related", index=True)
    strength: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class MemoryAccess(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_access"
    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    principal_type: Mapped[str] = mapped_column(String(40), index=True)
    principal_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    permission: Mapped[str] = mapped_column(String(40), default="read", index=True)
    granted_by_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class MemoryEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_events"
    memory_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    actor_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    trace_id: Mapped[str | None] = mapped_column(String(120), index=True)


class MemoryStatistic(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "memory_statistics"
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 3))
    unit: Mapped[str] = mapped_column(String(32), default="count")
    scope: Mapped[str] = mapped_column(String(40), default="workspace", index=True)
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_memories_workspace_type_status", Memory.workspace_id, Memory.memory_type, Memory.status, Memory.updated_at)
Index("ix_memories_workspace_privacy", Memory.workspace_id, Memory.privacy_level, Memory.visibility, Memory.status)
Index("ix_memories_agent_status", Memory.agent_id, Memory.status, Memory.updated_at)
Index("ix_memories_user_status", Memory.user_id, Memory.status, Memory.updated_at)
Index("ix_memories_category_status", Memory.category_id, Memory.status, Memory.updated_at)
Index("ix_memories_pinned_importance", Memory.workspace_id, Memory.pinned, Memory.importance_score)
Index("ix_memory_versions_memory_version", MemoryVersion.memory_id, MemoryVersion.version_number)
Index("ix_memory_links_source_target", MemoryLink.source_memory_id, MemoryLink.target_memory_id)
Index("ix_memory_access_principal", MemoryAccess.principal_type, MemoryAccess.principal_id, MemoryAccess.permission)
Index("ix_memory_events_memory_type", MemoryEvent.memory_id, MemoryEvent.event_type, MemoryEvent.created_at)
Index("ix_memory_statistics_metric_time", MemoryStatistic.workspace_id, MemoryStatistic.metric_name, MemoryStatistic.captured_at)