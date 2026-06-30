from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class AdminDepartment(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "admin_departments"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_admin_department_org_slug"),)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    parent_department_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("admin_departments.id", ondelete="SET NULL"), index=True)
    business_unit: Mapped[str | None] = mapped_column(String(180), index=True)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)


class UserGroup(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "user_groups"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_user_group_org_slug"),)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    attributes: Mapped[dict] = mapped_column(JSONB, default=dict)


class UserGroupMember(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "user_group_members"
    group_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("user_groups.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(80), default="member", index=True)


class CustomRole(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "custom_roles"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_custom_role_org_slug"),)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    permissions: Mapped[list[str]] = mapped_column(JSONB, default=list)
    constraints: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class GovernancePolicy(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "governance_policies"
    name: Mapped[str] = mapped_column(String(180))
    policy_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    enforcement_mode: Mapped[str] = mapped_column(String(40), default="monitor", index=True)
    scope: Mapped[dict] = mapped_column(JSONB, default=dict)
    rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    inherited_from_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("governance_policies.id", ondelete="SET NULL"), index=True)


class ABACPolicy(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "abac_policies"
    name: Mapped[str] = mapped_column(String(180))
    effect: Mapped[str] = mapped_column(String(40), default="allow", index=True)
    resource_type: Mapped[str] = mapped_column(String(80), index=True)
    action: Mapped[str] = mapped_column(String(120), index=True)
    conditions: Mapped[dict] = mapped_column(JSONB, default=dict)
    priority: Mapped[int] = mapped_column(Integer, default=100, index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class SSOConnection(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "sso_connections"
    provider: Mapped[str] = mapped_column(String(80), index=True)
    protocol: Mapped[str] = mapped_column(String(40), default="oidc", index=True)
    name: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    domain: Mapped[str | None] = mapped_column(String(180), index=True)
    issuer_url: Mapped[str | None] = mapped_column(Text)
    metadata_url: Mapped[str | None] = mapped_column(Text)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)


class MFAFactor(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "mfa_factors"
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    factor_type: Mapped[str] = mapped_column(String(60), index=True)
    status: Mapped[str] = mapped_column(String(40), default="enrolled", index=True)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    last_verified_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class TrustedDevice(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "trusted_devices"
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    device_fingerprint: Mapped[str] = mapped_column(String(160), index=True)
    device_type: Mapped[str | None] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="trusted", index=True)
    last_seen_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SecretRecord(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "secret_records"
    name: Mapped[str] = mapped_column(String(180))
    secret_type: Mapped[str] = mapped_column(String(80), index=True)
    provider: Mapped[str] = mapped_column(String(80), default="internal", index=True)
    secret_ref: Mapped[str] = mapped_column(Text)
    rotation_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    last_rotated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SecretVersion(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "secret_versions"
    secret_record_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("secret_records.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    secret_ref: Mapped[str] = mapped_column(Text)
    fingerprint: Mapped[str | None] = mapped_column(String(160), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ComplianceFramework(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "compliance_frameworks"
    framework: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="not_started", index=True)
    readiness_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    controls: Mapped[dict] = mapped_column(JSONB, default=dict)
    evidence_summary: Mapped[dict] = mapped_column(JSONB, default=dict)


class ComplianceEvidence(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "compliance_evidence"
    framework_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_frameworks.id", ondelete="SET NULL"), index=True)
    control_id: Mapped[str] = mapped_column(String(120), index=True)
    evidence_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="collected", index=True)
    file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DataGovernancePolicy(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "data_governance_policies"
    name: Mapped[str] = mapped_column(String(180))
    policy_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    data_classification: Mapped[str | None] = mapped_column(String(80), index=True)
    retention_days: Mapped[int | None] = mapped_column(Integer)
    residency_region: Mapped[str | None] = mapped_column(String(80), index=True)
    legal_hold: Mapped[dict] = mapped_column(JSONB, default=dict)
    rules: Mapped[dict] = mapped_column(JSONB, default=dict)


class EncryptionKeyRecord(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "encryption_key_records"
    key_alias: Mapped[str] = mapped_column(String(180), index=True)
    key_type: Mapped[str] = mapped_column(String(80), default="platform", index=True)
    provider: Mapped[str] = mapped_column(String(80), default="internal", index=True)
    key_ref: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    rotation_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    last_rotated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class SecurityRiskEvent(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "security_risk_events"
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(120), index=True)
    risk_level: Mapped[str] = mapped_column(String(40), default="low", index=True)
    risk_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    status: Mapped[str] = mapped_column(String(40), default="open", index=True)
    signal_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    mitigation_state: Mapped[dict] = mapped_column(JSONB, default=dict)


class SecurityHealthScore(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "security_health_scores"
    score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    grade: Mapped[str] = mapped_column(String(8), default="C", index=True)
    factors: Mapped[dict] = mapped_column(JSONB, default=dict)
    recommendations: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


class GovernanceGraphSnapshot(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "governance_graph_snapshots"
    snapshot_type: Mapped[str] = mapped_column(String(80), default="organization", index=True)
    node_count: Mapped[int] = mapped_column(Integer, default=0)
    edge_count: Mapped[int] = mapped_column(Integer, default=0)
    graph_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_admin_departments_org_slug", AdminDepartment.organization_id, AdminDepartment.slug, AdminDepartment.deleted_at)
Index("ix_user_groups_org_slug", UserGroup.organization_id, UserGroup.slug, UserGroup.deleted_at)
Index("ix_custom_roles_org_status", CustomRole.organization_id, CustomRole.status, CustomRole.deleted_at)
Index("ix_governance_policies_workspace_type", GovernancePolicy.workspace_id, GovernancePolicy.policy_type, GovernancePolicy.status)
Index("ix_abac_policies_resource_action", ABACPolicy.resource_type, ABACPolicy.action, ABACPolicy.status, ABACPolicy.priority)
Index("ix_sso_connections_org_provider", SSOConnection.organization_id, SSOConnection.provider, SSOConnection.status)
Index("ix_mfa_factors_user_status", MFAFactor.user_id, MFAFactor.status)
Index("ix_trusted_devices_user_status", TrustedDevice.user_id, TrustedDevice.status, TrustedDevice.last_seen_at)
Index("ix_secret_records_workspace_type", SecretRecord.workspace_id, SecretRecord.secret_type, SecretRecord.status)
Index("ix_secret_versions_record_version", SecretVersion.secret_record_id, SecretVersion.version)
Index("ix_compliance_frameworks_org_status", ComplianceFramework.organization_id, ComplianceFramework.framework, ComplianceFramework.status)
Index("ix_data_governance_workspace_type", DataGovernancePolicy.workspace_id, DataGovernancePolicy.policy_type, DataGovernancePolicy.status)
Index("ix_security_risk_events_workspace_level", SecurityRiskEvent.workspace_id, SecurityRiskEvent.risk_level, SecurityRiskEvent.status)
Index("ix_security_health_scores_org_captured", SecurityHealthScore.organization_id, SecurityHealthScore.captured_at)
