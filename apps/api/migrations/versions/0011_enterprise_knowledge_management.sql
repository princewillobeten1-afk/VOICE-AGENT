ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS owner_user_id UUID REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS visibility VARCHAR(40) NOT NULL DEFAULT 'workspace';
ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS status VARCHAR(40) NOT NULL DEFAULT 'draft';
ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS stats JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS permissions JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS published_at TIMESTAMPTZ;

ALTER TABLE data_sources ADD COLUMN IF NOT EXISTS provider VARCHAR(80);
ALTER TABLE data_sources ADD COLUMN IF NOT EXISTS health_status VARCHAR(40) NOT NULL DEFAULT 'unknown';
ALTER TABLE data_sources ADD COLUMN IF NOT EXISTS last_synced_at TIMESTAMPTZ;
ALTER TABLE data_sources ADD COLUMN IF NOT EXISTS next_sync_at TIMESTAMPTZ;
ALTER TABLE data_sources ADD COLUMN IF NOT EXISTS sync_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE data_sources ADD COLUMN IF NOT EXISTS credentials_ref TEXT;

ALTER TABLE documents ADD COLUMN IF NOT EXISTS folder_id UUID;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS category_id UUID;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS slug VARCHAR(180);
ALTER TABLE documents ADD COLUMN IF NOT EXISTS source_kind VARCHAR(60) NOT NULL DEFAULT 'document';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS status VARCHAR(40) NOT NULL DEFAULT 'draft';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS validation_status VARCHAR(40) NOT NULL DEFAULT 'pending';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS freshness_status VARCHAR(40) NOT NULL DEFAULT 'unknown';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS version_number INTEGER NOT NULL DEFAULT 1;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS published_version_id UUID;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS duplicate_of_document_id UUID REFERENCES documents(id) ON DELETE SET NULL;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS owner_user_id UUID REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS custom_metadata JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS published_at TIMESTAMPTZ;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ;

CREATE TABLE IF NOT EXISTS knowledge_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES knowledge_categories(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(160) NOT NULL,
    slug VARCHAR(120) NOT NULL,
    description TEXT,
    color VARCHAR(40),
    sort_order INTEGER NOT NULL DEFAULT 0,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_knowledge_category_kb_slug UNIQUE (knowledge_base_id, slug)
);

CREATE TABLE IF NOT EXISTS knowledge_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(120) NOT NULL,
    color VARCHAR(40),
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_knowledge_tag_workspace_slug UNIQUE (workspace_id, slug)
);

CREATE TABLE IF NOT EXISTS knowledge_folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES knowledge_folders(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    path TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_knowledge_folder_name UNIQUE (knowledge_base_id, parent_id, name)
);

CREATE TABLE IF NOT EXISTS knowledge_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    slug VARCHAR(120) NOT NULL,
    description TEXT,
    visibility VARCHAR(40) NOT NULL DEFAULT 'workspace',
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_knowledge_collection_kb_slug UNIQUE (knowledge_base_id, slug)
);
CREATE TABLE IF NOT EXISTS website_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    base_url TEXT NOT NULL,
    crawl_status VARCHAR(40) NOT NULL DEFAULT 'not_started',
    allowed_paths JSONB NOT NULL DEFAULT '[]'::jsonb,
    blocked_paths JSONB NOT NULL DEFAULT '[]'::jsonb,
    refresh_schedule JSONB NOT NULL DEFAULT '{}'::jsonb,
    crawl_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_crawled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS knowledge_faqs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    version_number INTEGER NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    title VARCHAR(300) NOT NULL,
    content_ref TEXT,
    checksum VARCHAR(128),
    size_bytes BIGINT,
    change_summary TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS knowledge_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    principal_type VARCHAR(40) NOT NULL,
    principal_id UUID,
    role VARCHAR(40) NOT NULL DEFAULT 'reader',
    permissions JSONB NOT NULL DEFAULT '[]'::jsonb,
    expires_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS knowledge_sync_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    data_source_id UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    sync_type VARCHAR(60) NOT NULL DEFAULT 'manual',
    status VARCHAR(40) NOT NULL DEFAULT 'queued',
    strategy VARCHAR(60) NOT NULL DEFAULT 'incremental',
    conflict_count INTEGER NOT NULL DEFAULT 0,
    documents_scanned INTEGER NOT NULL DEFAULT 0,
    documents_created INTEGER NOT NULL DEFAULT 0,
    documents_updated INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS knowledge_activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE SET NULL,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    data_source_id UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    summary TEXT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    trace_id VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS knowledge_quality_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    check_type VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'pending',
    severity VARCHAR(40) NOT NULL DEFAULT 'info',
    message TEXT,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_tag_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES knowledge_tags(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE documents ADD CONSTRAINT fk_documents_knowledge_folder_id FOREIGN KEY (folder_id) REFERENCES knowledge_folders(id) ON DELETE SET NULL;
ALTER TABLE documents ADD CONSTRAINT fk_documents_knowledge_category_id FOREIGN KEY (category_id) REFERENCES knowledge_categories(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS ix_knowledge_bases_workspace_status ON knowledge_bases(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_knowledge_bases_owner ON knowledge_bases(owner_user_id, status);
CREATE INDEX IF NOT EXISTS ix_knowledge_categories_kb_parent ON knowledge_categories(knowledge_base_id, parent_id, deleted_at);
CREATE INDEX IF NOT EXISTS ix_knowledge_tags_workspace_slug ON knowledge_tags(workspace_id, slug, deleted_at);
CREATE INDEX IF NOT EXISTS ix_knowledge_folders_kb_parent ON knowledge_folders(knowledge_base_id, parent_id, deleted_at);
CREATE INDEX IF NOT EXISTS ix_knowledge_collections_kb_slug ON knowledge_collections(knowledge_base_id, slug, deleted_at);
CREATE INDEX IF NOT EXISTS ix_data_sources_kb_status ON data_sources(knowledge_base_id, sync_status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_data_sources_provider_health ON data_sources(provider, health_status, last_synced_at);
CREATE INDEX IF NOT EXISTS ix_website_sources_kb_status ON website_sources(knowledge_base_id, crawl_status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_documents_kb_status ON documents(knowledge_base_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_documents_kb_validation ON documents(knowledge_base_id, validation_status, freshness_status);
CREATE INDEX IF NOT EXISTS ix_documents_checksum ON documents(knowledge_base_id, checksum);
CREATE INDEX IF NOT EXISTS ix_documents_source_kind ON documents(workspace_id, source_kind, status);
CREATE INDEX IF NOT EXISTS ix_knowledge_faqs_kb_status ON knowledge_faqs(knowledge_base_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_document_versions_document_version ON document_versions(document_id, version_number);
CREATE INDEX IF NOT EXISTS ix_knowledge_permissions_principal ON knowledge_permissions(principal_type, principal_id, role);
CREATE INDEX IF NOT EXISTS ix_knowledge_permissions_kb_document ON knowledge_permissions(knowledge_base_id, document_id);
CREATE INDEX IF NOT EXISTS ix_knowledge_sync_jobs_kb_status ON knowledge_sync_jobs(knowledge_base_id, status, created_at);
CREATE INDEX IF NOT EXISTS ix_knowledge_activity_kb_created ON knowledge_activity_logs(knowledge_base_id, created_at);
CREATE INDEX IF NOT EXISTS ix_knowledge_quality_kb_status ON knowledge_quality_checks(knowledge_base_id, status, severity);
CREATE INDEX IF NOT EXISTS ix_document_tag_assignments_document ON document_tag_assignments(document_id, tag_id);
