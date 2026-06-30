from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID
    name: str = Field(min_length=1, max_length=180)
    role: str = Field(min_length=1, max_length=160)
    department: str | None = Field(default=None, max_length=120)
    description: str | None = None
    template_id: UUID | None = None
    category: str | None = Field(default=None, max_length=80)


class AgentUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=180)
    display_name: str | None = Field(default=None, max_length=180)
    avatar_url: str | None = None
    role: str | None = Field(default=None, max_length=160)
    department: str | None = Field(default=None, max_length=120)
    description: str | None = None
    category: str | None = Field(default=None, max_length=80)
    settings: dict | None = None


class AgentVersionUpsert(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    instructions: str | None = None
    change_summary: str | None = None
    personality_config: dict = Field(default_factory=dict)
    voice_config: dict = Field(default_factory=dict)
    knowledge_config: dict = Field(default_factory=dict)
    memory_config: dict = Field(default_factory=dict)
    channel_config: dict = Field(default_factory=dict)
    collaboration_config: dict = Field(default_factory=dict)
    ai_model_config: dict = Field(default_factory=dict, alias="model_config")
    tool_config: dict = Field(default_factory=dict)
    workflow_config: dict = Field(default_factory=dict)
    validation_state: dict = Field(default_factory=dict)


class AgentOut(BaseModel):
    id: UUID
    workspace_id: UUID
    project_id: UUID
    name: str
    slug: str
    display_name: str | None = None
    avatar_url: str | None = None
    role: str | None = None
    department: str | None = None
    description: str | None = None
    category: str | None = None
    status: str
    lifecycle_stage: str
    current_version_id: UUID | None = None
    template_id: UUID | None = None
    last_published_at: datetime | None = None
    archived_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AgentVersionOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: UUID
    agent_id: UUID
    version_number: int
    status: str
    change_summary: str | None = None
    instructions: str | None = None
    personality_config: dict
    voice_config: dict
    knowledge_config: dict
    memory_config: dict
    channel_config: dict
    collaboration_config: dict
    ai_model_config: dict = Field(alias="model_config")
    tool_config: dict
    workflow_config: dict
    validation_state: dict
    published_at: datetime | None = None
    created_at: datetime


class AgentDetail(BaseModel):
    agent: AgentOut
    versions: list[AgentVersionOut]
    configuration: dict | None = None
    publishing_history: list[dict]


class AgentTemplateOut(BaseModel):
    id: UUID
    slug: str
    name: str
    category: str
    description: str | None = None
    role: str
    department: str | None = None
    default_config: dict
    recommended_tools: list[str]
    recommended_channels: list[str]
    featured: bool
    status: str


class PublishRequest(BaseModel):
    change_summary: str | None = None


class DuplicateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=180)


class BuilderStateUpdate(BaseModel):
    builder_state: dict = Field(default_factory=dict)
    readiness: dict = Field(default_factory=dict)
    playground_state: dict = Field(default_factory=dict)


class PlaygroundResult(BaseModel):
    response: str
    context_preview: dict
    memory_preview: dict
    tool_logs: list[dict]
    response_time_ms: int
    token_usage: dict