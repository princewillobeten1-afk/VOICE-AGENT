CREATE TABLE IF NOT EXISTS retrieval_provider_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(160) NOT NULL,
    provider_type VARCHAR(60) NOT NULL,
    provider VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'disabled',
    priority INTEGER NOT NULL DEFAULT 100,
    secret_ref TEXT,
    model VARCHAR(160),
    dimensions INTEGER,
    capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    health_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_retrieval_provider_config UNIQUE (workspace_id, provider_type, provider, name)
);

CREATE TABLE IF NOT EXISTS retrieval_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    chunking_strategy VARCHAR(80) NOT NULL DEFAULT 'paragraph_aware',
    chunk_size INTEGER NOT NULL DEFAULT 900,
    chunk_overlap INTEGER NOT NULL DEFAULT 120,
    embedding_provider_config_id UUID REFERENCES retrieval_provider_configs(id) ON DELETE SET NULL,
    vector_provider_config_id UUID REFERENCES retrieval_provider_configs(id) ON DELETE SET NULL,
    reranker_provider_config_id UUID REFERENCES retrieval_provider_configs(id) ON DELETE SET NULL,
    hybrid_weights JSONB NOT NULL DEFAULT '{}'::jsonb,
    token_budget INTEGER NOT NULL DEFAULT 4000,
    metadata_filters JSONB NOT NULL DEFAULT '{}'::jsonb,
    permission_mode VARCHAR(60) NOT NULL DEFAULT 'strict',
    cache_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_retrieval_setting_kb UNIQUE (workspace_id, knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS retrieval_indexes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    vector_store_provider VARCHAR(80) NOT NULL DEFAULT 'metadata_only',
    vector_store_ref TEXT,
    embedding_provider VARCHAR(80) NOT NULL DEFAULT 'placeholder',
    embedding_model VARCHAR(160),
    dimensions INTEGER,
    chunk_count INTEGER NOT NULL DEFAULT 0,
    document_count INTEGER NOT NULL DEFAULT 0,
    size_bytes INTEGER NOT NULL DEFAULT 0,
    last_indexed_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_retrieval_index_workspace_name UNIQUE (workspace_id, name)
);

CREATE TABLE IF NOT EXISTS retrieval_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    index_id UUID REFERENCES retrieval_indexes(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    chunk_index INTEGER NOT NULL,
    chunk_strategy VARCHAR(80) NOT NULL DEFAULT 'paragraph_aware',
    content_ref TEXT,
    text_preview TEXT,
    token_count INTEGER NOT NULL DEFAULT 0,
    char_count INTEGER NOT NULL DEFAULT 0,
    language VARCHAR(32),
    section_title VARCHAR(240),
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    embedding_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    vector_ref TEXT,
    checksum VARCHAR(128),
    status VARCHAR(40) NOT NULL DEFAULT 'ready',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS embedding_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    index_id UUID REFERENCES retrieval_indexes(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    job_type VARCHAR(60) NOT NULL DEFAULT 'index',
    status VARCHAR(40) NOT NULL DEFAULT 'queued',
    provider VARCHAR(80) NOT NULL DEFAULT 'placeholder',
    model VARCHAR(160),
    chunk_count INTEGER NOT NULL DEFAULT 0,
    processed_chunks INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS retrieval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    search_mode VARCHAR(60) NOT NULL DEFAULT 'hybrid',
    status VARCHAR(40) NOT NULL DEFAULT 'completed',
    filters JSONB NOT NULL DEFAULT '{}'::jsonb,
    weights JSONB NOT NULL DEFAULT '{}'::jsonb,
    result_count INTEGER NOT NULL DEFAULT 0,
    latency_ms INTEGER,
    token_budget INTEGER,
    context_tokens INTEGER,
    permission_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS search_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    retrieval_request_id UUID REFERENCES retrieval_requests(id) ON DELETE CASCADE,
    event_type VARCHAR(80) NOT NULL,
    stage VARCHAR(80),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS retrieval_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    metric_name VARCHAR(80) NOT NULL,
    metric_value NUMERIC(14, 3) NOT NULL,
    unit VARCHAR(32) NOT NULL DEFAULT 'count',
    scope VARCHAR(60) NOT NULL DEFAULT 'workspace',
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE SET NULL,
    dimensions JSONB NOT NULL DEFAULT '{}'::jsonb,
    captured_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_retrieval_provider_configs_workspace_type ON retrieval_provider_configs(workspace_id, provider_type, status, priority);
CREATE INDEX IF NOT EXISTS ix_retrieval_indexes_kb_status ON retrieval_indexes(knowledge_base_id, status, last_indexed_at);
CREATE INDEX IF NOT EXISTS ix_retrieval_chunks_document_index ON retrieval_chunks(document_id, chunk_index);
CREATE INDEX IF NOT EXISTS ix_retrieval_chunks_kb_status ON retrieval_chunks(knowledge_base_id, status, language);
CREATE INDEX IF NOT EXISTS ix_embedding_jobs_status ON embedding_jobs(workspace_id, status, created_at);
CREATE INDEX IF NOT EXISTS ix_retrieval_requests_kb_created ON retrieval_requests(knowledge_base_id, created_at);
CREATE INDEX IF NOT EXISTS ix_search_logs_request_stage ON search_logs(retrieval_request_id, stage, created_at);
CREATE INDEX IF NOT EXISTS ix_retrieval_metrics_metric_time ON retrieval_metrics(workspace_id, metric_name, captured_at);
