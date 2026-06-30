from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    workspace_id: UUID
    agent_id: UUID | None = None
    name: str
    category: str | None = None
    description: str | None = None
    system_prompt: str
    variables: dict = Field(default_factory=dict)
    guardrails: dict = Field(default_factory=dict)
    model_settings: dict = Field(default_factory=dict)


class PromptOut(BaseModel):
    id: UUID
    workspace_id: UUID
    agent_id: UUID | None
    name: str
    slug: str
    category: str | None
    status: str
    current_version_id: UUID | None
    description: str | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class PromptVersionCreate(BaseModel):
    system_prompt: str
    developer_prompt: str | None = None
    variables: dict = Field(default_factory=dict)
    sections: list[dict] = Field(default_factory=list)
    guardrails: dict = Field(default_factory=dict)
    dynamic_context: dict = Field(default_factory=dict)
    model_settings: dict = Field(default_factory=dict)
    release_notes: str | None = None


class PromptVersionOut(BaseModel):
    id: UUID
    prompt_id: UUID
    version_number: int
    status: str
    system_prompt: str
    developer_prompt: str | None
    variables: dict
    guardrails: dict
    model_settings: dict
    token_estimate: int
    validation_state: dict
    release_notes: str | None
    created_at: datetime


class TemplateCreate(BaseModel):
    workspace_id: UUID
    name: str
    category: str
    description: str | None = None
    template_body: str
    variables: dict = Field(default_factory=dict)
    recommended_guardrails: dict = Field(default_factory=dict)


class TemplateOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    category: str
    status: str
    description: str | None
    template_body: str
    variables: dict
    recommended_guardrails: dict
    created_at: datetime


class PlaygroundRunCreate(BaseModel):
    workspace_id: UUID
    prompt_id: UUID | None = None
    prompt_version_id: UUID | None = None
    agent_id: UUID | None = None
    channel: str = "text"
    input_payload: dict = Field(default_factory=dict)


class PlaygroundRunOut(BaseModel):
    id: UUID
    workspace_id: UUID
    prompt_id: UUID | None
    prompt_version_id: UUID | None
    agent_id: UUID | None
    channel: str
    status: str
    output_payload: dict
    execution_trace: dict
    latency_ms: int | None
    cost_usd: float | None
    created_at: datetime


class SimulationCreate(BaseModel):
    workspace_id: UUID
    prompt_id: UUID | None = None
    name: str
    scenario_type: str
    persona: dict = Field(default_factory=dict)
    conversation_script: list[dict] = Field(default_factory=list)
    assertions: list[dict] = Field(default_factory=list)


class SimulationOut(BaseModel):
    id: UUID
    workspace_id: UUID
    prompt_id: UUID | None
    name: str
    scenario_type: str
    status: str
    persona: dict
    conversation_script: list[dict]
    assertions: list[dict]
    created_at: datetime


class EvaluationCreate(BaseModel):
    workspace_id: UUID
    prompt_id: UUID | None = None
    prompt_version_id: UUID | None = None
    scenario_id: UUID | None = None
    metric_results: dict = Field(default_factory=dict)
    regression_summary: dict = Field(default_factory=dict)
    score: float | None = None


class EvaluationOut(BaseModel):
    id: UUID
    workspace_id: UUID
    prompt_id: UUID | None
    prompt_version_id: UUID | None
    scenario_id: UUID | None
    status: str
    score: float | None
    metric_results: dict
    regression_summary: dict
    created_at: datetime


class TestSuiteCreate(BaseModel):
    workspace_id: UUID
    name: str
    description: str | None = None
    schedule_config: dict = Field(default_factory=dict)
    deployment_gate: bool = False


class TestSuiteOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    description: str | None
    status: str
    deployment_gate: bool
    schedule_config: dict
    created_at: datetime


class BenchmarkCreate(BaseModel):
    workspace_id: UUID
    name: str
    baseline_prompt_version_id: UUID | None = None
    candidate_prompt_version_id: UUID | None = None
    metrics: dict = Field(default_factory=dict)


class DeploymentCreate(BaseModel):
    workspace_id: UUID
    prompt_id: UUID
    prompt_version_id: UUID
    environment: str = "staging"
    approval_state: dict = Field(default_factory=dict)
    rollout_config: dict = Field(default_factory=dict)


class CommentCreate(BaseModel):
    workspace_id: UUID
    prompt_id: UUID | None = None
    prompt_version_id: UUID | None = None
    parent_comment_id: UUID | None = None
    body: str
    mentions: list[str] = Field(default_factory=list)


class StudioSummary(BaseModel):
    prompts: int
    prompt_versions: int
    templates: int
    simulations: int
    evaluations: int
    test_suites: int
    deployments: int
    average_score: float
    ai_timeline_events: int
    recommendations: list[dict]