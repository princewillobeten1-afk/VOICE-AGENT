-- VoiceSense Task 009: Notification and event system foundation.

ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS event_version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS source VARCHAR(80) NOT NULL DEFAULT 'platform';
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS correlation_id VARCHAR(120);
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS causation_id UUID;
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(160);
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS status VARCHAR(40) NOT NULL DEFAULT 'published';
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS retry_count INTEGER NOT NULL DEFAULT 0;
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS processed_at TIMESTAMPTZ;
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS error_message TEXT;
ALTER TABLE domain_event_records ADD COLUMN IF NOT EXISTS metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE UNIQUE INDEX IF NOT EXISTS uq_domain_events_idempotency_key ON domain_event_records(idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_events_name_time ON domain_event_records(name, occurred_at);
CREATE INDEX IF NOT EXISTS ix_events_org_status_time ON domain_event_records(organization_id, status, occurred_at);
CREATE INDEX IF NOT EXISTS ix_events_correlation_id ON domain_event_records(correlation_id);
CREATE INDEX IF NOT EXISTS ix_events_causation_id ON domain_event_records(causation_id);

CREATE TABLE IF NOT EXISTS event_subscribers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(160) NOT NULL UNIQUE,
    description TEXT,
    event_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    handler_ref VARCHAR(240) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    max_retries INTEGER NOT NULL DEFAULT 3,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_event_subscribers_status ON event_subscribers(status, deleted_at);
INSERT INTO event_subscribers (name, description, event_types, handler_ref, status, max_retries)
VALUES ('notification-engine', 'Creates notifications from domain events.', '["*"]'::jsonb, 'app.notifications.service.process_event_for_notifications', 'active', 3)
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS event_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES domain_event_records(id) ON DELETE CASCADE,
    subscriber_id UUID REFERENCES event_subscribers(id) ON DELETE SET NULL,
    status VARCHAR(40) NOT NULL,
    processing_time_ms INTEGER,
    retry_count INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_event_logs_event_id ON event_logs(event_id);
CREATE INDEX IF NOT EXISTS ix_event_logs_subscriber_id ON event_logs(subscriber_id);
CREATE INDEX IF NOT EXISTS ix_event_logs_status ON event_logs(status);
CREATE INDEX IF NOT EXISTS ix_event_logs_event_status ON event_logs(event_id, status);

ALTER TABLE notifications ADD COLUMN IF NOT EXISTS event_id UUID REFERENCES domain_event_records(id) ON DELETE SET NULL;
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS category VARCHAR(80) NOT NULL DEFAULT 'system';
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS status VARCHAR(40) NOT NULL DEFAULT 'unread';
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS priority VARCHAR(40) NOT NULL DEFAULT 'normal';
ALTER TABLE notifications ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ;
UPDATE notifications SET status = CASE WHEN read_at IS NULL THEN 'unread' ELSE 'read' END WHERE status IS NULL;

CREATE INDEX IF NOT EXISTS ix_notifications_event_id ON notifications(event_id);
CREATE INDEX IF NOT EXISTS ix_notifications_category ON notifications(category);
CREATE INDEX IF NOT EXISTS ix_notifications_severity ON notifications(severity);
CREATE INDEX IF NOT EXISTS ix_notifications_status ON notifications(status);
CREATE INDEX IF NOT EXISTS ix_notifications_org_user_status ON notifications(organization_id, user_id, status, created_at);
CREATE INDEX IF NOT EXISTS ix_notifications_org_category ON notifications(organization_id, category, created_at);

ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS email_enabled BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS in_app_enabled BOOLEAN NOT NULL DEFAULT true;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS sms_enabled BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS push_enabled BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS webhook_enabled BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS frequency VARCHAR(40) NOT NULL DEFAULT 'instant';
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS quiet_hours JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS category_preferences JSONB NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS team_notifications BOOLEAN NOT NULL DEFAULT true;
ALTER TABLE notification_preferences ADD COLUMN IF NOT EXISTS metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb;
CREATE UNIQUE INDEX IF NOT EXISTS uq_notification_preference_user_org ON notification_preferences(organization_id, user_id);

CREATE TABLE IF NOT EXISTS notification_channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    channel VARCHAR(40) NOT NULL,
    name VARCHAR(160) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'disabled',
    provider VARCHAR(80),
    config_ref TEXT,
    capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_notification_channels_organization_id ON notification_channels(organization_id);
CREATE INDEX IF NOT EXISTS ix_notification_channels_channel ON notification_channels(channel);
CREATE INDEX IF NOT EXISTS ix_notification_channels_status ON notification_channels(status);

CREATE TABLE IF NOT EXISTS notification_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    event_type VARCHAR(120) NOT NULL,
    channel VARCHAR(40) NOT NULL DEFAULT 'in_app',
    category VARCHAR(80) NOT NULL DEFAULT 'system',
    severity VARCHAR(40) NOT NULL DEFAULT 'info',
    title_template VARCHAR(240) NOT NULL,
    body_template TEXT,
    action_url_template TEXT,
    variables JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_notification_template_event_channel UNIQUE (organization_id, event_type, channel)
);

CREATE INDEX IF NOT EXISTS ix_notification_templates_organization_id ON notification_templates(organization_id);
CREATE INDEX IF NOT EXISTS ix_notification_templates_event_type ON notification_templates(event_type);
CREATE INDEX IF NOT EXISTS ix_notification_templates_status ON notification_templates(status);

CREATE TABLE IF NOT EXISTS delivery_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    notification_id UUID REFERENCES notifications(id) ON DELETE CASCADE,
    event_id UUID REFERENCES domain_event_records(id) ON DELETE CASCADE,
    channel VARCHAR(40) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'queued',
    provider VARCHAR(80),
    attempt_number INTEGER NOT NULL DEFAULT 1,
    next_retry_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    failed_at TIMESTAMPTZ,
    latency_ms INTEGER,
    error_message TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_delivery_attempts_organization_id ON delivery_attempts(organization_id);
CREATE INDEX IF NOT EXISTS ix_delivery_attempts_notification_id ON delivery_attempts(notification_id);
CREATE INDEX IF NOT EXISTS ix_delivery_attempts_event_id ON delivery_attempts(event_id);
CREATE INDEX IF NOT EXISTS ix_delivery_attempts_channel ON delivery_attempts(channel);
CREATE INDEX IF NOT EXISTS ix_delivery_attempts_status ON delivery_attempts(status);
CREATE INDEX IF NOT EXISTS ix_delivery_attempts_status_retry ON delivery_attempts(status, next_retry_at);