from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class VoiceConfigurationBase(BaseModel):
    workspace_id: UUID
    agent_id: UUID | None = None
    name: str = Field(min_length=2, max_length=180)
    status: str = "draft"
    language: str = "en"
    accent: str | None = None
    stt_provider: str = "cartesia"
    stt_model: str | None = "ink"
    tts_provider: str = "cartesia"
    tts_model: str | None = "sonic-2"
    voice_id: str | None = None
    speaking_speed: str | None = "1.0"
    stability: str | None = None
    emotion: str | None = None
    streaming_mode: str = "full_duplex"
    audio_format: dict = Field(default_factory=dict)
    vad_config: dict = Field(default_factory=dict)
    interruption_config: dict = Field(default_factory=dict)
    latency_budget: dict = Field(default_factory=dict)
    fallback_chain: list[str] = Field(default_factory=list)
    metadata_json: dict = Field(default_factory=dict)


class VoiceConfigurationCreate(VoiceConfigurationBase):
    pass


class VoiceConfigurationUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    language: str | None = None
    accent: str | None = None
    stt_provider: str | None = None
    stt_model: str | None = None
    tts_provider: str | None = None
    tts_model: str | None = None
    voice_id: str | None = None
    speaking_speed: str | None = None
    stability: str | None = None
    emotion: str | None = None
    streaming_mode: str | None = None
    audio_format: dict | None = None
    vad_config: dict | None = None
    interruption_config: dict | None = None
    latency_budget: dict | None = None
    fallback_chain: list[str] | None = None
    metadata_json: dict | None = None


class VoiceConfigurationOut(VoiceConfigurationBase):
    id: UUID
    organization_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class VoiceProviderSettingCreate(BaseModel):
    workspace_id: UUID
    name: str
    provider_type: str
    provider: str
    status: str = "disabled"
    priority: int = 100
    secret_ref: str | None = None
    config: dict = Field(default_factory=dict)
    capabilities: list[str] = Field(default_factory=list)
    health_state: dict = Field(default_factory=dict)


class VoiceProviderSettingOut(VoiceProviderSettingCreate):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class VoiceSessionCreate(BaseModel):
    workspace_id: UUID
    agent_id: UUID | None = None
    voice_configuration_id: UUID | None = None
    channel: str = "browser"
    direction: str = "inbound"
    transport_mode: str = "websocket"
    connection_id: str | None = None
    timeout_minutes: int = Field(default=45, ge=1, le=360)
    context_snapshot: dict = Field(default_factory=dict)


class VoiceSessionOut(BaseModel):
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    agent_id: UUID | None = None
    voice_configuration_id: UUID | None = None
    user_id: UUID | None = None
    channel: str
    direction: str
    status: str
    current_speaker: str | None = None
    active_response_id: str | None = None
    interrupt_count: int
    pending_tool_calls: list[dict]
    context_snapshot: dict
    memory_updates: list[dict]
    conversation_state: dict
    transport_state: dict
    started_at: datetime | None = None
    last_activity_at: datetime | None = None
    timeout_at: datetime | None = None
    ended_at: datetime | None = None
    termination_reason: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class VoiceStreamEventCreate(BaseModel):
    event_type: str
    source: str = "client"
    stage: str | None = None
    payload: dict = Field(default_factory=dict)
    latency_ms: int | None = None
    provider: str | None = None


class VoiceStreamEventOut(BaseModel):
    id: UUID
    session_id: UUID
    event_type: str
    sequence_number: int
    source: str
    stage: str | None = None
    payload: dict
    latency_ms: int | None = None
    provider: str | None = None
    trace_id: str | None = None
    created_at: datetime | None = None


class VoiceStreamEventBatch(BaseModel):
    events: list[VoiceStreamEventOut]


class VoiceSessionMetricOut(BaseModel):
    id: UUID
    session_id: UUID
    metric_name: str
    metric_value: float
    unit: str
    stage: str | None = None
    provider: str | None = None
    captured_at: datetime | None = None
    metadata_json: dict


class VoiceSessionDetail(BaseModel):
    session: VoiceSessionOut
    events: list[VoiceStreamEventOut]
    metrics: list[VoiceSessionMetricOut]


class VoiceTerminateRequest(BaseModel):
    reason: str = "completed"


class VoiceTestRunRequest(BaseModel):
    workspace_id: UUID
    voice_configuration_id: UUID | None = None
    text: str = "Hello, this is a VoiceSense voice engine test."


class VoiceTestRunResult(BaseModel):
    status: str
    pipeline: list[str]
    transcript_preview: str
    tts_payload_ref: str | None
    estimated_latency_ms: int
    provider_plan: dict
    safety_notes: list[str]
