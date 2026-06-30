from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class Workflow(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflows"
    __table_args__ = (UniqueConstraint("project_id", "slug", name="uq_workflow_project_slug"),)
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    category: Mapped[str | None] = mapped_column(String(80), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    trigger_type: Mapped[str] = mapped_column(String(80), default="manual", index=True)
    execution_mode: Mapped[str] = mapped_column(String(60), default="async")
    current_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_versions.id", ondelete="SET NULL"), index=True)
    definition: Mapped[dict] = mapped_column(JSONB, default=dict)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    canvas_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    last_run_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    run_count: Mapped[int] = mapped_column(Integer, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)


class WorkflowVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_versions"
    __table_args__ = (UniqueConstraint("workflow_id", "version_number", name="uq_workflow_version_number"),)
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    change_summary: Mapped[str | None] = mapped_column(Text)
    definition: Mapped[dict] = mapped_column(JSONB, default=dict)
    canvas_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    validation_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    published_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    rolled_back_from_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_versions.id", ondelete="SET NULL"), index=True)


class WorkflowNode(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_nodes"
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_versions.id", ondelete="CASCADE"), index=True)
    node_key: Mapped[str] = mapped_column(String(120), index=True)
    node_type: Mapped[str] = mapped_column(String(100), index=True)
    label: Mapped[str] = mapped_column(String(180))
    position: Mapped[dict] = mapped_column(JSONB, default=dict)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    input_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    timeout_seconds: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class WorkflowConnection(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_connections"
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_versions.id", ondelete="CASCADE"), index=True)
    source_node_key: Mapped[str] = mapped_column(String(120), index=True)
    target_node_key: Mapped[str] = mapped_column(String(120), index=True)
    source_handle: Mapped[str | None] = mapped_column(String(80))
    target_handle: Mapped[str | None] = mapped_column(String(80))
    condition_expression: Mapped[str | None] = mapped_column(Text)
    label: Mapped[str | None] = mapped_column(String(140))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class WorkflowRun(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_runs"
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_versions.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    trigger_type: Mapped[str] = mapped_column(String(80), default="manual", index=True)
    trigger_ref: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    current_node_key: Mapped[str | None] = mapped_column(String(120), index=True)
    execution_mode: Mapped[str] = mapped_column(String(60), default="async")
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    paused_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    resumed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    next_run_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    input_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    variables: Mapped[dict] = mapped_column(JSONB, default=dict)
    execution_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    error_message: Mapped[str | None] = mapped_column(Text)


class WorkflowExecutionLog(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_execution_logs"
    workflow_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    workflow_run_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id", ondelete="CASCADE"), index=True)
    node_key: Mapped[str | None] = mapped_column(String(120), index=True)
    node_type: Mapped[str | None] = mapped_column(String(100), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    level: Mapped[str] = mapped_column(String(40), default="info", index=True)
    message: Mapped[str | None] = mapped_column(Text)
    input_snapshot: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_snapshot: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class WorkflowVariable(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_variables"
    workflow_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    scope: Mapped[str] = mapped_column(String(60), default="workflow", index=True)
    value_type: Mapped[str] = mapped_column(String(60), default="string")
    value_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    is_secret: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)


class WorkflowTemplate(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_templates"
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(140), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(40), default="beginner")
    definition: Mapped[dict] = mapped_column(JSONB, default=dict)
    canvas_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class WorkflowSchedule(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_schedules"
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    schedule_type: Mapped[str] = mapped_column(String(60), default="cron", index=True)
    cron_expression: Mapped[str | None] = mapped_column(String(120))
    timezone: Mapped[str] = mapped_column(String(80), default="UTC")
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    next_run_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    last_run_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class WorkflowApprovalRequest(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "workflow_approval_requests"
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    workflow_run_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id", ondelete="CASCADE"), index=True)
    node_key: Mapped[str | None] = mapped_column(String(120), index=True)
    assignee_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str | None] = mapped_column(Text)
    decision: Mapped[str | None] = mapped_column(String(40))
    comments: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    due_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    resolved_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class AutomationEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "automation_events"
    workflow_run_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(100), index=True)
    source: Mapped[str] = mapped_column(String(80))
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_workflows_project_status", Workflow.project_id, Workflow.status, Workflow.deleted_at)
Index("ix_workflows_workspace_status", Workflow.workspace_id, Workflow.status, Workflow.category, Workflow.deleted_at)
Index("ix_workflow_versions_workflow_status", WorkflowVersion.workflow_id, WorkflowVersion.status, WorkflowVersion.version_number)
Index("ix_workflow_nodes_workflow_type", WorkflowNode.workflow_id, WorkflowNode.node_type, WorkflowNode.status)
Index("ix_workflow_connections_workflow_source", WorkflowConnection.workflow_id, WorkflowConnection.source_node_key, WorkflowConnection.target_node_key)
Index("ix_workflow_runs_workflow_status", WorkflowRun.workflow_id, WorkflowRun.status, WorkflowRun.created_at)
Index("ix_workflow_runs_workspace_status", WorkflowRun.workspace_id, WorkflowRun.status, WorkflowRun.started_at)
Index("ix_workflow_execution_logs_run_event", WorkflowExecutionLog.workflow_run_id, WorkflowExecutionLog.event_type, WorkflowExecutionLog.created_at)
Index("ix_workflow_variables_scope_name", WorkflowVariable.workspace_id, WorkflowVariable.workflow_id, WorkflowVariable.scope, WorkflowVariable.name)
Index("ix_workflow_templates_category_status", WorkflowTemplate.workspace_id, WorkflowTemplate.category, WorkflowTemplate.status)
Index("ix_workflow_schedules_next_run", WorkflowSchedule.workspace_id, WorkflowSchedule.status, WorkflowSchedule.next_run_at)
Index("ix_workflow_approvals_status", WorkflowApprovalRequest.workspace_id, WorkflowApprovalRequest.status, WorkflowApprovalRequest.due_at)
