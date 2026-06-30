from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class Conversation(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversations"
    project_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    agent_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_versions.id", ondelete="SET NULL"), index=True)
    channel: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), default="open")
    subject: Mapped[str | None] = mapped_column(String(300))
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Message(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "messages"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    sender_type: Mapped[str] = mapped_column(String(40))
    sender_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True))
    role: Mapped[str] = mapped_column(String(40))
    content: Mapped[str | None] = mapped_column(Text)
    sequence_number: Mapped[int] = mapped_column(Integer)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Call(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "calls"
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    provider: Mapped[str | None] = mapped_column(String(60))
    provider_call_id: Mapped[str | None] = mapped_column(String(180), index=True)
    direction: Mapped[str] = mapped_column(String(20))
    from_number: Mapped[str | None] = mapped_column(String(40))
    to_number: Mapped[str | None] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), default="queued")
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    recording_file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    cost_cents: Mapped[int | None] = mapped_column(BigInteger)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class CallEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "call_events"
    call_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("calls.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(80), index=True)
    occurred_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_conversations_project_status", Conversation.project_id, Conversation.status, Conversation.started_at)
Index("ix_messages_conversation_sequence", Message.conversation_id, Message.sequence_number)
Index("ix_calls_workspace_status", Call.workspace_id, Call.status, Call.started_at)
Index("ix_call_events_call_occurred", CallEvent.call_id, CallEvent.occurred_at)

class ConversationSession(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversation_sessions"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    voice_session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_sessions.id", ondelete="SET NULL"), index=True)
    channel: Mapped[str] = mapped_column(String(40), index=True)
    adapter: Mapped[str] = mapped_column(String(80), default="universal")
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    state_version: Mapped[int] = mapped_column(Integer, default=1)
    current_speaker: Mapped[str | None] = mapped_column(String(40))
    active_turn_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    active_intent: Mapped[str | None] = mapped_column(String(120), index=True)
    pending_questions: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    tool_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    workflow_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    memory_refs: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    session_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    recovery_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    last_activity_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    paused_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    resumed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    ended_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    end_reason: Mapped[str | None] = mapped_column(Text)


class ConversationTurn(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversation_turns"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id", ondelete="SET NULL"), index=True)
    message_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="SET NULL"), index=True)
    sequence_number: Mapped[int] = mapped_column(Integer)
    speaker_type: Mapped[str] = mapped_column(String(40), index=True)
    turn_type: Mapped[str] = mapped_column(String(60), default="message", index=True)
    status: Mapped[str] = mapped_column(String(40), default="completed", index=True)
    content: Mapped[str | None] = mapped_column(Text)
    intent: Mapped[dict] = mapped_column(JSONB, default=dict)
    entities: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    context_delta: Mapped[dict] = mapped_column(JSONB, default=dict)
    response_plan: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    interrupted: Mapped[bool] = mapped_column(default=False)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ConversationGoal(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversation_goals"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    goal_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    success_criteria: Mapped[dict] = mapped_column(JSONB, default=dict)
    progress: Mapped[dict] = mapped_column(JSONB, default=dict)
    completed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class ConversationContextSnapshot(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversation_context_snapshots"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id", ondelete="SET NULL"), index=True)
    snapshot_type: Mapped[str] = mapped_column(String(80), default="turn", index=True)
    token_budget: Mapped[int | None] = mapped_column(Integer)
    sources: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    prioritized_context: Mapped[dict] = mapped_column(JSONB, default=dict)
    omitted_context: Mapped[dict] = mapped_column(JSONB, default=dict)
    model_limits: Mapped[dict] = mapped_column(JSONB, default=dict)


class ConversationEngineEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversation_engine_events"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id", ondelete="SET NULL"), index=True)
    turn_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversation_turns.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    stage: Mapped[str | None] = mapped_column(String(80), index=True)
    sequence_number: Mapped[int] = mapped_column(Integer, default=0)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    trace_id: Mapped[str | None] = mapped_column(String(120), index=True)


class ConversationAnalytics(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "conversation_analytics"
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id", ondelete="SET NULL"), index=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    turn_count: Mapped[int] = mapped_column(Integer, default=0)
    average_response_time_ms: Mapped[int | None] = mapped_column(Integer)
    completion_status: Mapped[str] = mapped_column(String(40), default="unknown", index=True)
    escalation_status: Mapped[str] = mapped_column(String(40), default="none", index=True)
    goal_achievement: Mapped[dict] = mapped_column(JSONB, default=dict)
    sentiment: Mapped[dict] = mapped_column(JSONB, default=dict)
    satisfaction: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_conversation_sessions_conversation_status", ConversationSession.conversation_id, ConversationSession.status, ConversationSession.last_activity_at)
Index("ix_conversation_turns_conversation_sequence", ConversationTurn.conversation_id, ConversationTurn.sequence_number)
Index("ix_conversation_goals_conversation_status", ConversationGoal.conversation_id, ConversationGoal.status, ConversationGoal.priority)
Index("ix_conversation_context_conversation_created", ConversationContextSnapshot.conversation_id, ConversationContextSnapshot.created_at)
Index("ix_conversation_engine_events_conversation_sequence", ConversationEngineEvent.conversation_id, ConversationEngineEvent.sequence_number)
Index("ix_conversation_analytics_conversation", ConversationAnalytics.conversation_id, ConversationAnalytics.completion_status)