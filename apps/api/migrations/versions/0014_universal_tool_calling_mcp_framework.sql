CREATE TABLE IF NOT EXISTS tool_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(140) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_tool_category_workspace_slug UNIQUE (workspace_id, slug)
);

CREATE TABLE IF NOT EXISTS tool_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    category_id UUID REFERENCES tool_categories(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    slug VARCHAR(140) NOT NULL,
    description TEXT,
    category VARCHAR(80) NOT NULL,
    provider_type VARCHAR(80) NOT NULL DEFAULT 'internal',
    runtime_type VARCHAR(80) NOT NULL DEFAULT 'simulated',
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    version VARCHAR(40) NOT NULL DEFAULT '0.1.0',
    input_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    auth_requirements JSONB NOT NULL DEFAULT '{}'::jsonb,
    permission_requirements JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    timeout_ms INTEGER NOT NULL DEFAULT 30000,
    cost_hint JSONB NOT NULL DEFAULT '{}'::jsonb,
    health_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_tool_definition_workspace_slug UNIQUE (workspace_id, slug)
);

CREATE TABLE IF NOT EXISTS tool_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES tool_definitions(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    version VARCHAR(40) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    change_summary TEXT,
    input_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    runtime_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_tool_version UNIQUE (tool_id, version)
);

CREATE TABLE IF NOT EXISTS tool_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES tool_definitions(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    principal_type VARCHAR(60) NOT NULL,
    principal_id UUID,
    action VARCHAR(60) NOT NULL DEFAULT 'execute',
    effect VARCHAR(20) NOT NULL DEFAULT 'allow',
    conditions JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS tool_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tool_definitions(id) ON DELETE CASCADE,
    connected_account_id UUID REFERENCES connected_accounts(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(160) NOT NULL,
    auth_type VARCHAR(60) NOT NULL,
    secret_ref TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
    expires_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS tool_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES tool_definitions(id) ON DELETE CASCADE,
    tool_version_id UUID REFERENCES tool_versions(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    workflow_run_id UUID REFERENCES workflow_runs(id) ON DELETE SET NULL,
    chain_id UUID,
    requested_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'queued',
    execution_mode VARCHAR(60) NOT NULL DEFAULT 'single',
    input_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    validation_result JSONB NOT NULL DEFAULT '{}'::jsonb,
    permission_result JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_count INTEGER NOT NULL DEFAULT 0,
    latency_ms INTEGER,
    cost_estimate JSONB NOT NULL DEFAULT '{}'::jsonb,
    error_code VARCHAR(80),
    error_message TEXT,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tool_execution_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    execution_id UUID NOT NULL REFERENCES tool_executions(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    stage VARCHAR(80),
    level VARCHAR(40) NOT NULL DEFAULT 'info',
    message TEXT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tool_health_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tool_definitions(id) ON DELETE CASCADE,
    metric_name VARCHAR(80) NOT NULL,
    metric_value NUMERIC(14, 3) NOT NULL,
    unit VARCHAR(32) NOT NULL DEFAULT 'count',
    dimensions JSONB NOT NULL DEFAULT '{}'::jsonb,
    captured_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS mcp_server_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    slug VARCHAR(140) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'disabled',
    transport_type VARCHAR(60) NOT NULL DEFAULT 'stdio',
    endpoint_ref TEXT,
    auth_requirements JSONB NOT NULL DEFAULT '{}'::jsonb,
    capabilities JSONB NOT NULL DEFAULT '{}'::jsonb,
    session_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    resource_discovery JSONB NOT NULL DEFAULT '{}'::jsonb,
    prompt_discovery JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_tool_definitions_workspace_status ON tool_definitions(workspace_id, status, category);
CREATE INDEX IF NOT EXISTS ix_tool_executions_tool_status ON tool_executions(tool_id, status, created_at);
CREATE INDEX IF NOT EXISTS ix_tool_executions_workspace_status ON tool_executions(workspace_id, status, created_at);
CREATE INDEX IF NOT EXISTS ix_tool_logs_execution_stage ON tool_execution_logs(execution_id, stage, created_at);
CREATE INDEX IF NOT EXISTS ix_tool_health_metric_time ON tool_health_metrics(workspace_id, metric_name, captured_at);
CREATE INDEX IF NOT EXISTS ix_mcp_servers_workspace_status ON mcp_server_definitions(workspace_id, status, transport_type);