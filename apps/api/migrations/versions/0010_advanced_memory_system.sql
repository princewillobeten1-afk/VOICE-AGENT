CREATE TABLE IF NOT EXISTS memory_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(120) NOT NULL,
    description TEXT,
    color VARCHAR(40),
    retention_days INTEGER,
    default_privacy_level VARCHAR(40) NOT NULL DEFAULT 'internal',
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_memory_category_workspace_slug UNIQUE (workspace_id, slug)
);

CREATE TABLE IF NOT EXISTS memory_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(160) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    scope VARCHAR(40) NOT NULL DEFAULT 'workspace',
    memory_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    retention_days INTEGER,
    expiration_rules JSONB NOT NULL DEFAULT '{}'::jsonb,
    auto_cleanup_enabled BOOLEAN NOT NULL DEFAULT false,
    max_memory_size INTEGER,
    privacy_rules JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_memory_policy_workspace_name UNIQUE (workspace_id, name)
);

CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    category_id UUID REFERENCES memory_categories(id) ON DELETE SET NULL,
    policy_id UUID REFERENCES memory_policies(id) ON DELETE SET NULL,
    memory_type VARCHAR(60) NOT NULL,
    title VARCHAR(240) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    privacy_level VARCHAR(40) NOT NULL DEFAULT 'internal',
    visibility VARCHAR(40) NOT NULL DEFAULT 'workspace',
    source_type VARCHAR(80) NOT NULL DEFAULT 'manual',
    source_ref VARCHAR(180),
    importance_score NUMERIC(5, 2) NOT NULL DEFAULT 0,
    confidence_score NUMERIC(5, 2) NOT NULL DEFAULT 0,
    recency_score NUMERIC(5, 2) NOT NULL DEFAULT 0,
    retrieval_count INTEGER NOT NULL DEFAULT 0,
    pinned BOOLEAN NOT NULL DEFAULT false,
    encrypted BOOLEAN NOT NULL DEFAULT false,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    facts JSONB NOT NULL DEFAULT '{}'::jsonb,
    evaluation JSONB NOT NULL DEFAULT '{}'::jsonb,
    index_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    expires_at TIMESTAMPTZ,
    archived_at TIMESTAMPTZ,
    forgotten_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS memory_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    title VARCHAR(240) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    change_type VARCHAR(60) NOT NULL DEFAULT 'created',
    change_summary TEXT,
    evaluation JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memory_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    source_memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    target_memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    link_type VARCHAR(60) NOT NULL DEFAULT 'related',
    strength NUMERIC(5, 2) NOT NULL DEFAULT 0,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memory_access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    principal_type VARCHAR(40) NOT NULL,
    principal_id UUID,
    permission VARCHAR(40) NOT NULL DEFAULT 'read',
    granted_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    expires_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memory_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    memory_id UUID REFERENCES memories(id) ON DELETE SET NULL,
    event_type VARCHAR(80) NOT NULL,
    actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    trace_id VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memory_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    metric_name VARCHAR(80) NOT NULL,
    metric_value NUMERIC(14, 3) NOT NULL,
    unit VARCHAR(32) NOT NULL DEFAULT 'count',
    scope VARCHAR(40) NOT NULL DEFAULT 'workspace',
    dimensions JSONB NOT NULL DEFAULT '{}'::jsonb,
    captured_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_memory_categories_workspace_slug ON memory_categories(workspace_id, slug, deleted_at);
CREATE INDEX IF NOT EXISTS ix_memory_policies_workspace_status ON memory_policies(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_memories_workspace_type_status ON memories(workspace_id, memory_type, status, updated_at);
CREATE INDEX IF NOT EXISTS ix_memories_workspace_privacy ON memories(workspace_id, privacy_level, visibility, status);
CREATE INDEX IF NOT EXISTS ix_memories_agent_status ON memories(agent_id, status, updated_at);
CREATE INDEX IF NOT EXISTS ix_memories_user_status ON memories(user_id, status, updated_at);
CREATE INDEX IF NOT EXISTS ix_memories_category_status ON memories(category_id, status, updated_at);
CREATE INDEX IF NOT EXISTS ix_memories_pinned_importance ON memories(workspace_id, pinned, importance_score);
CREATE INDEX IF NOT EXISTS ix_memory_versions_memory_version ON memory_versions(memory_id, version_number);
CREATE INDEX IF NOT EXISTS ix_memory_links_source_target ON memory_links(source_memory_id, target_memory_id);
CREATE INDEX IF NOT EXISTS ix_memory_access_principal ON memory_access(principal_type, principal_id, permission);
CREATE INDEX IF NOT EXISTS ix_memory_events_memory_type ON memory_events(memory_id, event_type, created_at);
CREATE INDEX IF NOT EXISTS ix_memory_statistics_metric_time ON memory_statistics(workspace_id, metric_name, captured_at);