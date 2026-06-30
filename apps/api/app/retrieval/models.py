from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class RetrievalProviderConfig(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "retrieval_provider_configs"
    __table_args__ = (UniqueConstraint("workspace_id", "provider_type", "provider", "name", name="uq_retrieval_provider_config"),)
    name: Mapped[str] = mapped_column(String(160))
    provider_type: Mapped[str] = mapped_column(String(60), index=True)
    provider: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    model: Mapped[str | None] = mapped_column(String(160))
    dimensions: Mapped[int | None] = mapped_column(Integer)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    health_state: Mapped[dict] = mapped_column(JSONB, default=dict)


class RetrievalSetting(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "retrieval_settings"
    __table_args__ = (UniqueConstraint("workspace_id", "knowledge_base_id", name="uq_retrieval_setting_kb"),)
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    chunking_strategy: Mapped[str] = mapped_column(String(80), default="paragraph_aware")
    chunk_size: Mapped[int] = mapped_column(Integer, default=900)
    chunk_overlap: Mapped[int] = mapped_column(Integer, default=120)
    embedding_provider_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("retrieval_provider_configs.id", ondelete="SET NULL"), index=True)
    vector_provider_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("retrieval_provider_configs.id", ondelete="SET NULL"), index=True)
    reranker_provider_config_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("retrieval_provider_configs.id", ondelete="SET NULL"), index=True)
    hybrid_weights: Mapped[dict] = mapped_column(JSONB, default=dict)
    token_budget: Mapped[int] = mapped_column(Integer, default=4000)
    metadata_filters: Mapped[dict] = mapped_column(JSONB, default=dict)
    permission_mode: Mapped[str] = mapped_column(String(60), default="strict")
    cache_policy: Mapped[dict] = mapped_column(JSONB, default=dict)


class RetrievalIndex(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "retrieval_indexes"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_retrieval_index_workspace_name"),)
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    vector_store_provider: Mapped[str] = mapped_column(String(80), default="metadata_only")
    vector_store_ref: Mapped[str | None] = mapped_column(Text)
    embedding_provider: Mapped[str] = mapped_column(String(80), default="placeholder")
    embedding_model: Mapped[str | None] = mapped_column(String(160))
    dimensions: Mapped[int | None] = mapped_column(Integer)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    document_count: Mapped[int] = mapped_column(Integer, default=0)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    last_indexed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class RetrievalChunk(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "retrieval_chunks"
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    index_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("retrieval_indexes.id", ondelete="SET NULL"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    chunk_strategy: Mapped[str] = mapped_column(String(80), default="paragraph_aware", index=True)
    content_ref: Mapped[str | None] = mapped_column(Text)
    text_preview: Mapped[str | None] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    char_count: Mapped[int] = mapped_column(Integer, default=0)
    language: Mapped[str | None] = mapped_column(String(32), index=True)
    section_title: Mapped[str | None] = mapped_column(String(240))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    embedding_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    vector_ref: Mapped[str | None] = mapped_column(Text)
    checksum: Mapped[str | None] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(40), default="ready", index=True)


class EmbeddingJob(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "embedding_jobs"
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    index_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("retrieval_indexes.id", ondelete="SET NULL"), index=True)
    job_type: Mapped[str] = mapped_column(String(60), default="index", index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    provider: Mapped[str] = mapped_column(String(80), default="placeholder")
    model: Mapped[str | None] = mapped_column(String(160))
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    processed_chunks: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class RetrievalRequest(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "retrieval_requests"
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    query: Mapped[str] = mapped_column(Text)
    search_mode: Mapped[str] = mapped_column(String(60), default="hybrid", index=True)
    status: Mapped[str] = mapped_column(String(40), default="completed", index=True)
    filters: Mapped[dict] = mapped_column(JSONB, default=dict)
    weights: Mapped[dict] = mapped_column(JSONB, default=dict)
    result_count: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    token_budget: Mapped[int | None] = mapped_column(Integer)
    context_tokens: Mapped[int | None] = mapped_column(Integer)
    permission_summary: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SearchLog(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "search_logs"
    retrieval_request_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("retrieval_requests.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    stage: Mapped[str | None] = mapped_column(String(80), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)


class RetrievalMetric(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "retrieval_metrics"
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 3))
    unit: Mapped[str] = mapped_column(String(32), default="count")
    scope: Mapped[str] = mapped_column(String(60), default="workspace", index=True)
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="SET NULL"), index=True)
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_retrieval_provider_configs_workspace_type", RetrievalProviderConfig.workspace_id, RetrievalProviderConfig.provider_type, RetrievalProviderConfig.status, RetrievalProviderConfig.priority)
Index("ix_retrieval_indexes_kb_status", RetrievalIndex.knowledge_base_id, RetrievalIndex.status, RetrievalIndex.last_indexed_at)
Index("ix_retrieval_chunks_document_index", RetrievalChunk.document_id, RetrievalChunk.chunk_index)
Index("ix_retrieval_chunks_kb_status", RetrievalChunk.knowledge_base_id, RetrievalChunk.status, RetrievalChunk.language)
Index("ix_embedding_jobs_status", EmbeddingJob.workspace_id, EmbeddingJob.status, EmbeddingJob.created_at)
Index("ix_retrieval_requests_kb_created", RetrievalRequest.knowledge_base_id, RetrievalRequest.created_at)
Index("ix_search_logs_request_stage", SearchLog.retrieval_request_id, SearchLog.stage, SearchLog.created_at)
Index("ix_retrieval_metrics_metric_time", RetrievalMetric.workspace_id, RetrievalMetric.metric_name, RetrievalMetric.captured_at)