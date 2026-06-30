from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class PolicyCreate(BaseModel):
    workspace_id: UUID | None = None
    name: str
    policy_type: str
    enforcement_mode: str = "monitor"
    scope: dict = Field(default_factory=dict)
    rules: dict = Field(default_factory=dict)


class PolicyOut(BaseModel):
    id: UUID
    workspace_id: UUID | None
    name: str
    policy_type: str
    status: str
    enforcement_mode: str
    scope: dict
    rules: dict
    created_at: datetime


class ABACPolicyCreate(BaseModel):
    workspace_id: UUID | None = None
    name: str
    effect: str = "allow"
    resource_type: str
    action: str
    conditions: dict = Field(default_factory=dict)
    priority: int = 100


class ABACPolicyOut(BaseModel):
    id: UUID
    workspace_id: UUID | None
    name: str
    effect: str
    resource_type: str
    action: str
    conditions: dict
    priority: int
    status: str
    created_at: datetime


class SSOConnectionCreate(BaseModel):
    provider: str
    protocol: str = "oidc"
    name: str
    domain: str | None = None
    issuer_url: str | None = None
    metadata_url: str | None = None
    secret_ref: str | None = None
    config: dict = Field(default_factory=dict)


class SSOConnectionOut(BaseModel):
    id: UUID
    provider: str
    protocol: str
    name: str
    status: str
    domain: str | None
    issuer_url: str | None
    metadata_url: str | None
    secret_ref: str | None
    config: dict
    created_at: datetime


class SecretCreate(BaseModel):
    workspace_id: UUID | None = None
    name: str
    secret_type: str
    provider: str = "internal"
    secret_ref: str
    rotation_policy: dict = Field(default_factory=dict)
    expires_at: datetime | None = None
    metadata_json: dict = Field(default_factory=dict)


class SecretOut(BaseModel):
    id: UUID
    workspace_id: UUID | None
    name: str
    secret_type: str
    provider: str
    secret_ref: str
    current_version: int
    status: str
    last_rotated_at: datetime | None
    expires_at: datetime | None
    metadata_json: dict
    created_at: datetime


class ComplianceFrameworkCreate(BaseModel):
    framework: str
    status: str = "in_progress"
    readiness_score: float = 0
    controls: dict = Field(default_factory=dict)
    evidence_summary: dict = Field(default_factory=dict)


class ComplianceFrameworkOut(BaseModel):
    id: UUID
    framework: str
    status: str
    readiness_score: float
    controls: dict
    evidence_summary: dict
    created_at: datetime


class DataGovernancePolicyCreate(BaseModel):
    workspace_id: UUID | None = None
    name: str
    policy_type: str
    data_classification: str | None = None
    retention_days: int | None = None
    residency_region: str | None = None
    legal_hold: dict = Field(default_factory=dict)
    rules: dict = Field(default_factory=dict)


class RiskEventCreate(BaseModel):
    workspace_id: UUID | None = None
    user_id: UUID | None = None
    event_type: str
    risk_level: str = "low"
    risk_score: float = 0
    signal_payload: dict = Field(default_factory=dict)


class RiskEventOut(BaseModel):
    id: UUID
    workspace_id: UUID | None
    user_id: UUID | None
    event_type: str
    risk_level: str
    risk_score: float
    status: str
    signal_payload: dict
    mitigation_state: dict
    created_at: datetime


class SecurityAnalyticsSummary(BaseModel):
    security_score: float
    grade: str
    active_policies: int
    abac_policies: int
    sso_connections: int
    secrets: int
    open_risks: int
    compliance: dict
    ai_security_center: dict
    recommendations: list[dict]
