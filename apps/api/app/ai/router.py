from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.models import Agent, AgentConfiguration, AgentPublishingHistory, AgentTemplate, AgentVersion
from app.ai.schemas import AgentCreate, AgentDetail, AgentOut, AgentTemplateOut, AgentUpdate, AgentVersionOut, AgentVersionUpsert, BuilderStateUpdate, DuplicateRequest, PlaygroundResult, PublishRequest
from app.ai.service import agent_out, create_initial_version, emit_agent_event, ensure_templates, get_owned_agent, record_publish_history, slugify, template_out, version_out
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission

router = APIRouter(prefix="/ai-employees", tags=["ai-employees"])


@router.get("", response_model=list[AgentOut])
async def list_agents(workspace_id: UUID, q: str | None = None, status_filter: str | None = Query(default=None, alias="status"), category: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Agent).where(Agent.organization_id == current.organization_id, Agent.workspace_id == workspace_id, Agent.deleted_at.is_(None))
    if q:
        query = query.where(or_(Agent.name.ilike(f"%{q}%"), Agent.role.ilike(f"%{q}%"), Agent.department.ilike(f"%{q}%")))
    if status_filter:
        query = query.where(Agent.status == status_filter)
    if category:
        query = query.where(Agent.category == category)
    rows = (await db.execute(query.order_by(Agent.updated_at.desc()))).scalars().all()
    return [AgentOut(**agent_out(item)) for item in rows]


@router.post("", response_model=AgentDetail, status_code=status.HTTP_201_CREATED)
async def create_agent(payload: AgentCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    slug = slugify(payload.name)
    agent = Agent(organization_id=current.organization_id, workspace_id=payload.workspace_id, project_id=payload.project_id, name=payload.name, slug=slug, display_name=payload.name, role=payload.role, department=payload.department, description=payload.description, category=payload.category, template_id=payload.template_id, status="draft", lifecycle_stage="builder", settings={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(agent)
    await db.flush()
    version = await create_initial_version(db, agent, current)
    config = AgentConfiguration(organization_id=current.organization_id, workspace_id=payload.workspace_id, agent_id=agent.id, active_version_id=version.id, builder_state={"current_step": "identity", "completed_steps": ["identity"]}, readiness={"status": "draft", "checks": []}, playground_state={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(config)
    await record_publish_history(db, current, agent, version, "created", None, "draft", "Initial AI employee draft created")
    await emit_agent_event(db, current, "ai.employee.created", agent, {"role": agent.role})
    await audit(db, "ai_employee.created", current.user.id, current.organization_id, "agent", agent.id)
    await db.commit()
    return await detail_response(db, agent)


@router.get("/templates", response_model=list[AgentTemplateOut])
async def list_templates(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    await ensure_templates(db)
    rows = (await db.execute(select(AgentTemplate).where(AgentTemplate.deleted_at.is_(None), AgentTemplate.status == "active").order_by(AgentTemplate.featured.desc(), AgentTemplate.name.asc()))).scalars().all()
    await db.commit()
    return [AgentTemplateOut(**template_out(item)) for item in rows]


@router.get("/{agent_id}", response_model=AgentDetail)
async def get_agent(agent_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    return await detail_response(db, agent)


@router.patch("/{agent_id}", response_model=AgentOut)
async def update_agent(agent_id: UUID, payload: AgentUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)
    if payload.name:
        agent.slug = slugify(payload.name)
    agent.updated_by_user_id = current.user.id
    await emit_agent_event(db, current, "ai.employee.updated", agent, {})
    await audit(db, "ai_employee.updated", current.user.id, current.organization_id, "agent", agent.id)
    await db.commit()
    return AgentOut(**agent_out(agent))


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    agent.deleted_at = datetime.now(UTC)
    await record_publish_history(db, current, agent, None, "deleted", agent.status, "deleted")
    await emit_agent_event(db, current, "ai.employee.deleted", agent, {})
    await audit(db, "ai_employee.deleted", current.user.id, current.organization_id, "agent", agent.id)
    await db.commit()


@router.post("/{agent_id}/versions", response_model=AgentVersionOut, status_code=201)
async def create_version(agent_id: UUID, payload: AgentVersionUpsert, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    version = await create_initial_version(db, agent, current, payload)
    await record_publish_history(db, current, agent, version, "version.created", agent.status, agent.status, payload.change_summary)
    await emit_agent_event(db, current, "ai.employee.version.created", agent, {"version_number": version.version_number})
    await db.commit()
    return AgentVersionOut(**version_out(version))


@router.get("/{agent_id}/versions", response_model=list[AgentVersionOut])
async def list_versions(agent_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    versions = (await db.execute(select(AgentVersion).where(AgentVersion.agent_id == agent.id).order_by(AgentVersion.version_number.desc()))).scalars().all()
    return [AgentVersionOut(**version_out(item)) for item in versions]


@router.post("/{agent_id}/publish", response_model=AgentOut)
async def publish_agent(agent_id: UUID, payload: PublishRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    version = await db.get(AgentVersion, agent.current_version_id) if agent.current_version_id else None
    if version is None:
        raise HTTPException(status_code=400, detail="AI employee has no version to publish")
    from_status = agent.status
    now = datetime.now(UTC)
    agent.status = "published"
    agent.lifecycle_stage = "published"
    agent.last_published_at = now
    version.status = "published"
    version.published_at = now
    await record_publish_history(db, current, agent, version, "published", from_status, "published", payload.change_summary)
    await emit_agent_event(db, current, "ai.employee.published", agent, {"version_number": version.version_number})
    await audit(db, "ai_employee.published", current.user.id, current.organization_id, "agent", agent.id)
    await db.commit()
    return AgentOut(**agent_out(agent))


@router.post("/{agent_id}/archive", response_model=AgentOut)
async def archive_agent(agent_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    from_status = agent.status
    agent.status = "archived"
    agent.archived_at = datetime.now(UTC)
    await record_publish_history(db, current, agent, None, "archived", from_status, "archived")
    await emit_agent_event(db, current, "ai.employee.archived", agent, {})
    await db.commit()
    return AgentOut(**agent_out(agent))


@router.post("/{agent_id}/duplicate", response_model=AgentDetail, status_code=201)
async def duplicate_agent(agent_id: UUID, payload: DuplicateRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    source = await get_owned_agent(db, agent_id, current)
    if source is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    copy = Agent(organization_id=source.organization_id, workspace_id=source.workspace_id, project_id=source.project_id, name=payload.name, slug=slugify(payload.name), display_name=payload.name, role=source.role, department=source.department, description=source.description, category=source.category, template_id=source.template_id, status="draft", lifecycle_stage="builder", settings=source.settings, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(copy)
    await db.flush()
    source_version = await db.get(AgentVersion, source.current_version_id) if source.current_version_id else None
    data = AgentVersionUpsert(instructions=source_version.instructions if source_version else None, change_summary=f"Duplicated from {source.name}", personality_config=source_version.personality_config if source_version else {}, voice_config=source_version.voice_config if source_version else {}, knowledge_config=source_version.knowledge_config if source_version else {}, memory_config=source_version.memory_config if source_version else {}, channel_config=source_version.channel_config if source_version else {}, collaboration_config=source_version.collaboration_config if source_version else {}, model_config=source_version.model_config if source_version else {}, tool_config=source_version.tool_config if source_version else {}, workflow_config=source_version.workflow_config if source_version else {}, validation_state=source_version.validation_state if source_version else {})
    version = await create_initial_version(db, copy, current, data)
    db.add(AgentConfiguration(organization_id=current.organization_id, workspace_id=copy.workspace_id, agent_id=copy.id, active_version_id=version.id, builder_state={"current_step": "review", "duplicated_from": str(source.id)}, readiness={}, playground_state={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id))
    await record_publish_history(db, current, copy, version, "duplicated", None, "draft", f"Duplicated from {source.name}")
    await emit_agent_event(db, current, "ai.employee.duplicated", copy, {"source_agent_id": str(source.id)})
    await db.commit()
    return await detail_response(db, copy)


@router.put("/{agent_id}/builder-state", response_model=AgentDetail)
async def update_builder_state(agent_id: UUID, payload: BuilderStateUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    config = (await db.execute(select(AgentConfiguration).where(AgentConfiguration.agent_id == agent.id))).scalar_one_or_none()
    if config is None:
        config = AgentConfiguration(organization_id=current.organization_id, workspace_id=agent.workspace_id, agent_id=agent.id, active_version_id=agent.current_version_id, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
        db.add(config)
    config.builder_state = payload.builder_state
    config.readiness = payload.readiness
    config.playground_state = payload.playground_state
    await db.commit()
    return await detail_response(db, agent)


@router.post("/{agent_id}/playground", response_model=PlaygroundResult)
async def playground(agent_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    agent = await get_owned_agent(db, agent_id, current)
    if agent is None:
        raise HTTPException(status_code=404, detail="AI employee not found")
    return PlaygroundResult(response=f"{agent.name} is ready for safe simulation. Real model execution is intentionally not enabled in Task 012.", context_preview={"sources": ["identity", "instructions", "placeholder knowledge"], "token_budget": "architecture-ready"}, memory_preview={"short_term": "enabled placeholder", "long_term": "policy pending"}, tool_logs=[{"tool": "calendar.lookup", "status": "placeholder"}], response_time_ms=184, token_usage={"input": 0, "output": 0, "mode": "placeholder"})


async def detail_response(db: AsyncSession, agent: Agent) -> AgentDetail:
    versions = (await db.execute(select(AgentVersion).where(AgentVersion.agent_id == agent.id).order_by(AgentVersion.version_number.desc()))).scalars().all()
    config = (await db.execute(select(AgentConfiguration).where(AgentConfiguration.agent_id == agent.id))).scalar_one_or_none()
    history = (await db.execute(select(AgentPublishingHistory).where(AgentPublishingHistory.agent_id == agent.id).order_by(AgentPublishingHistory.created_at.desc()).limit(20))).scalars().all()
    return AgentDetail(agent=AgentOut(**agent_out(agent)), versions=[AgentVersionOut(**version_out(item)) for item in versions], configuration={"builder_state": config.builder_state, "readiness": config.readiness, "playground_state": config.playground_state} if config else None, publishing_history=[{"id": str(item.id), "action": item.action, "from_status": item.from_status, "to_status": item.to_status, "change_summary": item.change_summary, "created_at": item.created_at.isoformat() if item.created_at else None} for item in history])