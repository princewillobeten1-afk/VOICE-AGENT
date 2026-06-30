-- VoiceSense identity foundation
-- PostgreSQL migration for users, organizations, teams, RBAC, sessions, OAuth, invitations, and audit logs.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(160) NOT NULL,
  display_name VARCHAR(160),
  email VARCHAR(320) NOT NULL UNIQUE,
  email_normalized VARCHAR(320) NOT NULL UNIQUE,
  email_verified_at TIMESTAMPTZ,
  avatar_url TEXT,
  timezone VARCHAR(80) NOT NULL DEFAULT 'UTC',
  language VARCHAR(16) NOT NULL DEFAULT 'en',
  password_hash TEXT,
  profile_settings JSONB NOT NULL DEFAULT '{}',
  disabled_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(180) NOT NULL,
  slug VARCHAR(120) NOT NULL UNIQUE,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug VARCHAR(60) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  permissions JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO roles (slug, name, permissions) VALUES
('owner', 'Owner', '["org:read","org:write","org:delete","team:read","team:write","team:delete","invite:create","invite:manage","members:manage","billing:manage","api_keys:manage","audit:read"]'),
('admin', 'Admin', '["org:read","org:write","team:read","team:write","team:delete","invite:create","invite:manage","members:manage","api_keys:manage","audit:read"]'),
('manager', 'Manager', '["org:read","team:read","team:write","invite:create","members:manage"]'),
('developer', 'Developer', '["org:read","team:read","api_keys:manage"]'),
('member', 'Member', '["org:read","team:read"]'),
('billing', 'Billing', '["org:read","billing:manage"]')
ON CONFLICT (slug) DO NOTHING;

CREATE TABLE memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id),
  status VARCHAR(24) NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_membership_org_user UNIQUE (organization_id, user_id)
);

CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name VARCHAR(160) NOT NULL,
  slug VARCHAR(120) NOT NULL,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_team_org_slug UNIQUE (organization_id, slug)
);

CREATE TABLE team_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_team_member UNIQUE (team_id, user_id)
);

CREATE TABLE invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  email VARCHAR(320) NOT NULL,
  role_id UUID NOT NULL REFERENCES roles(id),
  token_hash VARCHAR(128) NOT NULL UNIQUE,
  invited_by_user_id UUID NOT NULL REFERENCES users(id),
  expires_at TIMESTAMPTZ NOT NULL,
  accepted_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  refresh_token_hash VARCHAR(128) NOT NULL UNIQUE,
  user_agent TEXT,
  ip_address INET,
  expires_at TIMESTAMPTZ NOT NULL,
  revoked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE oauth_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider VARCHAR(40) NOT NULL,
  provider_user_id VARCHAR(180) NOT NULL,
  email VARCHAR(320),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_oauth_provider_user UNIQUE (provider, provider_user_id)
);

CREATE TABLE verification_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  purpose VARCHAR(40) NOT NULL,
  token_hash VARCHAR(128) NOT NULL UNIQUE,
  expires_at TIMESTAMPTZ NOT NULL,
  used_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
  actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  event_type VARCHAR(120) NOT NULL,
  target_type VARCHAR(80),
  target_id UUID,
  ip_address INET,
  user_agent TEXT,
  metadata_json JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_users_active_email ON users(email_normalized, deleted_at);
CREATE INDEX ix_memberships_user ON memberships(user_id);
CREATE INDEX ix_memberships_org ON memberships(organization_id);
CREATE INDEX ix_teams_org ON teams(organization_id);
CREATE INDEX ix_team_members_team ON team_members(team_id);
CREATE INDEX ix_team_members_user ON team_members(user_id);
CREATE INDEX ix_invitations_org_email ON invitations(organization_id, email);
CREATE INDEX ix_sessions_user_active ON sessions(user_id, revoked_at, expires_at);
CREATE INDEX ix_oauth_user ON oauth_accounts(user_id);
CREATE INDEX ix_verification_user_purpose ON verification_tokens(user_id, purpose, expires_at);
CREATE INDEX ix_audit_org_event_created ON audit_logs(organization_id, event_type, created_at DESC);