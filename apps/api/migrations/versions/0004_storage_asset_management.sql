-- VoiceSense Task 008: Storage and asset management foundation.
-- Storage is organization and workspace scoped. Object bytes live in an external provider;
-- this schema stores metadata, lifecycle state, hierarchy, versions, tags, and upload sessions.

CREATE TABLE IF NOT EXISTS storage_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider VARCHAR(60) NOT NULL,
    name VARCHAR(160) NOT NULL,
    environment VARCHAR(40) NOT NULL DEFAULT 'development',
    bucket VARCHAR(180),
    region VARCHAR(80),
    config_ref TEXT,
    capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_default BOOLEAN NOT NULL DEFAULT false,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_storage_providers_provider ON storage_providers(provider);
CREATE INDEX IF NOT EXISTS ix_storage_providers_provider_env ON storage_providers(provider, environment, deleted_at);
CREATE UNIQUE INDEX IF NOT EXISTS uq_storage_provider_default_env
    ON storage_providers(environment)
    WHERE is_default = true AND deleted_at IS NULL;

INSERT INTO storage_providers (provider, name, environment, bucket, capabilities, is_default)
VALUES ('local', 'Local development storage', 'development', 'voicesense-local', '["upload", "download", "delete", "preview"]'::jsonb, true)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    parent_folder_id UUID REFERENCES folders(id) ON DELETE CASCADE,
    name VARCHAR(180) NOT NULL,
    path TEXT NOT NULL,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_folder_parent_name UNIQUE (workspace_id, parent_folder_id, name)
);

CREATE INDEX IF NOT EXISTS ix_folders_organization_id ON folders(organization_id);
CREATE INDEX IF NOT EXISTS ix_folders_workspace_id ON folders(workspace_id);
CREATE INDEX IF NOT EXISTS ix_folders_project_id ON folders(project_id);
CREATE INDEX IF NOT EXISTS ix_folders_parent_folder_id ON folders(parent_folder_id);
CREATE INDEX IF NOT EXISTS ix_folders_workspace_parent ON folders(workspace_id, parent_folder_id, deleted_at);

ALTER TABLE files ADD COLUMN IF NOT EXISTS folder_id UUID REFERENCES folders(id) ON DELETE SET NULL;
ALTER TABLE files ADD COLUMN IF NOT EXISTS storage_provider_id UUID REFERENCES storage_providers(id) ON DELETE SET NULL;
ALTER TABLE files ADD COLUMN IF NOT EXISTS original_name VARCHAR(300);
ALTER TABLE files ADD COLUMN IF NOT EXISTS stored_name VARCHAR(300);
ALTER TABLE files ADD COLUMN IF NOT EXISTS extension VARCHAR(24);
ALTER TABLE files ADD COLUMN IF NOT EXISTS status VARCHAR(40) NOT NULL DEFAULT 'ready';
ALTER TABLE files ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE files ADD COLUMN IF NOT EXISTS tags JSONB NOT NULL DEFAULT '[]'::jsonb;
ALTER TABLE files ADD COLUMN IF NOT EXISTS scanned_at TIMESTAMPTZ;
ALTER TABLE files ADD COLUMN IF NOT EXISTS scan_status VARCHAR(40);

UPDATE files SET original_name = filename WHERE original_name IS NULL;
UPDATE files SET stored_name = filename WHERE stored_name IS NULL;
UPDATE files SET extension = lower(regexp_replace(filename, '^.*\.', '')) WHERE extension IS NULL AND filename LIKE '%.%';
UPDATE files SET status = 'ready' WHERE status IS NULL;
UPDATE files SET tags = '[]'::jsonb WHERE tags IS NULL;

ALTER TABLE files ALTER COLUMN original_name SET NOT NULL;
ALTER TABLE files ALTER COLUMN stored_name SET NOT NULL;

CREATE INDEX IF NOT EXISTS ix_files_folder_id ON files(folder_id);
CREATE INDEX IF NOT EXISTS ix_files_storage_provider_id ON files(storage_provider_id);
CREATE INDEX IF NOT EXISTS ix_files_extension ON files(extension);
CREATE INDEX IF NOT EXISTS ix_files_workspace_purpose ON files(workspace_id, purpose, deleted_at);
CREATE INDEX IF NOT EXISTS ix_files_workspace_folder ON files(workspace_id, folder_id, deleted_at);
CREATE INDEX IF NOT EXISTS ix_files_workspace_status ON files(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_files_workspace_name_search ON files USING gin (to_tsvector('simple', coalesce(original_name, '') || ' ' || coalesce(filename, '')));

CREATE TABLE IF NOT EXISTS file_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    provider VARCHAR(60) NOT NULL,
    bucket VARCHAR(180) NOT NULL,
    object_key TEXT NOT NULL,
    size_bytes BIGINT,
    checksum VARCHAR(128),
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_file_version UNIQUE (file_id, version)
);

CREATE INDEX IF NOT EXISTS ix_file_versions_organization_id ON file_versions(organization_id);
CREATE INDEX IF NOT EXISTS ix_file_versions_workspace_id ON file_versions(workspace_id);
CREATE INDEX IF NOT EXISTS ix_file_versions_file_id ON file_versions(file_id);
CREATE INDEX IF NOT EXISTS ix_file_versions_file_version ON file_versions(file_id, version);

CREATE TABLE IF NOT EXISTS upload_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    folder_id UUID REFERENCES folders(id) ON DELETE SET NULL,
    file_id UUID REFERENCES files(id) ON DELETE SET NULL,
    provider VARCHAR(60) NOT NULL DEFAULT 'local',
    original_name VARCHAR(300) NOT NULL,
    content_type VARCHAR(120),
    size_bytes BIGINT,
    status VARCHAR(40) NOT NULL DEFAULT 'initiated',
    upload_url_ref TEXT,
    resumable_token_hash VARCHAR(128),
    expires_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_upload_sessions_organization_id ON upload_sessions(organization_id);
CREATE INDEX IF NOT EXISTS ix_upload_sessions_workspace_id ON upload_sessions(workspace_id);
CREATE INDEX IF NOT EXISTS ix_upload_sessions_project_id ON upload_sessions(project_id);
CREATE INDEX IF NOT EXISTS ix_upload_sessions_folder_id ON upload_sessions(folder_id);
CREATE INDEX IF NOT EXISTS ix_upload_sessions_file_id ON upload_sessions(file_id);
CREATE INDEX IF NOT EXISTS ix_upload_sessions_workspace_status ON upload_sessions(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_upload_sessions_expires_at ON upload_sessions(expires_at);

CREATE TABLE IF NOT EXISTS file_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(80) NOT NULL,
    color VARCHAR(24),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_file_tag_workspace_name UNIQUE (workspace_id, name)
);

CREATE INDEX IF NOT EXISTS ix_file_tags_organization_id ON file_tags(organization_id);
CREATE INDEX IF NOT EXISTS ix_file_tags_workspace_id ON file_tags(workspace_id);

CREATE TABLE IF NOT EXISTS file_tag_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES file_tags(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_file_tag_assignment UNIQUE (file_id, tag_id)
);

CREATE INDEX IF NOT EXISTS ix_file_tag_assignments_organization_id ON file_tag_assignments(organization_id);
CREATE INDEX IF NOT EXISTS ix_file_tag_assignments_workspace_id ON file_tag_assignments(workspace_id);
CREATE INDEX IF NOT EXISTS ix_file_tag_assignments_file_id ON file_tag_assignments(file_id);
CREATE INDEX IF NOT EXISTS ix_file_tag_assignments_tag_id ON file_tag_assignments(tag_id);