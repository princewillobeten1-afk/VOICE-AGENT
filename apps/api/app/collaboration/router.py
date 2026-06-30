from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.collaboration.models import AiTeam, AiTeamMember, CollaborationLog, CollaborationPolicy, CollaborationSession
from app.collaboration.schemas import AnalyticsOut, DelegationOut, DelegationRequest, LogOut, MemberAssign, MemberOut, PolicyCreate, SessionOut, TeamCreate, TeamOut
from app.collaboration.service import analytics, create_delegation, delegation_dict, log_dict, member_dict, session_dict, team_dict
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission

router = APIRouter(prefix="/collaboration", tags=["multi-agent-collaboration"])


@router.get("/teams", response_model=list[TeamOut])
async def list_teams(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AiTeam).where(AiTeam.organization_id == current.organization_id, AiTeam.workspace_id == workspace_id, AiTeam.deleted_at.is_(None)).order_by(AiTeam.updated_at.desc()))).scalars().all()
    return [TeamOut(**team_dict(item)) for item in rows]


@router.post("/teams", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team(payload: TeamCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    team = AiTeam(organization_id=current.organization_id, workspace_id=payload.workspace_id, parent_team_id=payload.parent_team_id, supervisor_agent_id=payload.supervisor_agent_id, name=payload.name, slug=payload.slug, department=payload.department, description=payload.description, responsibilities=payload.responsibilities, routing_policy=payload.routing_policy, collaboration_rules=payload.collaboration_rules, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(team)
    await db.flush()
    await audit(db, "collaboration.team.created", current.user.id, current.organization_id, "ai_team", team.id)
    await db.commit()
    return TeamOut(**team_dict(team))


@router.post("/teams/{team_id}/members", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
async def assign_member(team_id: UUID, payload: MemberAssign, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    team = await db.get(AiTeam, team_id)
    if team is None or team.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Team not found")
    member = AiTeamMember(organization_id=current.organization_id, workspace_id=payload.workspace_id, team_id=team_id, agent_id=payload.agent_id, role_id=payload.role_id, membership_type=payload.membership_type, responsibilities=payload.responsibilities, availability_state=payload.availability_state, workload_score=payload.workload_score, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(member)
    await db.commit()
    return MemberOut(**member_dict(member))


@router.get("/teams/{team_id}/members", response_model=list[MemberOut])
async def list_members(team_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AiTeamMember).where(AiTeamMember.organization_id == current.organization_id, AiTeamMember.team_id == team_id, AiTeamMember.deleted_at.is_(None)).order_by(AiTeamMember.created_at.desc()))).scalars().all()
    return [MemberOut(**member_dict(item)) for item in rows]


@router.post("/policies", status_code=status.HTTP_201_CREATED)
async def create_policy(payload: PolicyCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    policy = CollaborationPolicy(organization_id=current.organization_id, workspace_id=payload.workspace_id, team_id=payload.team_id, name=payload.name, policy_type=payload.policy_type, max_delegation_depth=payload.max_delegation_depth, allowed_delegations=payload.allowed_delegations, approval_requirements=payload.approval_requirements, escalation_rules=payload.escalation_rules, department_restrictions=payload.department_restrictions, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(policy)
    await db.commit()
    return {"id": policy.id, "status": policy.status, "name": policy.name}


@router.post("/delegate", response_model=DelegationOut, status_code=status.HTTP_201_CREATED)
async def delegate_task(payload: DelegationRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    event = await create_delegation(db, current, payload)
    await audit(db, "collaboration.delegated", current.user.id, current.organization_id, "delegation_event", event.id)
    await db.commit()
    return DelegationOut(**delegation_dict(event))


@router.get("/sessions", response_model=list[SessionOut])
async def list_sessions(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(CollaborationSession).where(CollaborationSession.organization_id == current.organization_id, CollaborationSession.workspace_id == workspace_id).order_by(CollaborationSession.created_at.desc()).limit(100))).scalars().all()
    return [SessionOut(**session_dict(item)) for item in rows]


@router.get("/sessions/{session_id}/timeline", response_model=list[LogOut])
async def session_timeline(session_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(CollaborationLog).where(CollaborationLog.organization_id == current.organization_id, CollaborationLog.session_id == session_id).order_by(CollaborationLog.created_at.asc()))).scalars().all()
    return [LogOut(**log_dict(item)) for item in rows]


@router.get("/analytics", response_model=AnalyticsOut)
async def collaboration_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return AnalyticsOut(**await analytics(db, current, workspace_id))
