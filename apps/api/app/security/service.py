from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.identity.dependencies import CurrentUser
from app.identity.models import AuditLog, Session
from app.security.models import ABACPolicy, ComplianceFramework, GovernancePolicy, SecretRecord, SecurityRiskEvent, SSOConnection


def policy_out(item: GovernancePolicy) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "policy_type": item.policy_type, "status": item.status, "enforcement_mode": item.enforcement_mode, "scope": item.scope, "rules": item.rules, "created_at": item.created_at}


def abac_out(item: ABACPolicy) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "effect": item.effect, "resource_type": item.resource_type, "action": item.action, "conditions": item.conditions, "priority": item.priority, "status": item.status, "created_at": item.created_at}


def sso_out(item: SSOConnection) -> dict:
    return {"id": item.id, "provider": item.provider, "protocol": item.protocol, "name": item.name, "status": item.status, "domain": item.domain, "issuer_url": item.issuer_url, "metadata_url": item.metadata_url, "secret_ref": item.secret_ref, "config": item.config, "created_at": item.created_at}


def secret_out(item: SecretRecord) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "secret_type": item.secret_type, "provider": item.provider, "secret_ref": item.secret_ref, "current_version": item.current_version, "status": item.status, "last_rotated_at": item.last_rotated_at, "expires_at": item.expires_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


def compliance_out(item: ComplianceFramework) -> dict:
    return {"id": item.id, "framework": item.framework, "status": item.status, "readiness_score": float(item.readiness_score), "controls": item.controls, "evidence_summary": item.evidence_summary, "created_at": item.created_at}


def risk_out(item: SecurityRiskEvent) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "user_id": item.user_id, "event_type": item.event_type, "risk_level": item.risk_level, "risk_score": float(item.risk_score), "status": item.status, "signal_payload": item.signal_payload, "mitigation_state": item.mitigation_state, "created_at": item.created_at}


async def security_summary(db: AsyncSession, current: CurrentUser) -> dict:
    active_policies = int((await db.execute(select(func.count()).select_from(GovernancePolicy).where(GovernancePolicy.organization_id == current.organization_id, GovernancePolicy.status == "active", GovernancePolicy.deleted_at.is_(None)))).scalar_one() or 0)
    abac_policies = int((await db.execute(select(func.count()).select_from(ABACPolicy).where(ABACPolicy.organization_id == current.organization_id, ABACPolicy.status == "active", ABACPolicy.deleted_at.is_(None)))).scalar_one() or 0)
    sso_connections = int((await db.execute(select(func.count()).select_from(SSOConnection).where(SSOConnection.organization_id == current.organization_id, SSOConnection.deleted_at.is_(None)))).scalar_one() or 0)
    secrets = int((await db.execute(select(func.count()).select_from(SecretRecord).where(SecretRecord.organization_id == current.organization_id, SecretRecord.deleted_at.is_(None)))).scalar_one() or 0)
    open_risks = int((await db.execute(select(func.count()).select_from(SecurityRiskEvent).where(SecurityRiskEvent.organization_id == current.organization_id, SecurityRiskEvent.status == "open"))).scalar_one() or 0)
    audit_count = int((await db.execute(select(func.count()).select_from(AuditLog).where(AuditLog.organization_id == current.organization_id))).scalar_one() or 0)
    session_count = int((await db.execute(select(func.count()).select_from(Session).where(Session.user_id == current.user.id))).scalar_one() or 0)
    score = max(35, min(98, 72 + active_policies * 2 + abac_policies - open_risks * 5 + (5 if sso_connections else 0)))
    grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D"
    return {"security_score": float(score), "grade": grade, "active_policies": active_policies, "abac_policies": abac_policies, "sso_connections": sso_connections, "secrets": secrets, "open_risks": open_risks, "compliance": {"soc2": "readiness", "iso27001": "readiness", "gdpr": "mapped", "hipaa": "awareness", "audit_events": audit_count, "sessions": session_count}, "ai_security_center": {"ai_employee_permissions": "mapped", "tool_permissions": "mapped", "workflow_permissions": "mapped", "knowledge_access": "mapped", "memory_access": "mapped", "delegation_permissions": "mapped"}, "recommendations": [{"title": "Require MFA for admins", "impact": "high"}, {"title": "Enable SSO connection", "impact": "medium"}, {"title": "Rotate stale secrets", "impact": "medium"}]}
