-- VoiceSense developer platform foundation

ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS environment VARCHAR(40) NOT NULL DEFAULT 'development';
ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS usage_count BIGINT NOT NULL DEFAULT 0;
ALTER TABLE webhook_endpoints ADD COLUMN IF NOT EXISTS retry_policy JSONB NOT NULL DEFAULT '{}';

CREATE TABLE IF NOT EXISTS personal_access_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(180) NOT NULL,
  token_prefix VARCHAR(24) NOT NULL,
  token_hash VARCHAR(128) NOT NULL UNIQUE,
  scopes JSONB NOT NULL DEFAULT '[]',
  expires_at TIMESTAMPTZ,
  last_used_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS oauth_applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name VARCHAR(180) NOT NULL,
  client_id VARCHAR(80) NOT NULL UNIQUE,
  client_secret_hash VARCHAR(128) NOT NULL,
  redirect_uris JSONB NOT NULL DEFAULT '[]',
  allowed_scopes JSONB NOT NULL DEFAULT '[]',
  environment VARCHAR(40) NOT NULL DEFAULT 'development',
  status VARCHAR(40) NOT NULL DEFAULT 'active',
  created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS webhook_deliveries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  webhook_endpoint_id UUID NOT NULL REFERENCES webhook_endpoints(id) ON DELETE CASCADE,
  event_type VARCHAR(120) NOT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'pending',
  attempt INTEGER NOT NULL DEFAULT 1,
  request_id VARCHAR(80),
  response_status_code INTEGER,
  response_time_ms INTEGER,
  error_message TEXT,
  payload JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS api_request_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  api_key_id UUID REFERENCES api_keys(id) ON DELETE SET NULL,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  request_id VARCHAR(80) NOT NULL,
  method VARCHAR(12) NOT NULL,
  path TEXT NOT NULL,
  status_code INTEGER NOT NULL,
  response_time_ms INTEGER NOT NULL,
  ip_address INET,
  error_code VARCHAR(120),
  error_message TEXT,
  metadata_json JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS api_usage_buckets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  bucket_start TIMESTAMPTZ NOT NULL,
  bucket_grain VARCHAR(20) NOT NULL DEFAULT 'day',
  environment VARCHAR(40) NOT NULL DEFAULT 'development',
  total_requests INTEGER NOT NULL DEFAULT 0,
  success_count INTEGER NOT NULL DEFAULT 0,
  error_count INTEGER NOT NULL DEFAULT 0,
  rate_limited_count INTEGER NOT NULL DEFAULT 0,
  avg_latency_ms INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sdk_metadata (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  language VARCHAR(40) NOT NULL,
  package_name VARCHAR(160) NOT NULL,
  latest_version VARCHAR(40),
  status VARCHAR(40) NOT NULL DEFAULT 'planned',
  repository_url TEXT,
  docs_url TEXT,
  metadata_json JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS developer_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  environment VARCHAR(40) NOT NULL DEFAULT 'development',
  default_scopes JSONB NOT NULL DEFAULT '[]',
  webhook_retry_policy JSONB NOT NULL DEFAULT '{}',
  rate_limit_policy JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_api_keys_workspace_env ON api_keys(workspace_id, environment, deleted_at);
CREATE INDEX IF NOT EXISTS ix_pats_user_active ON personal_access_tokens(user_id, revoked_at, deleted_at);
CREATE INDEX IF NOT EXISTS ix_oauth_apps_workspace_status ON oauth_applications(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_webhook_deliveries_endpoint_created ON webhook_deliveries(webhook_endpoint_id, created_at);
CREATE INDEX IF NOT EXISTS ix_api_request_logs_workspace_created ON api_request_logs(workspace_id, created_at);
CREATE INDEX IF NOT EXISTS ix_api_usage_buckets_workspace_bucket ON api_usage_buckets(workspace_id, bucket_grain, bucket_start);
CREATE INDEX IF NOT EXISTS ix_sdk_metadata_language ON sdk_metadata(language);
CREATE INDEX IF NOT EXISTS ix_developer_settings_workspace_env ON developer_settings(workspace_id, environment);