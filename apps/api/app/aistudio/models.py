from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class AIStudioPrompt(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_prompts"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_ai_studio_prompt_workspace_slug"),)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(140), index=True)
    category: Mapped[str | None] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    current_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioPromptVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_prompt_versions"
    __table_args__ = (UniqueConstraint("prompt_id", "version_number", name="uq_ai_studio_prompt_version_number"),)
    prompt_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="CASCADE"), index=True)
    agent_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_versions.id", ondelete="SET NULL"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    system_prompt: Mapped[str] = mapped_column(Text)
    developer_prompt: Mapped[str | None] = mapped_column(Text)
    variables: Mapped[dict] = mapped_column(JSONB, default=dict)
    sections: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    guardrails: Mapped[dict] = mapped_column(JSONB, default=dict)
    dynamic_context: Mapped[dict] = mapped_column(JSONB, default=dict)
    model_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    token_estimate: Mapped[int] = mapped_column(Integer, default=0)
    validation_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    release_notes: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class AIStudioPromptTemplate(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_prompt_templates"
    name: Mapped[str] = mapped_column(String(180))
    category: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    description: Mapped[str | None] = mapped_column(Text)
    template_body: Mapped[str] = mapped_column(Text)
    variables: Mapped[dict] = mapped_column(JSONB, default=dict)
    recommended_guardrails: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioPlaygroundRun(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_playground_runs"
    prompt_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="SET NULL"), index=True)
    prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    channel: Mapped[str] = mapped_column(String(40), default="text", index=True)
    input_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    execution_trace: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="completed", index=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[float | None] = mapped_column(Numeric(12, 6))


class AIStudioSimulationScenario(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_simulation_scenarios"
    name: Mapped[str] = mapped_column(String(180))
    scenario_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    prompt_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="SET NULL"), index=True)
    persona: Mapped[dict] = mapped_column(JSONB, default=dict)
    conversation_script: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    assertions: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioEvaluationMetric(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_evaluation_metrics"
    name: Mapped[str] = mapped_column(String(160))
    metric_key: Mapped[str] = mapped_column(String(120), index=True)
    metric_type: Mapped[str] = mapped_column(String(80), index=True)
    scoring_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    weight: Mapped[float] = mapped_column(Numeric(6, 3), default=1)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class AIStudioEvaluationRun(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_evaluation_runs"
    prompt_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="SET NULL"), index=True)
    prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    scenario_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_simulation_scenarios.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    score: Mapped[float | None] = mapped_column(Numeric(6, 3))
    metric_results: Mapped[dict] = mapped_column(JSONB, default=dict)
    regression_summary: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[float | None] = mapped_column(Numeric(12, 6))
class AIStudioTestSuite(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_test_suites"
    name: Mapped[str] = mapped_column(String(180))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    schedule_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    deployment_gate: Mapped[bool] = mapped_column(default=False)


class AIStudioTestCase(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_test_cases"
    suite_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_test_suites.id", ondelete="CASCADE"), index=True)
    scenario_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_simulation_scenarios.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    input_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    expected_outcomes: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    assertions: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class AIStudioTestRun(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_test_runs"
    suite_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_test_suites.id", ondelete="CASCADE"), index=True)
    prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    total_tests: Mapped[int] = mapped_column(Integer, default=0)
    passed_tests: Mapped[int] = mapped_column(Integer, default=0)
    failed_tests: Mapped[int] = mapped_column(Integer, default=0)
    results: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioBenchmark(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_benchmarks"
    name: Mapped[str] = mapped_column(String(180))
    baseline_prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    candidate_prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict)
    comparison_summary: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioExperiment(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_experiments"
    name: Mapped[str] = mapped_column(String(180))
    experiment_type: Mapped[str] = mapped_column(String(80), default="ab_test", index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    variants: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    traffic_allocation: Mapped[dict] = mapped_column(JSONB, default=dict)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict)
    guardrails: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioDeployment(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_deployments"
    prompt_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="CASCADE"), index=True)
    prompt_version_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="CASCADE"), index=True)
    environment: Mapped[str] = mapped_column(String(60), default="staging", index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    approval_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    rollout_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    rollback_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    deployed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class AIStudioComment(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_comments"
    prompt_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="CASCADE"), index=True)
    prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="CASCADE"), index=True)
    parent_comment_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_comments.id", ondelete="CASCADE"), index=True)
    body: Mapped[str] = mapped_column(Text)
    mentions: Mapped[list[str]] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(40), default="open", index=True)


class AIStudioActivityLog(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_activity_logs"
    entity_type: Mapped[str] = mapped_column(String(80), index=True)
    entity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    action: Mapped[str] = mapped_column(String(120), index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioAnalyticsRecord(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_analytics_records"
    prompt_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompts.id", ondelete="SET NULL"), index=True)
    prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    metric_name: Mapped[str] = mapped_column(String(120), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 4), default=0)
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class AIStudioInteractionTimeline(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_interaction_timelines"
    playground_run_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_playground_runs.id", ondelete="CASCADE"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    sequence: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIStudioReplaySession(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ai_studio_replay_sessions"
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    voice_session_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_sessions.id", ondelete="SET NULL"), index=True)
    prompt_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_studio_prompt_versions.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="ready", index=True)
    transcript: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    audio_refs: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    timeline: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    inspection_notes: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_ai_studio_prompts_workspace_status", AIStudioPrompt.workspace_id, AIStudioPrompt.status, AIStudioPrompt.deleted_at)
Index("ix_ai_studio_prompt_versions_prompt_status", AIStudioPromptVersion.prompt_id, AIStudioPromptVersion.status)
Index("ix_ai_studio_templates_workspace_category", AIStudioPromptTemplate.workspace_id, AIStudioPromptTemplate.category, AIStudioPromptTemplate.status)
Index("ix_ai_studio_playground_prompt_created", AIStudioPlaygroundRun.prompt_id, AIStudioPlaygroundRun.created_at)
Index("ix_ai_studio_evaluation_prompt_status", AIStudioEvaluationRun.prompt_version_id, AIStudioEvaluationRun.status)
Index("ix_ai_studio_test_runs_suite_status", AIStudioTestRun.suite_id, AIStudioTestRun.status)
Index("ix_ai_studio_deployments_prompt_env", AIStudioDeployment.prompt_id, AIStudioDeployment.environment, AIStudioDeployment.status)
Index("ix_ai_studio_activity_entity", AIStudioActivityLog.entity_type, AIStudioActivityLog.entity_id, AIStudioActivityLog.created_at)
Index("ix_ai_studio_analytics_prompt_metric", AIStudioAnalyticsRecord.prompt_id, AIStudioAnalyticsRecord.metric_name, AIStudioAnalyticsRecord.captured_at)
Index("ix_ai_studio_timeline_run_sequence", AIStudioInteractionTimeline.playground_run_id, AIStudioInteractionTimeline.sequence)