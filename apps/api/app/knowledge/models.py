from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class KnowledgeBase(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_bases"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_knowledge_base_workspace_slug"),)
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    owner_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[str] = mapped_column(String(40), default="workspace", index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)
    permissions: Mapped[dict] = mapped_column(JSONB, default=dict)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class KnowledgeCategory(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_categories"
    __table_args__ = (UniqueConstraint("knowledge_base_id", "slug", name="uq_knowledge_category_kb_slug"),)
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    parent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_categories.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(String(40))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class KnowledgeTag(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_tags"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_knowledge_tag_workspace_slug"),)
    name: Mapped[str] = mapped_column(String(120))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    color: Mapped[str | None] = mapped_column(String(40))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class KnowledgeFolder(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_folders"
    __table_args__ = (UniqueConstraint("knowledge_base_id", "parent_id", "name", name="uq_knowledge_folder_name"),)
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    parent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_folders.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    path: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class KnowledgeCollection(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_collections"
    __table_args__ = (UniqueConstraint("knowledge_base_id", "slug", name="uq_knowledge_collection_kb_slug"),)
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[str] = mapped_column(String(40), default="workspace")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DataSource(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "data_sources"
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(60), index=True)
    provider: Mapped[str | None] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(180))
    uri: Mapped[str | None] = mapped_column(Text)
    sync_status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    health_status: Mapped[str] = mapped_column(String(40), default="unknown", index=True)
    last_synced_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    next_sync_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    sync_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    credentials_ref: Mapped[str | None] = mapped_column(Text)


class WebsiteSource(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "website_sources"
    data_source_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), index=True)
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    base_url: Mapped[str] = mapped_column(Text)
    crawl_status: Mapped[str] = mapped_column(String(40), default="not_started", index=True)
    allowed_paths: Mapped[list[str]] = mapped_column(JSONB, default=list)
    blocked_paths: Mapped[list[str]] = mapped_column(JSONB, default=list)
    refresh_schedule: Mapped[dict] = mapped_column(JSONB, default=dict)
    crawl_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    last_crawled_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class Document(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "documents"
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    data_source_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="SET NULL"), index=True)
    folder_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_folders.id", ondelete="SET NULL"), index=True)
    category_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_categories.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str | None] = mapped_column(String(180), index=True)
    content_type: Mapped[str | None] = mapped_column(String(120), index=True)
    source_kind: Mapped[str] = mapped_column(String(60), default="document", index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    validation_status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    freshness_status: Mapped[str] = mapped_column(String(40), default="unknown", index=True)
    storage_file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    checksum: Mapped[str | None] = mapped_column(String(128), index=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    published_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    duplicate_of_document_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), index=True)
    owner_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    custom_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    archived_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class KnowledgeFAQ(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_faqs"
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DocumentVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "document_versions"
    document_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    title: Mapped[str] = mapped_column(String(300))
    content_ref: Mapped[str | None] = mapped_column(Text)
    checksum: Mapped[str | None] = mapped_column(String(128))
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    change_summary: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))


class KnowledgePermission(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_permissions"
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    principal_type: Mapped[str] = mapped_column(String(40), index=True)
    principal_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    role: Mapped[str] = mapped_column(String(40), default="reader", index=True)
    permissions: Mapped[list[str]] = mapped_column(JSONB, default=list)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class KnowledgeSyncJob(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_sync_jobs"
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    data_source_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="SET NULL"), index=True)
    sync_type: Mapped[str] = mapped_column(String(60), default="manual", index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    strategy: Mapped[str] = mapped_column(String(60), default="incremental")
    conflict_count: Mapped[int] = mapped_column(Integer, default=0)
    documents_scanned: Mapped[int] = mapped_column(Integer, default=0)
    documents_created: Mapped[int] = mapped_column(Integer, default=0)
    documents_updated: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class KnowledgeActivity(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_activity_logs"
    knowledge_base_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="SET NULL"), index=True)
    document_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), index=True)
    data_source_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="SET NULL"), index=True)
    actor_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(100), index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    trace_id: Mapped[str | None] = mapped_column(String(120), index=True)


class KnowledgeQualityCheck(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "knowledge_quality_checks"
    knowledge_base_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    check_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    severity: Mapped[str] = mapped_column(String(40), default="info", index=True)
    message: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    resolved_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class DocumentTagAssignment(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "document_tag_assignments"
    document_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    tag_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_tags.id", ondelete="CASCADE"), index=True)


class EmbeddingPlaceholder(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "embedding_placeholders"
    document_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    provider: Mapped[str] = mapped_column(String(60))
    model: Mapped[str] = mapped_column(String(120))
    vector_ref: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_knowledge_bases_workspace_active", KnowledgeBase.workspace_id, KnowledgeBase.status, KnowledgeBase.deleted_at)
Index("ix_knowledge_categories_kb_parent", KnowledgeCategory.knowledge_base_id, KnowledgeCategory.parent_id, KnowledgeCategory.deleted_at)
Index("ix_knowledge_tags_workspace_slug", KnowledgeTag.workspace_id, KnowledgeTag.slug, KnowledgeTag.deleted_at)
Index("ix_knowledge_folders_kb_parent", KnowledgeFolder.knowledge_base_id, KnowledgeFolder.parent_id, KnowledgeFolder.deleted_at)
Index("ix_data_sources_kb_status", DataSource.knowledge_base_id, DataSource.sync_status, DataSource.deleted_at)
Index("ix_website_sources_kb_status", WebsiteSource.knowledge_base_id, WebsiteSource.crawl_status, WebsiteSource.deleted_at)
Index("ix_documents_kb_active", Document.knowledge_base_id, Document.status, Document.deleted_at)
Index("ix_documents_kb_validation", Document.knowledge_base_id, Document.validation_status, Document.freshness_status)
Index("ix_documents_checksum", Document.knowledge_base_id, Document.checksum)
Index("ix_document_versions_document_version", DocumentVersion.document_id, DocumentVersion.version_number)
Index("ix_knowledge_permissions_principal", KnowledgePermission.principal_type, KnowledgePermission.principal_id, KnowledgePermission.role)
Index("ix_knowledge_sync_jobs_kb_status", KnowledgeSyncJob.knowledge_base_id, KnowledgeSyncJob.status, KnowledgeSyncJob.created_at)
Index("ix_knowledge_activity_kb_created", KnowledgeActivity.knowledge_base_id, KnowledgeActivity.created_at)
Index("ix_knowledge_quality_kb_status", KnowledgeQualityCheck.knowledge_base_id, KnowledgeQualityCheck.status, KnowledgeQualityCheck.severity)
Index("ix_embeddings_document_chunk", EmbeddingPlaceholder.document_id, EmbeddingPlaceholder.chunk_index)