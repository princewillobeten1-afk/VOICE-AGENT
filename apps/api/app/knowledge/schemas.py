from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class KnowledgeBaseCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID | None = None
    name: str = Field(min_length=2, max_length=180)
    slug: str | None = None
    description: str | None = None
    visibility: str = "workspace"
    status: str = "draft"
    permissions: dict = Field(default_factory=dict)
    settings: dict = Field(default_factory=dict)


class KnowledgeBaseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    visibility: str | None = None
    status: str | None = None
    permissions: dict | None = None
    settings: dict | None = None


class KnowledgeBaseOut(BaseModel):
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    project_id: UUID | None = None
    owner_user_id: UUID | None = None
    name: str
    slug: str
    description: str | None = None
    visibility: str
    status: str
    stats: dict
    permissions: dict
    settings: dict
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SourceCreate(BaseModel):
    knowledge_base_id: UUID
    workspace_id: UUID
    type: str
    provider: str | None = None
    name: str
    uri: str | None = None
    config: dict = Field(default_factory=dict)
    sync_config: dict = Field(default_factory=dict)
    credentials_ref: str | None = None


class SourceOut(SourceCreate):
    id: UUID
    sync_status: str
    health_status: str
    last_synced_at: datetime | None = None
    next_sync_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class WebsiteSourceCreate(BaseModel):
    knowledge_base_id: UUID
    data_source_id: UUID
    workspace_id: UUID
    base_url: str
    allowed_paths: list[str] = Field(default_factory=list)
    blocked_paths: list[str] = Field(default_factory=list)
    refresh_schedule: dict = Field(default_factory=dict)
    crawl_config: dict = Field(default_factory=dict)


class WebsiteSourceOut(WebsiteSourceCreate):
    id: UUID
    crawl_status: str
    last_crawled_at: datetime | None = None


class DocumentCreate(BaseModel):
    knowledge_base_id: UUID
    workspace_id: UUID
    data_source_id: UUID | None = None
    folder_id: UUID | None = None
    category_id: UUID | None = None
    title: str
    content_type: str | None = None
    source_kind: str = "document"
    storage_file_id: UUID | None = None
    checksum: str | None = None
    size_bytes: int | None = None
    custom_metadata: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class DocumentUpdate(BaseModel):
    title: str | None = None
    folder_id: UUID | None = None
    category_id: UUID | None = None
    status: str | None = None
    validation_status: str | None = None
    freshness_status: str | None = None
    custom_metadata: dict | None = None
    metadata_json: dict | None = None
    change_summary: str | None = None


class DocumentOut(BaseModel):
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    knowledge_base_id: UUID
    data_source_id: UUID | None = None
    folder_id: UUID | None = None
    category_id: UUID | None = None
    title: str
    slug: str | None = None
    content_type: str | None = None
    source_kind: str
    status: str
    validation_status: str
    freshness_status: str
    storage_file_id: UUID | None = None
    checksum: str | None = None
    size_bytes: int | None = None
    version_number: int
    published_version_id: UUID | None = None
    duplicate_of_document_id: UUID | None = None
    owner_user_id: UUID | None = None
    custom_metadata: dict
    metadata_json: dict
    published_at: datetime | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DocumentVersionOut(BaseModel):
    id: UUID
    document_id: UUID
    version_number: int
    status: str
    title: str
    content_ref: str | None = None
    checksum: str | None = None
    size_bytes: int | None = None
    change_summary: str | None = None
    metadata_json: dict
    published_at: datetime | None = None
    created_at: datetime | None = None


class PermissionCreate(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID | None = None
    document_id: UUID | None = None
    principal_type: str
    principal_id: UUID | None = None
    role: str = "reader"
    permissions: list[str] = Field(default_factory=list)
    expires_at: datetime | None = None
    metadata_json: dict = Field(default_factory=dict)


class PermissionOut(PermissionCreate):
    id: UUID
    created_at: datetime | None = None


class SyncRequest(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID
    data_source_id: UUID | None = None
    sync_type: str = "manual"
    strategy: str = "incremental"


class SyncJobOut(BaseModel):
    id: UUID
    knowledge_base_id: UUID
    data_source_id: UUID | None = None
    sync_type: str
    status: str
    strategy: str
    conflict_count: int
    documents_scanned: int
    documents_created: int
    documents_updated: int
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    metadata_json: dict
    created_at: datetime | None = None


class CategoryCreate(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID
    parent_id: UUID | None = None
    name: str
    slug: str | None = None
    description: str | None = None
    color: str | None = None
    sort_order: int = 0
    metadata_json: dict = Field(default_factory=dict)


class CategoryOut(CategoryCreate):
    id: UUID


class ActivityOut(BaseModel):
    id: UUID
    knowledge_base_id: UUID | None = None
    document_id: UUID | None = None
    data_source_id: UUID | None = None
    actor_user_id: UUID | None = None
    action: str
    summary: str | None = None
    payload: dict
    created_at: datetime | None = None


class KnowledgeSearchQuery(BaseModel):
    workspace_id: UUID
    knowledge_base_id: UUID | None = None
    q: str | None = None
    status: str | None = None
    source_kind: str | None = None
    limit: int = Field(default=25, ge=1, le=100)


class KnowledgeDashboard(BaseModel):
    knowledge_bases: list[KnowledgeBaseOut]
    documents: list[DocumentOut]
    sources: list[SourceOut]
    recent_activity: list[ActivityOut]
    stats: dict