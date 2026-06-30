from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.models import Agent, AgentConfiguration
from app.ai.schemas import AgentOut
from app.ai.service import agent_out, create_initial_version, emit_agent_event, slugify
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.workspace.models import Project, Workspace
from app.workspace.schemas import DemoBootstrapOut, ProjectOut, WorkspaceOut

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[WorkspaceOut])
async def list_workspaces(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Workspace).where(Workspace.organization_id == current.organization_id, Workspace.deleted_at.is_(None)).order_by(Workspace.created_at.asc()))).scalars().all()
    return rows


@router.get("/{workspace_id}/projects", response_model=list[ProjectOut])
async def list_projects(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Project).where(Project.organization_id == current.organization_id, Project.workspace_id == workspace_id, Project.deleted_at.is_(None)).order_by(Project.created_at.asc()))).scalars().all()
    return rows


@router.post("/bootstrap-demo", response_model=DemoBootstrapOut)
async def bootstrap_demo(current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    workspace = (await db.execute(select(Workspace).where(Workspace.organization_id == current.organization_id, Workspace.slug == "demo-workspace", Workspace.deleted_at.is_(None)))).scalar_one_or_none()
    if workspace is None:
        workspace = Workspace(organization_id=current.organization_id, name="Demo Workspace", slug="demo-workspace", description="Safe sample workspace for exploring VoiceSense live data.", settings={"demo": True}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
        db.add(workspace)
        await db.flush()

    project = (await db.execute(select(Project).where(Project.organization_id == current.organization_id, Project.workspace_id == workspace.id, Project.slug == "ai-employee-demo", Project.deleted_at.is_(None)))).scalar_one_or_none()
    if project is None:
        project = Project(organization_id=current.organization_id, workspace_id=workspace.id, name="AI Employee Demo", slug="ai-employee-demo", description="Demo project with seeded AI employees and live dashboard data.", settings={"demo": True}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
        db.add(project)
        await db.flush()

    seeds = [
        {"name": "Maya", "role": "Customer Success Agent", "department": "CX", "category": "support", "status": "published", "stage": "live", "description": "Handles billing questions, refund preparation, and customer retention workflows."},
        {"name": "Noah", "role": "Inbound Sales Qualifier", "department": "Revenue", "category": "sales", "status": "testing", "stage": "testing", "description": "Qualifies inbound leads, captures intent, and prepares calendar handoffs."},
        {"name": "Iris", "role": "Internal IT Helper", "department": "Operations", "category": "internal", "status": "draft", "stage": "builder", "description": "Answers internal policy questions and drafts support tickets."},
    ]
    existing = (await db.execute(select(Agent).where(Agent.organization_id == current.organization_id, Agent.workspace_id == workspace.id, Agent.deleted_at.is_(None)))).scalars().all()
    existing_slugs = {agent.slug for agent in existing}
    for seed in seeds:
        slug = slugify(seed["name"])
        if slug in existing_slugs:
            continue
        agent = Agent(organization_id=current.organization_id, workspace_id=workspace.id, project_id=project.id, name=seed["name"], slug=slug, display_name=seed["name"], role=seed["role"], department=seed["department"], description=seed["description"], category=seed["category"], status=seed["status"], lifecycle_stage=seed["stage"], settings={"demo": True, "channels": ["voice", "chat", "email"]}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
        db.add(agent)
        await db.flush()
        version = await create_initial_version(db, agent, current)
        agent.current_version_id = version.id
        db.add(AgentConfiguration(organization_id=current.organization_id, workspace_id=workspace.id, agent_id=agent.id, active_version_id=version.id, builder_state={"current_step": "review", "demo": True}, readiness={"status": seed["status"], "checks": ["prompt", "knowledge", "tools"]}, playground_state={"last_mode": "simulation"}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id))
        await emit_agent_event(db, current, "ai.employee.demo_seeded", agent, {"source": "bootstrap-demo"})
        existing.append(agent)
    await audit(db, "workspace.demo_bootstrapped", current.user.id, current.organization_id, "workspace", workspace.id)
    await db.commit()
    agents = (await db.execute(select(Agent).where(Agent.organization_id == current.organization_id, Agent.workspace_id == workspace.id, Agent.deleted_at.is_(None)).order_by(Agent.created_at.asc()))).scalars().all()
    return DemoBootstrapOut(workspace=WorkspaceOut.model_validate(workspace), project=ProjectOut.model_validate(project), agents=[AgentOut(**agent_out(agent)) for agent in agents])