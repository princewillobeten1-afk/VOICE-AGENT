ALTER TABLE workflows ALTER COLUMN project_id DROP NOT NULL;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS category VARCHAR(80);
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS trigger_type VARCHAR(80) NOT NULL DEFAULT 'manual';
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS execution_mode VARCHAR(60) NOT NULL DEFAULT 'async';
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS current_version_id UUID;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS settings JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS canvas_state JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS published_at TIMESTAMPTZ;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS last_run_at TIMESTAMPTZ;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS run_count INTEGER NOT NULL DEFAULT 0;
ALTER TABLE workflows ADD COLUMN IF NOT EXISTS failure_count INTEGER NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS workflow_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    version_number INTEGER NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    change_summary TEXT,
    definition JSONB NOT NULL DEFAULT '{}'::jsonb,
    canvas_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    validation_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    published_at TIMESTAMPTZ,
    rolled_back_from_version_id UUID REFERENCES workflow_versions(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_workflow_version_number UNIQUE (workflow_id, version_number)
);

ALTER TABLE workflows ADD CONSTRAINT fk_workflows_current_version FOREIGN KEY (current_version_id) REFERENCES workflow_versions(id) ON DELETE SET NULL;

CREATE TABLE IF NOT EXISTS workflow_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    version_id UUID REFERENCES workflow_versions(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    node_key VARCHAR(120) NOT NULL,
    node_type VARCHAR(100) NOT NULL,
    label VARCHAR(180) NOT NULL,
    position JSONB NOT NULL DEFAULT '{}'::jsonb,
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    input_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    timeout_seconds INTEGER,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS workflow_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    version_id UUID REFERENCES workflow_versions(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    source_node_key VARCHAR(120) NOT NULL,
    target_node_key VARCHAR(120) NOT NULL,
    source_handle VARCHAR(80),
    target_handle VARCHAR(80),
    condition_expression TEXT,
    label VARCHAR(140),
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS version_id UUID REFERENCES workflow_versions(id) ON DELETE SET NULL;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS agent_id UUID REFERENCES agents(id) ON DELETE SET NULL;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS trigger_type VARCHAR(80) NOT NULL DEFAULT 'manual';
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS trigger_ref TEXT;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS current_node_key VARCHAR(120);
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS execution_mode VARCHAR(60) NOT NULL DEFAULT 'async';
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS paused_at TIMESTAMPTZ;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS resumed_at TIMESTAMPTZ;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS next_run_at TIMESTAMPTZ;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS retry_count INTEGER NOT NULL DEFAULT 0;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS duration_ms INTEGER;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS variables JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE workflow_runs ADD COLUMN IF NOT EXISTS execution_state JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE TABLE IF NOT EXISTS workflow_execution_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    workflow_run_id UUID NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    node_key VARCHAR(120),
    node_type VARCHAR(100),
    event_type VARCHAR(100) NOT NULL,
    level VARCHAR(40) NOT NULL DEFAULT 'info',
    message TEXT,
    input_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    retry_count INTEGER NOT NULL DEFAULT 0,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS workflow_variables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(120) NOT NULL,
    scope VARCHAR(60) NOT NULL DEFAULT 'workflow',
    value_type VARCHAR(60) NOT NULL DEFAULT 'string',
    value_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    secret_ref TEXT,
    is_secret BOOLEAN NOT NULL DEFAULT false,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS workflow_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    slug VARCHAR(140) NOT NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT,
    difficulty VARCHAR(40) NOT NULL DEFAULT 'beginner',
    definition JSONB NOT NULL DEFAULT '{}'::jsonb,
    canvas_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    usage_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS workflow_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(160) NOT NULL,
    schedule_type VARCHAR(60) NOT NULL DEFAULT 'cron',
    cron_expression VARCHAR(120),
    timezone VARCHAR(80) NOT NULL DEFAULT 'UTC',
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    next_run_at TIMESTAMPTZ,
    last_run_at TIMESTAMPTZ,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS workflow_approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    workflow_run_id UUID REFERENCES workflow_runs(id) ON DELETE CASCADE,
    node_key VARCHAR(120),
    assignee_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'pending',
    title VARCHAR(180) NOT NULL,
    description TEXT,
    decision VARCHAR(40),
    comments JSONB NOT NULL DEFAULT '[]'::jsonb,
    due_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_workflows_workspace_status ON workflows(workspace_id, status, category, deleted_at);
CREATE INDEX IF NOT EXISTS ix_workflow_versions_workflow_status ON workflow_versions(workflow_id, status, version_number);
CREATE INDEX IF NOT EXISTS ix_workflow_nodes_workflow_type ON workflow_nodes(workflow_id, node_type, status);
CREATE INDEX IF NOT EXISTS ix_workflow_connections_workflow_source ON workflow_connections(workflow_id, source_node_key, target_node_key);
CREATE INDEX IF NOT EXISTS ix_workflow_runs_workspace_status ON workflow_runs(workspace_id, status, started_at);
CREATE INDEX IF NOT EXISTS ix_workflow_execution_logs_run_event ON workflow_execution_logs(workflow_run_id, event_type, created_at);
CREATE INDEX IF NOT EXISTS ix_workflow_variables_scope_name ON workflow_variables(workspace_id, workflow_id, scope, name);
CREATE INDEX IF NOT EXISTS ix_workflow_templates_category_status ON workflow_templates(workspace_id, category, status);
CREATE INDEX IF NOT EXISTS ix_workflow_schedules_next_run ON workflow_schedules(workspace_id, status, next_run_at);
CREATE INDEX IF NOT EXISTS ix_workflow_approvals_status ON workflow_approval_requests(workspace_id, status, due_at);