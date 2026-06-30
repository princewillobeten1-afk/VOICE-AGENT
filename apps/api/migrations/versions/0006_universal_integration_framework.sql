-- VoiceSense Task 010: Universal Integration Framework foundation.

CREATE TABLE IF NOT EXISTS integration_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(80) NOT NULL UNIQUE,
    name VARCHAR(160) NOT NULL,
    description TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_integration_categories_slug ON integration_categories(slug);

ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS slug VARCHAR(120);
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS version VARCHAR(40) NOT NULL DEFAULT '1.0.0';
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS auth_methods JSONB NOT NULL DEFAULT '[]'::jsonb;
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS compatibility JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS documentation_url TEXT;
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS icon_url TEXT;
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS featured BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE external_integrations ADD COLUMN IF NOT EXISTS status VARCHAR(40) NOT NULL DEFAULT 'available';
UPDATE external_integrations SET slug = provider WHERE slug IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_external_integrations_slug ON external_integrations(slug) WHERE slug IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_external_integrations_category ON external_integrations(category);
CREATE INDEX IF NOT EXISTS ix_external_integrations_status ON external_integrations(status);

CREATE TABLE IF NOT EXISTS connector_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_integration_id UUID NOT NULL REFERENCES external_integrations(id) ON DELETE CASCADE,
    connector_key VARCHAR(160) NOT NULL UNIQUE,
    handler_ref VARCHAR(240) NOT NULL,
    interface_version VARCHAR(40) NOT NULL DEFAULT '1',
    auth_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    config_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    rate_limit_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    health_check_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_connector_definitions_external_integration_id ON connector_definitions(external_integration_id);
CREATE INDEX IF NOT EXISTS ix_connector_definitions_connector_key ON connector_definitions(connector_key);
CREATE INDEX IF NOT EXISTS ix_connector_definitions_status ON connector_definitions(status);

ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS connector_definition_id UUID REFERENCES connector_definitions(id) ON DELETE SET NULL;
ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS auth_method VARCHAR(60) NOT NULL DEFAULT 'api_key';
ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS scopes JSONB NOT NULL DEFAULT '[]'::jsonb;
ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS last_validated_at TIMESTAMPTZ;
ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS last_health_status VARCHAR(40);
ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS expires_at TIMESTAMPTZ;
ALTER TABLE connected_accounts ADD COLUMN IF NOT EXISTS disabled_at TIMESTAMPTZ;
CREATE INDEX IF NOT EXISTS ix_connected_accounts_connector_definition_id ON connected_accounts(connector_definition_id);
CREATE INDEX IF NOT EXISTS ix_connected_accounts_integration_status ON connected_accounts(external_integration_id, status);

CREATE TABLE IF NOT EXISTS integration_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    connected_account_id UUID NOT NULL REFERENCES connected_accounts(id) ON DELETE CASCADE,
    auth_method VARCHAR(60) NOT NULL,
    secret_fingerprint VARCHAR(128) NOT NULL,
    secret_ref TEXT NOT NULL,
    secret_provider VARCHAR(80) NOT NULL DEFAULT 'external_secret_manager',
    rotation_version INTEGER NOT NULL DEFAULT 1,
    expires_at TIMESTAMPTZ,
    last_rotated_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_organization_id ON integration_credentials(organization_id);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_workspace_id ON integration_credentials(workspace_id);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_connected_account_id ON integration_credentials(connected_account_id);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_auth_method ON integration_credentials(auth_method);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_secret_fingerprint ON integration_credentials(secret_fingerprint);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_status ON integration_credentials(status);
CREATE INDEX IF NOT EXISTS ix_integration_credentials_account_status ON integration_credentials(connected_account_id, status);

CREATE TABLE IF NOT EXISTS integration_action_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_integration_id UUID NOT NULL REFERENCES external_integrations(id) ON DELETE CASCADE,
    key VARCHAR(160) NOT NULL,
    name VARCHAR(180) NOT NULL,
    description TEXT,
    input_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_integration_action_key UNIQUE (external_integration_id, key)
);
CREATE INDEX IF NOT EXISTS ix_integration_action_definitions_external_integration_id ON integration_action_definitions(external_integration_id);
CREATE INDEX IF NOT EXISTS ix_integration_action_definitions_key ON integration_action_definitions(key);
CREATE INDEX IF NOT EXISTS ix_integration_action_definitions_status ON integration_action_definitions(status);

CREATE TABLE IF NOT EXISTS integration_trigger_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_integration_id UUID NOT NULL REFERENCES external_integrations(id) ON DELETE CASCADE,
    key VARCHAR(160) NOT NULL,
    name VARCHAR(180) NOT NULL,
    description TEXT,
    payload_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    subscription_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_integration_trigger_key UNIQUE (external_integration_id, key)
);
CREATE INDEX IF NOT EXISTS ix_integration_trigger_definitions_external_integration_id ON integration_trigger_definitions(external_integration_id);
CREATE INDEX IF NOT EXISTS ix_integration_trigger_definitions_key ON integration_trigger_definitions(key);
CREATE INDEX IF NOT EXISTS ix_integration_trigger_definitions_status ON integration_trigger_definitions(status);

CREATE TABLE IF NOT EXISTS connection_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    connected_account_id UUID REFERENCES connected_accounts(id) ON DELETE SET NULL,
    event_type VARCHAR(120) NOT NULL,
    status VARCHAR(40) NOT NULL,
    message TEXT,
    latency_ms INTEGER,
    retry_count INTEGER NOT NULL DEFAULT 0,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_connection_logs_organization_id ON connection_logs(organization_id);
CREATE INDEX IF NOT EXISTS ix_connection_logs_workspace_id ON connection_logs(workspace_id);
CREATE INDEX IF NOT EXISTS ix_connection_logs_connected_account_id ON connection_logs(connected_account_id);
CREATE INDEX IF NOT EXISTS ix_connection_logs_event_type ON connection_logs(event_type);
CREATE INDEX IF NOT EXISTS ix_connection_logs_status ON connection_logs(status);
CREATE INDEX IF NOT EXISTS ix_connection_logs_account_created ON connection_logs(connected_account_id, created_at);

CREATE TABLE IF NOT EXISTS integration_health_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    connected_account_id UUID NOT NULL REFERENCES connected_accounts(id) ON DELETE CASCADE,
    status VARCHAR(40) NOT NULL,
    checked_at TIMESTAMPTZ NOT NULL,
    latency_ms INTEGER,
    error_message TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_integration_health_checks_organization_id ON integration_health_checks(organization_id);
CREATE INDEX IF NOT EXISTS ix_integration_health_checks_workspace_id ON integration_health_checks(workspace_id);
CREATE INDEX IF NOT EXISTS ix_integration_health_checks_connected_account_id ON integration_health_checks(connected_account_id);
CREATE INDEX IF NOT EXISTS ix_integration_health_checks_status ON integration_health_checks(status);
CREATE INDEX IF NOT EXISTS ix_health_checks_account_checked ON integration_health_checks(connected_account_id, checked_at);