-- VoiceSense Task 012: AI Employee Builder foundation.

CREATE TABLE IF NOT EXISTS agent_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(120) NOT NULL UNIQUE,
    name VARCHAR(180) NOT NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT,
    role VARCHAR(160) NOT NULL,
    department VARCHAR(120),
    default_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    recommended_tools JSONB NOT NULL DEFAULT '[]'::jsonb,
    recommended_channels JSONB NOT NULL DEFAULT '[]'::jsonb,
    featured BOOLEAN NOT NULL DEFAULT false,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_agent_templates_slug ON agent_templates(slug);
CREATE INDEX IF NOT EXISTS ix_agent_templates_category ON agent_templates(category);
CREATE INDEX IF NOT EXISTS ix_agent_templates_status ON agent_templates(status);

ALTER TABLE agents ADD COLUMN IF NOT EXISTS display_name VARCHAR(180);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS avatar_url TEXT;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS role VARCHAR(160);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS department VARCHAR(120);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS category VARCHAR(80);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS lifecycle_stage VARCHAR(40) NOT NULL DEFAULT 'builder';
ALTER TABLE agents ADD COLUMN IF NOT EXISTS template_id UUID REFERENCES agent_templates(id) ON DELETE SET NULL;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS last_published_at TIMESTAMPTZ;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ;
UPDATE agents SET display_name = name WHERE display_name IS NULL;
CREATE INDEX IF NOT EXISTS ix_agents_workspace_status ON agents(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_agents_workspace_category ON agents(workspace_id, category, deleted_at);
CREATE INDEX IF NOT EXISTS ix_agents_role ON agents(role);
CREATE INDEX IF NOT EXISTS ix_agents_department ON agents(department);
CREATE INDEX IF NOT EXISTS ix_agents_category ON agents(category);
CREATE INDEX IF NOT EXISTS ix_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS ix_agents_template_id ON agents(template_id);

ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS change_summary TEXT;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS personality_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS voice_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS knowledge_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS memory_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS channel_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS collaboration_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS workflow_config JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE agent_versions ADD COLUMN IF NOT EXISTS validation_state JSONB NOT NULL DEFAULT '{}'::jsonb;
CREATE INDEX IF NOT EXISTS ix_agent_versions_agent_status ON agent_versions(agent_id, status);

CREATE TABLE IF NOT EXISTS agent_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    active_version_id UUID REFERENCES agent_versions(id) ON DELETE SET NULL,
    builder_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    readiness JSONB NOT NULL DEFAULT '{}'::jsonb,
    playground_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_agent_configuration_agent UNIQUE (agent_id)
);
CREATE INDEX IF NOT EXISTS ix_agent_configurations_organization_id ON agent_configurations(organization_id);
CREATE INDEX IF NOT EXISTS ix_agent_configurations_workspace_id ON agent_configurations(workspace_id);
CREATE INDEX IF NOT EXISTS ix_agent_configurations_agent_id ON agent_configurations(agent_id);
CREATE INDEX IF NOT EXISTS ix_agent_configurations_active_version_id ON agent_configurations(active_version_id);
CREATE INDEX IF NOT EXISTS ix_agent_configurations_agent ON agent_configurations(agent_id, active_version_id);

CREATE TABLE IF NOT EXISTS agent_drafts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    name VARCHAR(180) NOT NULL,
    step VARCHAR(80) NOT NULL DEFAULT 'identity',
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_agent_drafts_organization_id ON agent_drafts(organization_id);
CREATE INDEX IF NOT EXISTS ix_agent_drafts_workspace_id ON agent_drafts(workspace_id);
CREATE INDEX IF NOT EXISTS ix_agent_drafts_agent_id ON agent_drafts(agent_id);
CREATE INDEX IF NOT EXISTS ix_agent_drafts_status ON agent_drafts(status);
CREATE INDEX IF NOT EXISTS ix_agent_drafts_agent_status ON agent_drafts(agent_id, status);

CREATE TABLE IF NOT EXISTS agent_publishing_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    version_id UUID REFERENCES agent_versions(id) ON DELETE SET NULL,
    action VARCHAR(80) NOT NULL,
    from_status VARCHAR(40),
    to_status VARCHAR(40),
    change_summary TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_agent_publishing_history_organization_id ON agent_publishing_history(organization_id);
CREATE INDEX IF NOT EXISTS ix_agent_publishing_history_workspace_id ON agent_publishing_history(workspace_id);
CREATE INDEX IF NOT EXISTS ix_agent_publishing_history_agent_id ON agent_publishing_history(agent_id);
CREATE INDEX IF NOT EXISTS ix_agent_publishing_history_version_id ON agent_publishing_history(version_id);
CREATE INDEX IF NOT EXISTS ix_agent_publishing_history_action ON agent_publishing_history(action);
CREATE INDEX IF NOT EXISTS ix_agent_publishing_history_agent_created ON agent_publishing_history(agent_id, created_at);