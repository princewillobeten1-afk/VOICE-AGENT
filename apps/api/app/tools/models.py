from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class ToolCategory(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_categories"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_tool_category_workspace_slug"),)
    name: Mapped[str] = mapped_column(String(140))
    slug: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ToolDefinition(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_definitions"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_tool_definition_workspace_slug"),)
    category_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_categories.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(140), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80), index=True)
    provider_type: Mapped[str] = mapped_column(String(80), default="internal", index=True)
    runtime_type: Mapped[str] = mapped_column(String(80), default="simulated")
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    version: Mapped[str] = mapped_column(String(40), default="0.1.0")
    input_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    auth_requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    permission_requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    timeout_ms: Mapped[int] = mapped_column(Integer, default=30000)
    cost_hint: Mapped[dict] = mapped_column(JSONB, default=dict)
    health_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ToolVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_versions"
    __table_args__ = (UniqueConstraint("tool_id", "version", name="uq_tool_version"),)
    tool_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_definitions.id", ondelete="CASCADE"), index=True)
    version: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    change_summary: Mapped[str | None] = mapped_column(Text)
    input_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    runtime_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class ToolPermission(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_permissions"
    tool_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_definitions.id", ondelete="CASCADE"), index=True)
    principal_type: Mapped[str] = mapped_column(String(60), index=True)
    principal_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    action: Mapped[str] = mapped_column(String(60), default="execute", index=True)
    effect: Mapped[str] = mapped_column(String(20), default="allow", index=True)
    conditions: Mapped[dict] = mapped_column(JSONB, default=dict)


class ToolCredential(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_credentials"
    tool_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_definitions.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    auth_type: Mapped[str] = mapped_column(String(60), index=True)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    connected_account_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connected_accounts.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ToolExecution(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_executions"
    tool_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_definitions.id", ondelete="CASCADE"), index=True)
    tool_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_versions.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    workflow_run_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id", ondelete="SET NULL"), index=True)
    chain_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    requested_by_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    execution_mode: Mapped[str] = mapped_column(String(60), default="single")
    input_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    validation_result: Mapped[dict] = mapped_column(JSONB, default=dict)
    permission_result: Mapped[dict] = mapped_column(JSONB, default=dict)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost_estimate: Mapped[dict] = mapped_column(JSONB, default=dict)
    error_code: Mapped[str | None] = mapped_column(String(80))
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class ToolExecutionLog(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_execution_logs"
    execution_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_executions.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    stage: Mapped[str | None] = mapped_column(String(80), index=True)
    level: Mapped[str] = mapped_column(String(40), default="info", index=True)
    message: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)


class ToolHealthMetric(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "tool_health_metrics"
    tool_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_definitions.id", ondelete="CASCADE"), index=True)
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(14, 3))
    unit: Mapped[str] = mapped_column(String(32), default="count")
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class McpServerDefinition(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "mcp_server_definitions"
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(140), index=True)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    transport_type: Mapped[str] = mapped_column(String(60), default="stdio")
    endpoint_ref: Mapped[str | None] = mapped_column(Text)
    auth_requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    capabilities: Mapped[dict] = mapped_column(JSONB, default=dict)
    session_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    resource_discovery: Mapped[dict] = mapped_column(JSONB, default=dict)
    prompt_discovery: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_tool_definitions_workspace_status", ToolDefinition.workspace_id, ToolDefinition.status, ToolDefinition.category)
Index("ix_tool_executions_tool_status", ToolExecution.tool_id, ToolExecution.status, ToolExecution.created_at)
Index("ix_tool_executions_workspace_status", ToolExecution.workspace_id, ToolExecution.status, ToolExecution.created_at)
Index("ix_tool_logs_execution_stage", ToolExecutionLog.execution_id, ToolExecutionLog.stage, ToolExecutionLog.created_at)
Index("ix_tool_health_metric_time", ToolHealthMetric.workspace_id, ToolHealthMetric.metric_name, ToolHealthMetric.captured_at)
Index("ix_mcp_servers_workspace_status", McpServerDefinition.workspace_id, McpServerDefinition.status, McpServerDefinition.transport_type)
