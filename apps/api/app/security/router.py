from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.models import AuditLog, Session
from app.identity.rbac import Permission
from app.security.models import ABACPolicy, ComplianceFramework, DataGovernancePolicy, GovernancePolicy, SecretRecord, SecurityRiskEvent, SSOConnection
from app.security.schemas import ABACPolicyCreate, ABACPolicyOut, ComplianceFrameworkCreate, ComplianceFrameworkOut, DataGovernancePolicyCreate, PolicyCreate, PolicyOut, RiskEventCreate, RiskEventOut, SSOConnectionCreate, SSOConnectionOut, SecretCreate, SecretOut, SecurityAnalyticsSummary
from app.security.service import abac_out, compliance_out, policy_out, risk_out, secret_out, security_summary, sso_out

router = APIRouter(prefix="/security", tags=["security"])


@router.post("/policies", response_model=PolicyOut, status_code=status.HTTP_201_CREATED)
async def create_policy(payload: PolicyCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = GovernancePolicy(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, policy_type=payload.policy_type, enforcement_mode=payload.enforcement_mode, scope=payload.scope, rules=payload.rules, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.flush()
    await audit(db, "security.policy.created", current.user.id, current.organization_id, "governance_policy", item.id)
    await db.commit()
    return PolicyOut(**policy_out(item))


@router.get("/policies", response_model=list[PolicyOut])
async def list_policies(workspace_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(GovernancePolicy).where(GovernancePolicy.organization_id == current.organization_id, GovernancePolicy.deleted_at.is_(None))
    if workspace_id:
        query = query.where(GovernancePolicy.workspace_id == workspace_id)
    rows = (await db.execute(query.order_by(GovernancePolicy.created_at.desc()))).scalars().all()
    return [PolicyOut(**policy_out(item)) for item in rows]


@router.post("/abac-policies", response_model=ABACPolicyOut, status_code=status.HTTP_201_CREATED)
async def create_abac_policy(payload: ABACPolicyCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = ABACPolicy(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, effect=payload.effect, resource_type=payload.resource_type, action=payload.action, conditions=payload.conditions, priority=payload.priority, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return ABACPolicyOut(**abac_out(item))


@router.get("/abac-policies", response_model=list[ABACPolicyOut])
async def list_abac_policies(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ABACPolicy).where(ABACPolicy.organization_id == current.organization_id, ABACPolicy.deleted_at.is_(None)).order_by(ABACPolicy.priority.asc()))).scalars().all()
    return [ABACPolicyOut(**abac_out(item)) for item in rows]


@router.post("/sso", response_model=SSOConnectionOut, status_code=status.HTTP_201_CREATED)
async def create_sso(payload: SSOConnectionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = SSOConnection(organization_id=current.organization_id, provider=payload.provider, protocol=payload.protocol, name=payload.name, domain=payload.domain, issuer_url=payload.issuer_url, metadata_url=payload.metadata_url, secret_ref=payload.secret_ref, config=payload.config, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return SSOConnectionOut(**sso_out(item))


@router.get("/sso", response_model=list[SSOConnectionOut])
async def list_sso(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(SSOConnection).where(SSOConnection.organization_id == current.organization_id, SSOConnection.deleted_at.is_(None)).order_by(SSOConnection.created_at.desc()))).scalars().all()
    return [SSOConnectionOut(**sso_out(item)) for item in rows]


@router.post("/secrets", response_model=SecretOut, status_code=status.HTTP_201_CREATED)
async def create_secret(payload: SecretCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = SecretRecord(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, secret_type=payload.secret_type, provider=payload.provider, secret_ref=payload.secret_ref, rotation_policy=payload.rotation_policy, expires_at=payload.expires_at, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return SecretOut(**secret_out(item))


@router.get("/secrets", response_model=list[SecretOut])
async def list_secrets(workspace_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(SecretRecord).where(SecretRecord.organization_id == current.organization_id, SecretRecord.deleted_at.is_(None))
    if workspace_id:
        query = query.where(SecretRecord.workspace_id == workspace_id)
    rows = (await db.execute(query.order_by(SecretRecord.created_at.desc()))).scalars().all()
    return [SecretOut(**secret_out(item)) for item in rows]


@router.post("/compliance/frameworks", response_model=ComplianceFrameworkOut, status_code=status.HTTP_201_CREATED)
async def create_compliance_framework(payload: ComplianceFrameworkCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = ComplianceFramework(organization_id=current.organization_id, framework=payload.framework, status=payload.status, readiness_score=payload.readiness_score, controls=payload.controls, evidence_summary=payload.evidence_summary, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return ComplianceFrameworkOut(**compliance_out(item))


@router.get("/compliance/frameworks", response_model=list[ComplianceFrameworkOut])
async def list_compliance_frameworks(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ComplianceFramework).where(ComplianceFramework.organization_id == current.organization_id, ComplianceFramework.deleted_at.is_(None)).order_by(ComplianceFramework.framework.asc()))).scalars().all()
    return [ComplianceFrameworkOut(**compliance_out(item)) for item in rows]


@router.post("/data-governance", status_code=status.HTTP_201_CREATED)
async def create_data_governance_policy(payload: DataGovernancePolicyCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = DataGovernancePolicy(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, policy_type=payload.policy_type, data_classification=payload.data_classification, retention_days=payload.retention_days, residency_region=payload.residency_region, legal_hold=payload.legal_hold, rules=payload.rules, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "name": item.name, "status": item.status}


@router.post("/risk-events", response_model=RiskEventOut, status_code=status.HTTP_201_CREATED)
async def create_risk_event(payload: RiskEventCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = SecurityRiskEvent(organization_id=current.organization_id, workspace_id=payload.workspace_id, user_id=payload.user_id, event_type=payload.event_type, risk_level=payload.risk_level, risk_score=payload.risk_score, signal_payload=payload.signal_payload)
    db.add(item)
    await db.commit()
    return RiskEventOut(**risk_out(item))


@router.get("/risk-events", response_model=list[RiskEventOut])
async def list_risk_events(workspace_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(SecurityRiskEvent).where(SecurityRiskEvent.organization_id == current.organization_id)
    if workspace_id:
        query = query.where(SecurityRiskEvent.workspace_id == workspace_id)
    rows = (await db.execute(query.order_by(SecurityRiskEvent.created_at.desc()).limit(100))).scalars().all()
    return [RiskEventOut(**risk_out(item)) for item in rows]


@router.get("/sessions")
async def session_center(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Session).where(Session.user_id == current.user.id).order_by(Session.created_at.desc()).limit(50))).scalars().all()
    return [{"id": row.id, "user_id": row.user_id, "expires_at": row.expires_at, "revoked_at": row.revoked_at, "user_agent": row.user_agent, "ip_address": str(row.ip_address) if row.ip_address else None} for row in rows]


@router.get("/audit")
async def audit_center(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AuditLog).where(AuditLog.organization_id == current.organization_id).order_by(AuditLog.created_at.desc()).limit(100))).scalars().all()
    return [{"id": row.id, "event_type": row.event_type, "actor_user_id": row.actor_user_id, "target_type": row.target_type, "target_id": row.target_id, "created_at": row.created_at, "metadata": row.metadata_json} for row in rows]


@router.get("/governance-graph")
async def governance_graph(workspace_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return {"organization_id": current.organization_id, "workspace_id": workspace_id, "nodes": ["organization", "workspaces", "teams", "users", "ai_employees", "workflows", "knowledge_bases", "integrations"], "edges": ["membership", "ownership", "access", "delegation", "execution"], "status": "snapshot_ready"}


@router.get("/analytics", response_model=SecurityAnalyticsSummary)
async def analytics(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return SecurityAnalyticsSummary(**await security_summary(db, current))
