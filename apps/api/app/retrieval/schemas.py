from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ProviderConfigCreate(BaseModel):
    workspace_id: UUID
    name: str
    provider_type: str
    provider: str
    status: str = "disabled"
    priority: int = 100
    secret_ref: str | None = None
    model: str | None = None
    dimensions: int | None = None
    capabilities: list[str] = Field(default_factory=list)
    config: dict = Field(default_factory=dict)
    health_state: dict = Field(default_factory=dict)


class ProviderConfigOut(ProviderConfigCreate):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RetrievalSettingCreate(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID | None = None
    chunking_strategy: str = "paragraph_aware"
    chunk_size: int = 900
    chunk_overlap: int = 120
    embedding_provider_config_id: UUID | None = None
    vector_provider_config_id: UUID | None = None
    reranker_provider_config_id: UUID | None = None
    hybrid_weights: dict = Field(default_factory=lambda: {"semantic": 0.45, "keyword": 0.35, "metadata": 0.1, "recency": 0.1})
    token_budget: int = 4000
    metadata_filters: dict = Field(default_factory=dict)
    permission_mode: str = "strict"
    cache_policy: dict = Field(default_factory=dict)


class RetrievalSettingOut(RetrievalSettingCreate):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class IndexCreate(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID | None = None
    name: str
    vector_store_provider: str = "metadata_only"
    vector_store_ref: str | None = None
    embedding_provider: str = "placeholder"
    embedding_model: str | None = None
    dimensions: int | None = None
    metadata_json: dict = Field(default_factory=dict)


class IndexOut(BaseModel):
    id: UUID
    workspace_id: UUID
    knowledge_base_id: UUID | None = None
    name: str
    status: str
    vector_store_provider: str
    vector_store_ref: str | None = None
    embedding_provider: str
    embedding_model: str | None = None
    dimensions: int | None = None
    chunk_count: int
    document_count: int
    size_bytes: int
    last_indexed_at: datetime | None = None
    metadata_json: dict
    created_at: datetime | None = None
    updated_at: datetime | None = None


class IndexContentRequest(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID
    document_id: UUID | None = None
    index_id: UUID | None = None
    strategy: str = "incremental"
    chunking_strategy: str = "paragraph_aware"
    chunk_size: int = 900
    chunk_overlap: int = 120


class EmbeddingJobOut(BaseModel):
    id: UUID
    knowledge_base_id: UUID | None = None
    document_id: UUID | None = None
    index_id: UUID | None = None
    job_type: str
    status: str
    provider: str
    model: str | None = None
    chunk_count: int
    processed_chunks: int
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    metadata_json: dict
    created_at: datetime | None = None


class ChunkOut(BaseModel):
    id: UUID
    knowledge_base_id: UUID
    document_id: UUID
    index_id: UUID | None = None
    chunk_index: int
    chunk_strategy: str
    content_ref: str | None = None
    text_preview: str | None = None
    token_count: int
    char_count: int
    language: str | None = None
    section_title: str | None = None
    metadata_json: dict
    embedding_state: dict
    vector_ref: str | None = None
    checksum: str | None = None
    status: str
    created_at: datetime | None = None


class SearchRequest(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID | None = None
    agent_id: UUID | None = None
    conversation_id: UUID | None = None
    query: str
    search_mode: str = "hybrid"
    filters: dict = Field(default_factory=dict)
    weights: dict = Field(default_factory=lambda: {"semantic": 0.45, "keyword": 0.35, "metadata": 0.1, "recency": 0.1})
    limit: int = Field(default=8, ge=1, le=50)
    token_budget: int = 4000
    rerank: bool = True


class SearchResult(BaseModel):
    chunk: ChunkOut
    score: float
    reasons: list[str]
    citation: dict


class ContextAssemblyOut(BaseModel):
    retrieval_request_id: UUID
    query: str
    context: str
    citations: list[dict]
    chunks: list[SearchResult]
    token_budget: int
    context_tokens: int
    permission_summary: dict
    latency_ms: int


class RetrievalRequestOut(BaseModel):
    id: UUID
    knowledge_base_id: UUID | None = None
    agent_id: UUID | None = None
    conversation_id: UUID | None = None
    query: str
    search_mode: str
    status: str
    filters: dict
    weights: dict
    result_count: int
    latency_ms: int | None = None
    token_budget: int | None = None
    context_tokens: int | None = None
    permission_summary: dict
    metadata_json: dict
    created_at: datetime | None = None


class RetrievalMetricsOut(BaseModel):
    indexes: int
    chunks: int
    embedding_jobs: int
    retrieval_requests: int
    average_latency_ms: int | None = None
    provider_catalog: list[dict]
    observability: dict