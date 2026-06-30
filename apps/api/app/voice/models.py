from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class VoiceProviderSetting(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voice_provider_settings"
    __table_args__ = (UniqueConstraint("workspace_id", "provider_type", "provider", "name", name="uq_voice_provider_setting_name"),)
    name: Mapped[str] = mapped_column(String(160))
    provider_type: Mapped[str] = mapped_column(String(40), index=True)
    provider: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    health_state: Mapped[dict] = mapped_column(JSONB, default=dict)


class VoiceConfiguration(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voice_configurations"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_voice_configuration_workspace_name"),)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    language: Mapped[str] = mapped_column(String(32), default="en")
    accent: Mapped[str | None] = mapped_column(String(80))
    stt_provider: Mapped[str] = mapped_column(String(80), default="openai")
    stt_model: Mapped[str | None] = mapped_column(String(120))
    tts_provider: Mapped[str] = mapped_column(String(80), default="openai")
    tts_model: Mapped[str | None] = mapped_column(String(120))
    voice_id: Mapped[str | None] = mapped_column(String(180))
    speaking_speed: Mapped[str | None] = mapped_column(String(32))
    stability: Mapped[str | None] = mapped_column(String(32))
    emotion: Mapped[str | None] = mapped_column(String(80))
    streaming_mode: Mapped[str] = mapped_column(String(40), default="full_duplex")
    audio_format: Mapped[dict] = mapped_column(JSONB, default=dict)
    vad_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    interruption_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_budget: Mapped[dict] = mapped_column(JSONB, default=dict)
    fallback_chain: Mapped[list[str]] = mapped_column(JSONB, default=list)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class VoiceSession(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voice_sessions"
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    voice_configuration_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_configurations.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    channel: Mapped[str] = mapped_column(String(40), default="browser", index=True)
    direction: Mapped[str] = mapped_column(String(40), default="inbound")
    status: Mapped[str] = mapped_column(String(40), default="initializing", index=True)
    current_speaker: Mapped[str | None] = mapped_column(String(40))
    active_response_id: Mapped[str | None] = mapped_column(String(120))
    interrupt_count: Mapped[int] = mapped_column(Integer, default=0)
    pending_tool_calls: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    context_snapshot: Mapped[dict] = mapped_column(JSONB, default=dict)
    memory_updates: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    conversation_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    transport_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    last_activity_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    timeout_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    ended_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    termination_reason: Mapped[str | None] = mapped_column(Text)


class VoiceSessionMetric(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voice_session_metrics"
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_sessions.id", ondelete="CASCADE"), index=True)
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(12, 3))
    unit: Mapped[str] = mapped_column(String(32), default="ms")
    stage: Mapped[str | None] = mapped_column(String(40), index=True)
    provider: Mapped[str | None] = mapped_column(String(80), index=True)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class VoiceAudioMetadata(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voice_audio_metadata"
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_sessions.id", ondelete="CASCADE"), index=True)
    direction: Mapped[str] = mapped_column(String(40), index=True)
    codec: Mapped[str] = mapped_column(String(40), default="pcm16")
    sample_rate_hz: Mapped[int] = mapped_column(Integer, default=16000)
    channels: Mapped[int] = mapped_column(Integer, default=1)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    byte_count: Mapped[int] = mapped_column(Integer, default=0)
    storage_policy: Mapped[str] = mapped_column(String(40), default="metadata_only")
    storage_object_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    quality_score: Mapped[str | None] = mapped_column(String(40))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class VoiceStreamEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "voice_stream_events"
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_sessions.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    sequence_number: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(40), default="client", index=True)
    stage: Mapped[str | None] = mapped_column(String(40), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    provider: Mapped[str | None] = mapped_column(String(80))
    trace_id: Mapped[str | None] = mapped_column(String(120), index=True)


Index("ix_voice_provider_settings_workspace_type", VoiceProviderSetting.workspace_id, VoiceProviderSetting.provider_type, VoiceProviderSetting.status, VoiceProviderSetting.priority)
Index("ix_voice_configurations_workspace_status", VoiceConfiguration.workspace_id, VoiceConfiguration.status, VoiceConfiguration.deleted_at)
Index("ix_voice_sessions_workspace_status", VoiceSession.workspace_id, VoiceSession.status, VoiceSession.last_activity_at)
Index("ix_voice_sessions_agent_status", VoiceSession.agent_id, VoiceSession.status, VoiceSession.started_at)
Index("ix_voice_session_metrics_session_name", VoiceSessionMetric.session_id, VoiceSessionMetric.metric_name, VoiceSessionMetric.captured_at)
Index("ix_voice_stream_events_session_sequence", VoiceStreamEvent.session_id, VoiceStreamEvent.sequence_number)