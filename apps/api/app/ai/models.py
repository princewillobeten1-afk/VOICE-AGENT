from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class Agent(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "agents"
    __table_args__ = (UniqueConstraint("project_id", "slug", name="uq_agent_project_slug"),)
    project_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120))
    display_name: Mapped[str | None] = mapped_column(String(180))
    avatar_url: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str | None] = mapped_column(String(160), index=True)
    department: Mapped[str | None] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    lifecycle_stage: Mapped[str] = mapped_column(String(40), default="builder")
    current_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True))
    template_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_templates.id", ondelete="SET NULL"), index=True)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    last_published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    archived_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class AgentVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "agent_versions"
    __table_args__ = (UniqueConstraint("agent_id", "version_number", name="uq_agent_version_number"),)
    agent_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    change_summary: Mapped[str | None] = mapped_column(Text)
    instructions: Mapped[str | None] = mapped_column(Text)
    personality_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    voice_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    knowledge_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    memory_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    channel_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    collaboration_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    model_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    tool_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    workflow_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    validation_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class AgentConfiguration(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "agent_configurations"
    agent_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    active_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_versions.id", ondelete="SET NULL"), index=True)
    builder_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    readiness: Mapped[dict] = mapped_column(JSONB, default=dict)
    playground_state: Mapped[dict] = mapped_column(JSONB, default=dict)


class AgentTemplate(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "agent_templates"
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(180))
    category: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(160))
    department: Mapped[str | None] = mapped_column(String(120))
    default_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    recommended_tools: Mapped[list[str]] = mapped_column(JSONB, default=list)
    recommended_channels: Mapped[list[str]] = mapped_column(JSONB, default=list)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class AgentDraft(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "agent_drafts"
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    step: Mapped[str] = mapped_column(String(80), default="identity")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class AgentPublishingHistory(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "agent_publishing_history"
    agent_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_versions.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    from_status: Mapped[str | None] = mapped_column(String(40))
    to_status: Mapped[str | None] = mapped_column(String(40))
    change_summary: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Voice(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voices"
    name: Mapped[str] = mapped_column(String(160))
    provider: Mapped[str] = mapped_column(String(60))
    provider_voice_id: Mapped[str | None] = mapped_column(String(180))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)


class Prompt(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "prompts"
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    purpose: Mapped[str] = mapped_column(String(80))
    body: Mapped[str] = mapped_column(Text)
    variables: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_agents_project_status", Agent.project_id, Agent.status, Agent.deleted_at)
Index("ix_agents_workspace_status", Agent.workspace_id, Agent.status, Agent.deleted_at)
Index("ix_agents_workspace_category", Agent.workspace_id, Agent.category, Agent.deleted_at)
Index("ix_agent_versions_agent_created", AgentVersion.agent_id, AgentVersion.created_at)
Index("ix_agent_versions_agent_status", AgentVersion.agent_id, AgentVersion.status)
Index("ix_agent_configurations_agent", AgentConfiguration.agent_id, AgentConfiguration.active_version_id)
Index("ix_agent_drafts_agent_status", AgentDraft.agent_id, AgentDraft.status)
Index("ix_agent_publishing_history_agent_created", AgentPublishingHistory.agent_id, AgentPublishingHistory.created_at)
Index("ix_voices_workspace_provider", Voice.workspace_id, Voice.provider, Voice.deleted_at)