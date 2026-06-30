from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID
    agent_id: UUID | None = None
    agent_version_id: UUID | None = None
    channel: str = "chat"
    subject: str | None = None
    customer_ref: str | None = None
    external_thread_id: str | None = None
    goals: list[dict] = Field(default_factory=list)
    metadata_json: dict = Field(default_factory=dict)


class ConversationOut(BaseModel):
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    project_id: UUID
    agent_id: UUID | None = None
    agent_version_id: UUID | None = None
    channel: str
    status: str
    lifecycle_stage: str
    priority: str
    current_topic: str | None = None
    active_intent: str | None = None
    subject: str | None = None
    customer_ref: str | None = None
    external_thread_id: str | None = None
    handoff_status: str
    summary: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    metadata_json: dict
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ConversationSessionCreate(BaseModel):
    channel: str = "chat"
    adapter: str = "universal"
    voice_session_id: UUID | None = None
    expires_in_minutes: int = Field(default=1440, ge=1, le=43200)
    session_state: dict = Field(default_factory=dict)


class ConversationSessionOut(BaseModel):
    id: UUID
    conversation_id: UUID
    workspace_id: UUID
    channel: str
    adapter: str
    status: str
    state_version: int
    current_speaker: str | None = None
    active_turn_id: UUID | None = None
    active_intent: str | None = None
    pending_questions: list[dict]
    tool_state: dict
    workflow_state: dict
    memory_refs: list[dict]
    session_state: dict
    recovery_state: dict
    started_at: datetime | None = None
    last_activity_at: datetime | None = None
    paused_at: datetime | None = None
    resumed_at: datetime | None = None
    expires_at: datetime | None = None
    ended_at: datetime | None = None
    end_reason: str | None = None


class TurnCreate(BaseModel):
    session_id: UUID | None = None
    speaker_type: str = "user"
    turn_type: str = "message"
    content: str | None = None
    intent: dict = Field(default_factory=dict)
    entities: list[dict] = Field(default_factory=list)
    context_delta: dict = Field(default_factory=dict)
    response_plan: dict = Field(default_factory=dict)
    latency_ms: int | None = None
    interrupted: bool = False
    metadata_json: dict = Field(default_factory=dict)


class ConversationTurnOut(BaseModel):
    id: UUID
    conversation_id: UUID
    session_id: UUID | None = None
    message_id: UUID | None = None
    sequence_number: int
    speaker_type: str
    turn_type: str
    status: str
    content: str | None = None
    intent: dict
    entities: list[dict]
    context_delta: dict
    response_plan: dict
    latency_ms: int | None = None
    interrupted: bool
    metadata_json: dict
    created_at: datetime | None = None


class GoalCreate(BaseModel):
    name: str
    goal_type: str
    priority: int = 100
    success_criteria: dict = Field(default_factory=dict)
    progress: dict = Field(default_factory=dict)


class ConversationGoalOut(BaseModel):
    id: UUID
    conversation_id: UUID
    name: str
    goal_type: str
    status: str
    priority: int
    success_criteria: dict
    progress: dict
    completed_at: datetime | None = None


class ContextSnapshotCreate(BaseModel):
    session_id: UUID | None = None
    snapshot_type: str = "turn"
    token_budget: int | None = None
    sources: list[dict] = Field(default_factory=list)
    prioritized_context: dict = Field(default_factory=dict)
    omitted_context: dict = Field(default_factory=dict)
    model_limits: dict = Field(default_factory=dict)


class ContextSnapshotOut(ContextSnapshotCreate):
    id: UUID
    conversation_id: UUID
    created_at: datetime | None = None


class HandoffRequest(BaseModel):
    reason: str
    summary: str | None = None
    priority: str = "normal"


class ConversationEventOut(BaseModel):
    id: UUID
    conversation_id: UUID
    session_id: UUID | None = None
    turn_id: UUID | None = None
    event_type: str
    stage: str | None = None
    sequence_number: int
    payload: dict
    latency_ms: int | None = None
    trace_id: str | None = None
    created_at: datetime | None = None


class ConversationAnalyticsOut(BaseModel):
    id: UUID
    conversation_id: UUID
    session_id: UUID | None = None
    duration_seconds: int
    turn_count: int
    average_response_time_ms: int | None = None
    completion_status: str
    escalation_status: str
    goal_achievement: dict
    sentiment: dict
    satisfaction: dict
    metadata_json: dict


class ConversationDetail(BaseModel):
    conversation: ConversationOut
    sessions: list[ConversationSessionOut]
    turns: list[ConversationTurnOut]
    goals: list[ConversationGoalOut]
    context_snapshots: list[ContextSnapshotOut]
    events: list[ConversationEventOut]
    analytics: ConversationAnalyticsOut | None = None


class EndSessionRequest(BaseModel):
    reason: str = "completed"


class PauseSessionRequest(BaseModel):
    reason: str = "paused_by_user"