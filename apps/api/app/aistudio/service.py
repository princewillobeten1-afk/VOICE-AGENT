import re
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.aistudio.models import AIStudioDeployment, AIStudioEvaluationRun, AIStudioInteractionTimeline, AIStudioPrompt, AIStudioPromptTemplate, AIStudioPromptVersion, AIStudioSimulationScenario, AIStudioTestSuite
from app.identity.dependencies import CurrentUser


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "prompt"


def estimate_tokens(*parts: str | None) -> int:
    text = "\n".join(part for part in parts if part)
    return max(1, int(len(text.split()) * 1.35)) if text else 0


def prompt_out(item: AIStudioPrompt) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "agent_id": item.agent_id, "name": item.name, "slug": item.slug, "category": item.category, "status": item.status, "current_version_id": item.current_version_id, "description": item.description, "tags": item.tags, "created_at": item.created_at, "updated_at": item.updated_at}


def version_out(item: AIStudioPromptVersion) -> dict:
    return {"id": item.id, "prompt_id": item.prompt_id, "version_number": item.version_number, "status": item.status, "system_prompt": item.system_prompt, "developer_prompt": item.developer_prompt, "variables": item.variables, "guardrails": item.guardrails, "model_settings": item.model_config, "token_estimate": item.token_estimate, "validation_state": item.validation_state, "release_notes": item.release_notes, "created_at": item.created_at}


def template_out(item: AIStudioPromptTemplate) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "category": item.category, "status": item.status, "description": item.description, "template_body": item.template_body, "variables": item.variables, "recommended_guardrails": item.recommended_guardrails, "created_at": item.created_at}


async def next_prompt_version(db: AsyncSession, prompt_id) -> int:
    result = await db.execute(select(func.max(AIStudioPromptVersion.version_number)).where(AIStudioPromptVersion.prompt_id == prompt_id))
    return int(result.scalar_one() or 0) + 1


async def studio_summary(db: AsyncSession, current: CurrentUser) -> dict:
    org = current.organization_id
    prompts = int((await db.execute(select(func.count()).select_from(AIStudioPrompt).where(AIStudioPrompt.organization_id == org, AIStudioPrompt.deleted_at.is_(None)))).scalar_one() or 0)
    versions = int((await db.execute(select(func.count()).select_from(AIStudioPromptVersion).where(AIStudioPromptVersion.organization_id == org))).scalar_one() or 0)
    templates = int((await db.execute(select(func.count()).select_from(AIStudioPromptTemplate).where(AIStudioPromptTemplate.organization_id == org, AIStudioPromptTemplate.deleted_at.is_(None)))).scalar_one() or 0)
    simulations = int((await db.execute(select(func.count()).select_from(AIStudioSimulationScenario).where(AIStudioSimulationScenario.organization_id == org, AIStudioSimulationScenario.deleted_at.is_(None)))).scalar_one() or 0)
    evaluations = int((await db.execute(select(func.count()).select_from(AIStudioEvaluationRun).where(AIStudioEvaluationRun.organization_id == org))).scalar_one() or 0)
    test_suites = int((await db.execute(select(func.count()).select_from(AIStudioTestSuite).where(AIStudioTestSuite.organization_id == org, AIStudioTestSuite.deleted_at.is_(None)))).scalar_one() or 0)
    deployments = int((await db.execute(select(func.count()).select_from(AIStudioDeployment).where(AIStudioDeployment.organization_id == org))).scalar_one() or 0)
    avg = (await db.execute(select(func.avg(AIStudioEvaluationRun.score)).where(AIStudioEvaluationRun.organization_id == org, AIStudioEvaluationRun.score.is_not(None)))).scalar_one()
    timeline_events = int((await db.execute(select(func.count()).select_from(AIStudioInteractionTimeline).where(AIStudioInteractionTimeline.organization_id == org))).scalar_one() or 0)
    return {"prompts": prompts, "prompt_versions": versions, "templates": templates, "simulations": simulations, "evaluations": evaluations, "test_suites": test_suites, "deployments": deployments, "average_score": float(avg or 0), "ai_timeline_events": timeline_events, "recommendations": [{"title": "Create deployment-gated regression suite", "impact": "high"}, {"title": "Add edge-case simulations for interruptions", "impact": "medium"}, {"title": "Track prompt cost and latency by version", "impact": "medium"}]}