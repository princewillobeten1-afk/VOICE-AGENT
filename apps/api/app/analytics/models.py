from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class UsageRecord(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "usage_records"
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    metric: Mapped[str] = mapped_column(String(80), index=True)
    quantity: Mapped[int] = mapped_column(BigInteger)
    unit: Mapped[str] = mapped_column(String(40))
    occurred_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class AnalyticsEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "analytics_events"
    actor_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    source: Mapped[str] = mapped_column(String(80))
    occurred_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    properties: Mapped[dict] = mapped_column(JSONB, default=dict)


class MetricSnapshot(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "metric_snapshots"
    __table_args__ = (UniqueConstraint("workspace_id", "metric", "period", "bucket_date", name="uq_metric_snapshot_bucket"),)
    metric: Mapped[str] = mapped_column(String(100))
    period: Mapped[str] = mapped_column(String(20))
    bucket_date: Mapped[str] = mapped_column(Date)
    value: Mapped[float] = mapped_column(Numeric(18, 6))
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)


class OpsDashboard(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_dashboards"
    name: Mapped[str] = mapped_column(String(180))
    scope: Mapped[str] = mapped_column(String(60), default="workspace", index=True)
    owner_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    layout: Mapped[dict] = mapped_column(JSONB, default=dict)
    filters: Mapped[dict] = mapped_column(JSONB, default=dict)
    widgets: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class OpsMetric(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_metrics"
    metric_name: Mapped[str] = mapped_column(String(120), index=True)
    metric_family: Mapped[str] = mapped_column(String(80), index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80), index=True)
    entity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    value: Mapped[float] = mapped_column(Numeric(18, 6))
    unit: Mapped[str] = mapped_column(String(40), default="count")
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)


class OpsAlert(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_alerts"
    name: Mapped[str] = mapped_column(String(180))
    alert_type: Mapped[str] = mapped_column(String(80), index=True)
    severity: Mapped[str] = mapped_column(String(40), default="warning", index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    condition: Mapped[dict] = mapped_column(JSONB, default=dict)
    channels: Mapped[list[str]] = mapped_column(JSONB, default=list)
    last_triggered_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class OpsAlertEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_alert_events"
    alert_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ops_alerts.id", ondelete="SET NULL"), index=True)
    severity: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(40), default="open", index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(80), index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80), index=True)
    entity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    resolved_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class OpsHealthReport(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_health_reports"
    component: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    score: Mapped[int] = mapped_column(Integer, default=100)
    checks: Mapped[dict] = mapped_column(JSONB, default=dict)
    incidents: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    measured_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)


class OpsCostRecord(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_cost_records"
    cost_type: Mapped[str] = mapped_column(String(80), index=True)
    provider: Mapped[str | None] = mapped_column(String(80), index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80), index=True)
    entity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 6))
    currency: Mapped[str] = mapped_column(String(12), default="USD")
    quantity: Mapped[float | None] = mapped_column(Numeric(18, 6))
    unit: Mapped[str | None] = mapped_column(String(40))
    occurred_at: Mapped[str] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class OpsEvaluationResult(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "ops_evaluation_results"
    agent_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), index=True)
    conversation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    evaluation_type: Mapped[str] = mapped_column(String(80), index=True)
    score: Mapped[float | None] = mapped_column(Numeric(8, 3))
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    evaluator: Mapped[str] = mapped_column(String(80), default="framework")
    criteria: Mapped[dict] = mapped_column(JSONB, default=dict)
    result: Mapped[dict] = mapped_column(JSONB, default=dict)
    reviewed_by_user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    evaluated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_usage_records_workspace_metric_time", UsageRecord.workspace_id, UsageRecord.metric, UsageRecord.occurred_at)
Index("ix_analytics_events_workspace_name_time", AnalyticsEvent.workspace_id, AnalyticsEvent.name, AnalyticsEvent.occurred_at)
Index("ix_ops_metrics_workspace_family_time", OpsMetric.workspace_id, OpsMetric.metric_family, OpsMetric.captured_at)
Index("ix_ops_alerts_workspace_status", OpsAlert.workspace_id, OpsAlert.status, OpsAlert.severity)
Index("ix_ops_alert_events_workspace_status", OpsAlertEvent.workspace_id, OpsAlertEvent.status, OpsAlertEvent.severity)
Index("ix_ops_health_component_time", OpsHealthReport.workspace_id, OpsHealthReport.component, OpsHealthReport.measured_at)
Index("ix_ops_cost_records_type_time", OpsCostRecord.workspace_id, OpsCostRecord.cost_type, OpsCostRecord.occurred_at)
Index("ix_ops_evaluations_agent_type", OpsEvaluationResult.workspace_id, OpsEvaluationResult.agent_id, OpsEvaluationResult.evaluation_type)
