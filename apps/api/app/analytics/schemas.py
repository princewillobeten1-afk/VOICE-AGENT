from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ExecutiveSummaryOut(BaseModel):
    active_ai_employees: int
    active_conversations: int
    active_voice_sessions: int
    running_workflows: int
    tool_executions: int
    knowledge_queries: int
    memory_usage: int
    collaboration_sessions: int
    success_rate: float
    error_rate: float
    customer_satisfaction: str
    average_response_time_ms: int | None
    ai_cost: float
    system_health: int


class AlertCreate(BaseModel):
    workspace_id: UUID
    name: str
    alert_type: str
    severity: str = "warning"
    condition: dict = Field(default_factory=dict)
    channels: list[str] = Field(default_factory=list)
    metadata_json: dict = Field(default_factory=dict)


class AlertOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    alert_type: str
    severity: str
    status: str
    condition: dict
    channels: list[str]
    last_triggered_at: datetime | None
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


class HealthCreate(BaseModel):
    workspace_id: UUID
    component: str
    status: str
    score: int = 100
    checks: dict = Field(default_factory=dict)
    incidents: list[dict] = Field(default_factory=list)


class HealthOut(BaseModel):
    id: UUID
    workspace_id: UUID
    component: str
    status: str
    score: int
    checks: dict
    incidents: list[dict]
    measured_at: datetime
    created_at: datetime


class CostCreate(BaseModel):
    workspace_id: UUID
    cost_type: str
    provider: str | None = None
    entity_type: str | None = None
    entity_id: UUID | None = None
    amount: float
    currency: str = "USD"
    quantity: float | None = None
    unit: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class CostOut(BaseModel):
    id: UUID
    workspace_id: UUID
    cost_type: str
    provider: str | None
    entity_type: str | None
    entity_id: UUID | None
    amount: float
    currency: str
    quantity: float | None
    unit: str | None
    occurred_at: datetime
    metadata_json: dict


class EvaluationCreate(BaseModel):
    workspace_id: UUID
    agent_id: UUID | None = None
    conversation_id: UUID | None = None
    evaluation_type: str
    score: float | None = None
    status: str = "pending"
    evaluator: str = "framework"
    criteria: dict = Field(default_factory=dict)
    result: dict = Field(default_factory=dict)


class EvaluationOut(BaseModel):
    id: UUID
    workspace_id: UUID
    agent_id: UUID | None
    conversation_id: UUID | None
    evaluation_type: str
    score: float | None
    status: str
    evaluator: str
    criteria: dict
    result: dict
    reviewed_by_user_id: UUID | None
    evaluated_at: datetime | None
    created_at: datetime
