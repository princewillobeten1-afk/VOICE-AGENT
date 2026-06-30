from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    workspace_id: UUID
    agent_id: UUID | None = None
    conversation_id: UUID | None = None
    user_id: UUID | None = None
    category_id: UUID | None = None
    policy_id: UUID | None = None
    memory_type: str = "long_term"
    title: str = Field(min_length=2, max_length=240)
    content: str = Field(min_length=1)
    summary: str | None = None
    privacy_level: str = "internal"
    visibility: str = "workspace"
    source_type: str = "manual"
    source_ref: str | None = None
    importance_score: float | None = None
    confidence_score: float | None = None
    tags: list[str] = Field(default_factory=list)
    facts: dict = Field(default_factory=dict)
    expires_at: datetime | None = None


class MemoryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    summary: str | None = None
    category_id: UUID | None = None
    memory_type: str | None = None
    privacy_level: str | None = None
    visibility: str | None = None
    importance_score: float | None = None
    confidence_score: float | None = None
    tags: list[str] | None = None
    facts: dict | None = None
    expires_at: datetime | None = None
    change_summary: str | None = None


class MemoryOut(BaseModel):
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    agent_id: UUID | None = None
    conversation_id: UUID | None = None
    user_id: UUID | None = None
    category_id: UUID | None = None
    policy_id: UUID | None = None
    memory_type: str
    title: str
    content: str
    summary: str | None = None
    status: str
    privacy_level: str
    visibility: str
    source_type: str
    source_ref: str | None = None
    importance_score: float
    confidence_score: float
    recency_score: float
    retrieval_count: int
    pinned: bool
    encrypted: bool
    tags: list[str]
    facts: dict
    evaluation: dict
    index_state: dict
    expires_at: datetime | None = None
    archived_at: datetime | None = None
    forgotten_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MemorySearchQuery(BaseModel):
    workspace_id: UUID
    q: str | None = None
    memory_types: list[str] = Field(default_factory=list)
    categories: list[UUID] = Field(default_factory=list)
    agent_id: UUID | None = None
    user_id: UUID | None = None
    privacy_levels: list[str] = Field(default_factory=list)
    include_archived: bool = False
    limit: int = Field(default=20, ge=1, le=100)


class MemorySearchResult(BaseModel):
    memory: MemoryOut
    score: float
    reasons: list[str]


class MemoryCategoryCreate(BaseModel):
    workspace_id: UUID
    name: str
    slug: str
    description: str | None = None
    color: str | None = None
    retention_days: int | None = None
    default_privacy_level: str = "internal"
    metadata_json: dict = Field(default_factory=dict)


class MemoryCategoryOut(MemoryCategoryCreate):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MemoryPolicyCreate(BaseModel):
    workspace_id: UUID
    name: str
    status: str = "active"
    scope: str = "workspace"
    memory_types: list[str] = Field(default_factory=list)
    retention_days: int | None = None
    expiration_rules: dict = Field(default_factory=dict)
    auto_cleanup_enabled: bool = False
    max_memory_size: int | None = None
    privacy_rules: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class MemoryPolicyOut(MemoryPolicyCreate):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MemoryVersionOut(BaseModel):
    id: UUID
    memory_id: UUID
    version_number: int
    title: str
    content: str
    summary: str | None = None
    change_type: str
    change_summary: str | None = None
    evaluation: dict
    created_at: datetime | None = None


class MemoryActionRequest(BaseModel):
    reason: str | None = None


class MemoryMergeRequest(BaseModel):
    target_memory_id: UUID
    strategy: str = "append_summary"
    reason: str | None = None


class MemoryLinkCreate(BaseModel):
    target_memory_id: UUID
    link_type: str = "related"
    strength: float = 0.5
    metadata_json: dict = Field(default_factory=dict)


class MemoryLinkOut(BaseModel):
    id: UUID
    source_memory_id: UUID
    target_memory_id: UUID
    link_type: str
    strength: float
    metadata_json: dict


class MemoryAnalyticsOut(BaseModel):
    total_memories: int
    active_memories: int
    archived_memories: int
    pinned_memories: int
    by_type: dict
    by_privacy: dict
    observability: dict


class MemoryDetail(BaseModel):
    memory: MemoryOut
    versions: list[MemoryVersionOut]
    links: list[MemoryLinkOut]
    related: list[MemorySearchResult]