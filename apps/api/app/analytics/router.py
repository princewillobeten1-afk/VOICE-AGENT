from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.analytics.models import OpsAlert, OpsCostRecord, OpsEvaluationResult, OpsHealthReport
from app.analytics.schemas import AlertCreate, AlertOut, CostCreate, CostOut, EvaluationCreate, EvaluationOut, ExecutiveSummaryOut, HealthCreate, HealthOut
from app.analytics.service import alert_dict, analytics_breakdown, cost_dict, dashboard_dict, evaluation_dict, executive_summary, health_dict, live_monitoring
from app.core.database import get_db
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.models import AuditLog
from app.identity.rbac import Permission

router = APIRouter(prefix="/analytics", tags=["aiops-analytics"])


@router.get("/dashboard", response_model=ExecutiveSummaryOut)
async def dashboard(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return ExecutiveSummaryOut(**await executive_summary(db, current, workspace_id))


@router.get("/live")
async def live(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return await live_monitoring(db, current, workspace_id)


@router.get("/breakdown")
async def breakdown(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return await analytics_breakdown(db, current, workspace_id)


@router.post("/alerts", response_model=AlertOut, status_code=status.HTTP_201_CREATED)
async def create_alert(payload: AlertCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    alert = OpsAlert(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, alert_type=payload.alert_type, severity=payload.severity, condition=payload.condition, channels=payload.channels, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(alert)
    await db.commit()
    return AlertOut(**alert_dict(alert))


@router.get("/alerts", response_model=list[AlertOut])
async def list_alerts(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(OpsAlert).where(OpsAlert.organization_id == current.organization_id, OpsAlert.workspace_id == workspace_id, OpsAlert.deleted_at.is_(None)).order_by(OpsAlert.updated_at.desc()))).scalars().all()
    return [AlertOut(**alert_dict(item)) for item in rows]


@router.post("/health", response_model=HealthOut, status_code=status.HTTP_201_CREATED)
async def create_health(payload: HealthCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    report = OpsHealthReport(organization_id=current.organization_id, workspace_id=payload.workspace_id, component=payload.component, status=payload.status, score=payload.score, checks=payload.checks, incidents=payload.incidents, measured_at=datetime.now(UTC))
    db.add(report)
    await db.commit()
    return HealthOut(**health_dict(report))


@router.get("/health", response_model=list[HealthOut])
async def list_health(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(OpsHealthReport).where(OpsHealthReport.organization_id == current.organization_id, OpsHealthReport.workspace_id == workspace_id).order_by(OpsHealthReport.measured_at.desc()).limit(100))).scalars().all()
    return [HealthOut(**health_dict(item)) for item in rows]


@router.post("/costs", response_model=CostOut, status_code=status.HTTP_201_CREATED)
async def create_cost(payload: CostCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    record = OpsCostRecord(organization_id=current.organization_id, workspace_id=payload.workspace_id, cost_type=payload.cost_type, provider=payload.provider, entity_type=payload.entity_type, entity_id=payload.entity_id, amount=payload.amount, currency=payload.currency, quantity=payload.quantity, unit=payload.unit, occurred_at=datetime.now(UTC), metadata_json=payload.metadata_json)
    db.add(record)
    await db.commit()
    return CostOut(**cost_dict(record))


@router.get("/costs", response_model=list[CostOut])
async def list_costs(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(OpsCostRecord).where(OpsCostRecord.organization_id == current.organization_id, OpsCostRecord.workspace_id == workspace_id).order_by(OpsCostRecord.occurred_at.desc()).limit(100))).scalars().all()
    return [CostOut(**cost_dict(item)) for item in rows]


@router.post("/evaluations", response_model=EvaluationOut, status_code=status.HTTP_201_CREATED)
async def create_evaluation(payload: EvaluationCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = OpsEvaluationResult(organization_id=current.organization_id, workspace_id=payload.workspace_id, agent_id=payload.agent_id, conversation_id=payload.conversation_id, evaluation_type=payload.evaluation_type, score=payload.score, status=payload.status, evaluator=payload.evaluator, criteria=payload.criteria, result=payload.result, evaluated_at=datetime.now(UTC))
    db.add(item)
    await db.commit()
    return EvaluationOut(**evaluation_dict(item))


@router.get("/evaluations", response_model=list[EvaluationOut])
async def list_evaluations(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(OpsEvaluationResult).where(OpsEvaluationResult.organization_id == current.organization_id, OpsEvaluationResult.workspace_id == workspace_id).order_by(OpsEvaluationResult.created_at.desc()).limit(100))).scalars().all()
    return [EvaluationOut(**evaluation_dict(item)) for item in rows]


@router.get("/audit")
async def audit_logs(organization_id: UUID, current: CurrentUser = Depends(require_permission(Permission.AUDIT_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AuditLog).where(AuditLog.organization_id == organization_id).order_by(AuditLog.created_at.desc()).limit(100))).scalars().all()
    return {"logs": [{"id": item.id, "action": item.action, "actor_user_id": item.actor_user_id, "target_type": item.target_type, "target_id": item.target_id, "created_at": item.created_at, "metadata_json": item.metadata_json} for item in rows]}
