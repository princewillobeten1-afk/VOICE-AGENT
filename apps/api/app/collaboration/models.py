from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class AiRole(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_roles"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_ai_role_workspace_slug"),)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(80), default="custom", index=True)
    description: Mapped[str | None] = mapped_column(Text)
    responsibilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    permissions: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class AiTeam(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_teams"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_ai_team_workspace_slug"),)
    parent_team_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_teams.id", ondelete="SET NULL"), index=True)
    supervisor_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(140), index=True)
    department: Mapped[str | None] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    responsibilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    routing_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    collaboration_rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class AiTeamMember(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_team_members"
    __table_args__ = (UniqueConstraint("team_id", "agent_id", name="uq_ai_team_member_agent"),)
    team_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_teams.id", ondelete="CASCADE"), index=True)
    agent_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    role_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_roles.id", ondelete="SET NULL"), index=True)
    membership_type: Mapped[str] = mapped_column(String(60), default="member", index=True)
    responsibilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    availability_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    workload_score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class CollaborationPolicy(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "collaboration_policies"
    team_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_teams.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    policy_type: Mapped[str] = mapped_column(String(80), index=True)
    max_delegation_depth: Mapped[int] = mapped_column(Integer, default=4)
    allowed_delegations: Mapped[dict] = mapped_column(JSONB, default=dict)
    approval_requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    escalation_rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    department_restrictions: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class CollaborationSession(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "collaboration_sessions"
    team_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_teams.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    workflow_run_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id", ondelete="SET NULL"), index=True)
    supervisor_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    objective: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    priority: Mapped[str] = mapped_column(String(40), default="normal", index=True)
    shared_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    success_criteria: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    completed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class DelegationEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "delegation_events"
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("collaboration_sessions.id", ondelete="CASCADE"), index=True)
    source_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    target_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    team_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_teams.id", ondelete="SET NULL"), index=True)
    task_title: Mapped[str] = mapped_column(String(200))
    task_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    routing_reason: Mapped[str | None] = mapped_column(Text)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    depth: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(40), default="assigned", index=True)
    due_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    completed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class SharedContext(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "shared_contexts"
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("collaboration_sessions.id", ondelete="CASCADE"), index=True)
    context_type: Mapped[str] = mapped_column(String(80), index=True)
    key: Mapped[str] = mapped_column(String(160), index=True)
    value_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    visibility: Mapped[str] = mapped_column(String(60), default="team", index=True)
    source_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)


class SharedMemoryReference(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "shared_memory_refs"
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("collaboration_sessions.id", ondelete="CASCADE"), index=True)
    memory_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="SET NULL"), index=True)
    reference_type: Mapped[str] = mapped_column(String(80), default="fact", index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    permission_summary: Mapped[dict] = mapped_column(JSONB, default=dict)


class CollaborationMessage(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "collaboration_messages"
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("collaboration_sessions.id", ondelete="CASCADE"), index=True)
    sender_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    recipient_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    message_type: Mapped[str] = mapped_column(String(80), default="direct", index=True)
    subject: Mapped[str | None] = mapped_column(String(180))
    body: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="sent", index=True)


class CollaborationLog(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "collaboration_logs"
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("collaboration_sessions.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    actor_agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    level: Mapped[str] = mapped_column(String(40), default="info", index=True)
    message: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class CollaborationMetric(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "collaboration_metrics"
    team_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_teams.id", ondelete="CASCADE"), index=True)
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 3))
    unit: Mapped[str] = mapped_column(String(32), default="count")
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_ai_teams_workspace_status", AiTeam.workspace_id, AiTeam.status, AiTeam.department)
Index("ix_ai_team_members_team_status", AiTeamMember.team_id, AiTeamMember.status, AiTeamMember.membership_type)
Index("ix_collab_sessions_workspace_status", CollaborationSession.workspace_id, CollaborationSession.status, CollaborationSession.started_at)
Index("ix_delegation_events_session_status", DelegationEvent.session_id, DelegationEvent.status, DelegationEvent.created_at)
Index("ix_shared_context_session_key", SharedContext.session_id, SharedContext.context_type, SharedContext.key)
Index("ix_collab_messages_session_type", CollaborationMessage.session_id, CollaborationMessage.message_type, CollaborationMessage.created_at)
Index("ix_collab_logs_session_event", CollaborationLog.session_id, CollaborationLog.event_type, CollaborationLog.created_at)
Index("ix_collab_metrics_team_time", CollaborationMetric.team_id, CollaborationMetric.metric_name, CollaborationMetric.captured_at)
