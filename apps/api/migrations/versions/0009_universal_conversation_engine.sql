ALTER TABLE conversations ADD COLUMN IF NOT EXISTS lifecycle_stage VARCHAR(60) NOT NULL DEFAULT 'created';
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS priority VARCHAR(40) NOT NULL DEFAULT 'normal';
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS current_topic VARCHAR(240);
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS active_intent VARCHAR(120);
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS customer_ref VARCHAR(180);
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS external_thread_id VARCHAR(180);
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS handoff_status VARCHAR(40) NOT NULL DEFAULT 'none';
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS summary TEXT;
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL;

CREATE TABLE IF NOT EXISTS conversation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    voice_session_id UUID REFERENCES voice_sessions(id) ON DELETE SET NULL,
    channel VARCHAR(40) NOT NULL,
    adapter VARCHAR(80) NOT NULL DEFAULT 'universal',
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    state_version INTEGER NOT NULL DEFAULT 1,
    current_speaker VARCHAR(40),
    active_turn_id UUID,
    active_intent VARCHAR(120),
    pending_questions JSONB NOT NULL DEFAULT '[]'::jsonb,
    tool_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    workflow_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    memory_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    session_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    recovery_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    started_at TIMESTAMPTZ,
    last_activity_at TIMESTAMPTZ,
    paused_at TIMESTAMPTZ,
    resumed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    end_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_turns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    session_id UUID REFERENCES conversation_sessions(id) ON DELETE SET NULL,
    message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
    sequence_number INTEGER NOT NULL,
    speaker_type VARCHAR(40) NOT NULL,
    turn_type VARCHAR(60) NOT NULL DEFAULT 'message',
    status VARCHAR(40) NOT NULL DEFAULT 'completed',
    content TEXT,
    intent JSONB NOT NULL DEFAULT '{}'::jsonb,
    entities JSONB NOT NULL DEFAULT '[]'::jsonb,
    context_delta JSONB NOT NULL DEFAULT '{}'::jsonb,
    response_plan JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    interrupted BOOLEAN NOT NULL DEFAULT false,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    name VARCHAR(180) NOT NULL,
    goal_type VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    priority INTEGER NOT NULL DEFAULT 100,
    success_criteria JSONB NOT NULL DEFAULT '{}'::jsonb,
    progress JSONB NOT NULL DEFAULT '{}'::jsonb,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_context_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    session_id UUID REFERENCES conversation_sessions(id) ON DELETE SET NULL,
    snapshot_type VARCHAR(80) NOT NULL DEFAULT 'turn',
    token_budget INTEGER,
    sources JSONB NOT NULL DEFAULT '[]'::jsonb,
    prioritized_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    omitted_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    model_limits JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_engine_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    session_id UUID REFERENCES conversation_sessions(id) ON DELETE SET NULL,
    turn_id UUID REFERENCES conversation_turns(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    stage VARCHAR(80),
    sequence_number INTEGER NOT NULL DEFAULT 0,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    latency_ms INTEGER,
    trace_id VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    session_id UUID REFERENCES conversation_sessions(id) ON DELETE SET NULL,
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    turn_count INTEGER NOT NULL DEFAULT 0,
    average_response_time_ms INTEGER,
    completion_status VARCHAR(40) NOT NULL DEFAULT 'unknown',
    escalation_status VARCHAR(40) NOT NULL DEFAULT 'none',
    goal_achievement JSONB NOT NULL DEFAULT '{}'::jsonb,
    sentiment JSONB NOT NULL DEFAULT '{}'::jsonb,
    satisfaction JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_conversations_workspace_status ON conversations(workspace_id, status, started_at);
CREATE INDEX IF NOT EXISTS ix_conversations_customer_ref ON conversations(customer_ref);
CREATE INDEX IF NOT EXISTS ix_conversations_external_thread_id ON conversations(external_thread_id);
CREATE INDEX IF NOT EXISTS ix_conversations_handoff_status ON conversations(handoff_status);
CREATE INDEX IF NOT EXISTS ix_conversation_sessions_conversation_status ON conversation_sessions(conversation_id, status, last_activity_at);
CREATE INDEX IF NOT EXISTS ix_conversation_sessions_workspace_status ON conversation_sessions(workspace_id, status, expires_at);
CREATE INDEX IF NOT EXISTS ix_conversation_turns_conversation_sequence ON conversation_turns(conversation_id, sequence_number);
CREATE INDEX IF NOT EXISTS ix_conversation_turns_session_status ON conversation_turns(session_id, status, created_at);
CREATE INDEX IF NOT EXISTS ix_conversation_goals_conversation_status ON conversation_goals(conversation_id, status, priority);
CREATE INDEX IF NOT EXISTS ix_conversation_context_conversation_created ON conversation_context_snapshots(conversation_id, created_at);
CREATE INDEX IF NOT EXISTS ix_conversation_engine_events_conversation_sequence ON conversation_engine_events(conversation_id, sequence_number);
CREATE INDEX IF NOT EXISTS ix_conversation_engine_events_trace ON conversation_engine_events(trace_id);
CREATE INDEX IF NOT EXISTS ix_conversation_analytics_conversation ON conversation_analytics(conversation_id, completion_status);