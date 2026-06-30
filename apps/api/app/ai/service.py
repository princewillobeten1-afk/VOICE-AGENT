from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.models import Agent, AgentConfiguration, AgentPublishingHistory, AgentTemplate, AgentVersion
from app.ai.schemas import AgentVersionUpsert
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event

TEMPLATE_SEEDS = [
    ("receptionist", "Receptionist", "front_office", "Answers calls, routes inquiries, and schedules follow-up.", "Receptionist", "Operations", ["calendar", "handoff"], ["phone", "chat"]),
    ("sales-representative", "Sales Representative", "sales", "Qualifies leads, answers product questions, and books meetings.", "Sales Representative", "Revenue", ["crm", "calendar", "email"], ["phone", "sms", "email"]),
    ("customer-support", "Customer Support", "support", "Resolves customer issues with policy-aware responses.", "Customer Support Agent", "CX", ["knowledge", "tickets", "crm"], ["chat", "email", "phone"]),
    ("appointment-scheduler", "Appointment Scheduler", "operations", "Coordinates availability and books appointments.", "Appointment Scheduler", "Operations", ["calendar", "email"], ["phone", "sms", "chat"]),
    ("hr-assistant", "HR Assistant", "hr", "Answers HR policy questions and routes sensitive requests.", "HR Assistant", "People", ["knowledge", "approval"], ["chat", "email"]),
    ("technical-support", "Technical Support", "support", "Triages technical issues and gathers diagnostic context.", "Technical Support Agent", "Support", ["knowledge", "tickets", "database"], ["chat", "email"]),
    ("real-estate-agent", "Real Estate Agent", "sales", "Qualifies buyers and schedules property tours.", "Real Estate Agent", "Sales", ["crm", "calendar"], ["phone", "whatsapp", "sms"]),
    ("healthcare-assistant", "Healthcare Assistant", "healthcare", "Handles appointment intake with strict safety boundaries.", "Healthcare Assistant", "Care", ["calendar", "handoff"], ["phone", "sms"]),
]


def slugify(value: str) -> str:
    chars = [char.lower() if char.isalnum() else "-" for char in value.strip()]
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "ai-employee"


def agent_out(agent: Agent) -> dict:
    return {"id": agent.id, "workspace_id": agent.workspace_id, "project_id": agent.project_id, "name": agent.name, "slug": agent.slug, "display_name": agent.display_name, "avatar_url": agent.avatar_url, "role": agent.role, "department": agent.department, "description": agent.description, "category": agent.category, "status": agent.status, "lifecycle_stage": agent.lifecycle_stage, "current_version_id": agent.current_version_id, "template_id": agent.template_id, "last_published_at": agent.last_published_at, "archived_at": agent.archived_at, "created_at": agent.created_at, "updated_at": agent.updated_at}


def version_out(version: AgentVersion) -> dict:
    return {"id": version.id, "agent_id": version.agent_id, "version_number": version.version_number, "status": version.status, "change_summary": version.change_summary, "instructions": version.instructions, "personality_config": version.personality_config, "voice_config": version.voice_config, "knowledge_config": version.knowledge_config, "memory_config": version.memory_config, "channel_config": version.channel_config, "collaboration_config": version.collaboration_config, "model_config": version.model_config, "tool_config": version.tool_config, "workflow_config": version.workflow_config, "validation_state": version.validation_state, "published_at": version.published_at, "created_at": version.created_at}


def template_out(template: AgentTemplate) -> dict:
    return {"id": template.id, "slug": template.slug, "name": template.name, "category": template.category, "description": template.description, "role": template.role, "department": template.department, "default_config": template.default_config, "recommended_tools": template.recommended_tools, "recommended_channels": template.recommended_channels, "featured": template.featured, "status": template.status}


async def ensure_templates(db: AsyncSession) -> None:
    existing = (await db.execute(select(func.count()).select_from(AgentTemplate))).scalar_one()
    if existing:
        return
    for index, (slug, name, category, description, role, department, tools, channels) in enumerate(TEMPLATE_SEEDS):
        db.add(AgentTemplate(slug=slug, name=name, category=category, description=description, role=role, department=department, default_config={"personality": {"tone": "clear", "formality": 70}, "memory": {"short_term": True, "long_term": False}}, recommended_tools=tools, recommended_channels=channels, featured=index < 4, status="active"))
    await db.flush()


async def emit_agent_event(db: AsyncSession, current: CurrentUser, name: str, agent: Agent, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(name=name, organization_id=current.organization_id, workspace_id=agent.workspace_id, actor_user_id=current.user.id, aggregate_type="agent", aggregate_id=agent.id, payload={"agent_name": agent.name, **payload}, source="ai_employee_builder"))


async def next_version_number(db: AsyncSession, agent_id: UUID) -> int:
    value = (await db.execute(select(func.coalesce(func.max(AgentVersion.version_number), 0)).where(AgentVersion.agent_id == agent_id))).scalar_one()
    return int(value) + 1


async def create_initial_version(db: AsyncSession, agent: Agent, current: CurrentUser, payload: AgentVersionUpsert | None = None) -> AgentVersion:
    data = payload or AgentVersionUpsert()
    version = AgentVersion(organization_id=agent.organization_id, workspace_id=agent.workspace_id, project_id=agent.project_id, agent_id=agent.id, version_number=await next_version_number(db, agent.id), status="draft", instructions=data.instructions or "Define this AI employee's operating instructions before publishing.", change_summary=data.change_summary or "Initial draft", personality_config=data.personality_config, voice_config=data.voice_config, knowledge_config=data.knowledge_config, memory_config=data.memory_config, channel_config=data.channel_config, collaboration_config=data.collaboration_config, model_config=data.ai_model_config or {"provider": "provider_manager", "model": "default"}, tool_config=data.tool_config, workflow_config=data.workflow_config, validation_state=data.validation_state, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    await db.flush()
    agent.current_version_id = version.id
    return version


async def record_publish_history(db: AsyncSession, current: CurrentUser, agent: Agent, version: AgentVersion | None, action: str, from_status: str | None, to_status: str | None, summary: str | None = None) -> None:
    db.add(AgentPublishingHistory(organization_id=current.organization_id, workspace_id=agent.workspace_id, agent_id=agent.id, version_id=version.id if version else None, action=action, from_status=from_status, to_status=to_status, change_summary=summary, created_by_user_id=current.user.id, updated_by_user_id=current.user.id))


async def get_owned_agent(db: AsyncSession, agent_id: UUID, current: CurrentUser) -> Agent | None:
    return (await db.execute(select(Agent).where(Agent.id == agent_id, Agent.organization_id == current.organization_id, Agent.deleted_at.is_(None)))).scalar_one_or_none()