from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID | None = None
    name: str = Field(min_length=2, max_length=180)
    category: str | None = None
    description: str | None = None
    trigger_type: str = "manual"
    execution_mode: str = "async"
    definition: dict = Field(default_factory=dict)
    settings: dict = Field(default_factory=dict)
    canvas_state: dict = Field(default_factory=dict)


class WorkflowUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    category: str | None = None
    description: str | None = None
    trigger_type: str | None = None
    execution_mode: str | None = None
    definition: dict | None = None
    settings: dict | None = None
    canvas_state: dict | None = None
    change_summary: str | None = None


class WorkflowOut(BaseModel):
    id: UUID
    workspace_id: UUID
    project_id: UUID | None
    name: str
    slug: str
    status: str
    category: str | None
    description: str | None
    trigger_type: str
    execution_mode: str
    current_version_id: UUID | None
    definition: dict
    settings: dict
    canvas_state: dict
    published_at: datetime | None
    last_run_at: datetime | None
    run_count: int
    failure_count: int
    created_at: datetime
    updated_at: datetime


class WorkflowVersionOut(BaseModel):
    id: UUID
    workflow_id: UUID
    version_number: int
    status: str
    change_summary: str | None
    definition: dict
    canvas_state: dict
    validation_state: dict
    published_at: datetime | None
    rolled_back_from_version_id: UUID | None
    created_at: datetime


class WorkflowExecuteRequest(BaseModel):
    trigger_type: str = "manual"
    trigger_ref: str | None = None
    conversation_id: UUID | None = None
    agent_id: UUID | None = None
    execution_mode: str | None = None
    input_payload: dict = Field(default_factory=dict)
    variables: dict = Field(default_factory=dict)
    allow_pause: bool = True


class WorkflowRunOut(BaseModel):
    id: UUID
    workflow_id: UUID
    version_id: UUID | None
    conversation_id: UUID | None
    agent_id: UUID | None
    trigger_type: str
    trigger_ref: str | None
    status: str
    current_node_key: str | None
    execution_mode: str
    started_at: datetime | None
    paused_at: datetime | None
    resumed_at: datetime | None
    finished_at: datetime | None
    next_run_at: datetime | None
    attempt: int
    retry_count: int
    duration_ms: int | None
    input_payload: dict
    output_payload: dict
    variables: dict
    execution_state: dict
    error_message: str | None
    created_at: datetime


class WorkflowLogOut(BaseModel):
    id: UUID
    workflow_id: UUID | None
    workflow_run_id: UUID
    node_key: str | None
    node_type: str | None
    event_type: str
    level: str
    message: str | None
    input_snapshot: dict
    output_snapshot: dict
    latency_ms: int | None
    retry_count: int
    metadata_json: dict
    created_at: datetime


class MonitoringOut(BaseModel):
    workflows: int
    running: int
    completed: int
    failed: int
    average_duration_ms: int | None
    node_catalog_size: int
    queue_mode: str
    fault_tolerance: dict
