CREATE TABLE IF NOT EXISTS voice_provider_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(160) NOT NULL,
    provider_type VARCHAR(40) NOT NULL,
    provider VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'disabled',
    priority INTEGER NOT NULL DEFAULT 100,
    secret_ref TEXT,
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,
    health_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_voice_provider_setting_name UNIQUE (workspace_id, provider_type, provider, name)
);

CREATE TABLE IF NOT EXISTS voice_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(180) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    language VARCHAR(32) NOT NULL DEFAULT 'en',
    accent VARCHAR(80),
    stt_provider VARCHAR(80) NOT NULL DEFAULT 'placeholder',
    stt_model VARCHAR(120),
    tts_provider VARCHAR(80) NOT NULL DEFAULT 'placeholder',
    tts_model VARCHAR(120),
    voice_id VARCHAR(180),
    speaking_speed VARCHAR(32),
    stability VARCHAR(32),
    emotion VARCHAR(80),
    streaming_mode VARCHAR(40) NOT NULL DEFAULT 'full_duplex',
    audio_format JSONB NOT NULL DEFAULT '{}'::jsonb,
    vad_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    interruption_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_budget JSONB NOT NULL DEFAULT '{}'::jsonb,
    fallback_chain JSONB NOT NULL DEFAULT '[]'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_voice_configuration_workspace_name UNIQUE (workspace_id, name)
);

CREATE TABLE IF NOT EXISTS voice_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    voice_configuration_id UUID REFERENCES voice_configurations(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    channel VARCHAR(40) NOT NULL DEFAULT 'browser',
    direction VARCHAR(40) NOT NULL DEFAULT 'inbound',
    status VARCHAR(40) NOT NULL DEFAULT 'initializing',
    current_speaker VARCHAR(40),
    active_response_id VARCHAR(120),
    interrupt_count INTEGER NOT NULL DEFAULT 0,
    pending_tool_calls JSONB NOT NULL DEFAULT '[]'::jsonb,
    context_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    memory_updates JSONB NOT NULL DEFAULT '[]'::jsonb,
    conversation_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    transport_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    started_at TIMESTAMPTZ,
    last_activity_at TIMESTAMPTZ,
    timeout_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    termination_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_session_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    session_id UUID NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
    metric_name VARCHAR(80) NOT NULL,
    metric_value NUMERIC(12, 3) NOT NULL,
    unit VARCHAR(32) NOT NULL DEFAULT 'ms',
    stage VARCHAR(40),
    provider VARCHAR(80),
    captured_at TIMESTAMPTZ,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_audio_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    session_id UUID NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
    direction VARCHAR(40) NOT NULL,
    codec VARCHAR(40) NOT NULL DEFAULT 'pcm16',
    sample_rate_hz INTEGER NOT NULL DEFAULT 16000,
    channels INTEGER NOT NULL DEFAULT 1,
    chunk_count INTEGER NOT NULL DEFAULT 0,
    duration_ms INTEGER NOT NULL DEFAULT 0,
    byte_count INTEGER NOT NULL DEFAULT 0,
    storage_policy VARCHAR(40) NOT NULL DEFAULT 'metadata_only',
    storage_object_id UUID REFERENCES files(id) ON DELETE SET NULL,
    quality_score VARCHAR(40),
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_stream_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    session_id UUID NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
    event_type VARCHAR(80) NOT NULL,
    sequence_number INTEGER NOT NULL DEFAULT 0,
    source VARCHAR(40) NOT NULL DEFAULT 'client',
    stage VARCHAR(40),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    provider VARCHAR(80),
    trace_id VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_voice_provider_settings_workspace_type ON voice_provider_settings(workspace_id, provider_type, status, priority);
CREATE INDEX IF NOT EXISTS ix_voice_configurations_workspace_status ON voice_configurations(workspace_id, status, deleted_at);
CREATE INDEX IF NOT EXISTS ix_voice_sessions_workspace_status ON voice_sessions(workspace_id, status, last_activity_at);
CREATE INDEX IF NOT EXISTS ix_voice_sessions_agent_status ON voice_sessions(agent_id, status, started_at);
CREATE INDEX IF NOT EXISTS ix_voice_session_metrics_session_name ON voice_session_metrics(session_id, metric_name, captured_at);
CREATE INDEX IF NOT EXISTS ix_voice_audio_metadata_session_direction ON voice_audio_metadata(session_id, direction);
CREATE INDEX IF NOT EXISTS ix_voice_stream_events_session_sequence ON voice_stream_events(session_id, sequence_number);
CREATE INDEX IF NOT EXISTS ix_voice_stream_events_trace ON voice_stream_events(trace_id);