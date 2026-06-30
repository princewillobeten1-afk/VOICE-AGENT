from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.aistudio.models import AIStudioBenchmark, AIStudioComment, AIStudioDeployment, AIStudioEvaluationRun, AIStudioPlaygroundRun, AIStudioPrompt, AIStudioPromptTemplate, AIStudioPromptVersion, AIStudioSimulationScenario, AIStudioTestSuite
from app.aistudio.schemas import BenchmarkCreate, CommentCreate, DeploymentCreate, EvaluationCreate, EvaluationOut, PlaygroundRunCreate, PlaygroundRunOut, PromptCreate, PromptOut, PromptVersionCreate, PromptVersionOut, SimulationCreate, SimulationOut, StudioSummary, TemplateCreate, TemplateOut, TestSuiteCreate, TestSuiteOut
from app.aistudio.service import estimate_tokens, next_prompt_version, prompt_out, slugify, studio_summary, template_out, version_out
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission

router = APIRouter(prefix="/ai-studio", tags=["ai-studio"])


@router.get("/summary", response_model=StudioSummary)
async def summary(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return StudioSummary(**await studio_summary(db, current))


@router.post("/prompts", response_model=PromptOut, status_code=status.HTTP_201_CREATED)
async def create_prompt(payload: PromptCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    prompt = AIStudioPrompt(organization_id=current.organization_id, workspace_id=payload.workspace_id, agent_id=payload.agent_id, name=payload.name, slug=slugify(payload.name), category=payload.category, status="draft", description=payload.description, tags=[], settings={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(prompt)
    await db.flush()
    version = AIStudioPromptVersion(organization_id=current.organization_id, workspace_id=payload.workspace_id, prompt_id=prompt.id, version_number=1, status="draft", system_prompt=payload.system_prompt, developer_prompt=None, variables=payload.variables, sections=[], guardrails=payload.guardrails, dynamic_context={}, model_config=payload.model_settings, token_estimate=estimate_tokens(payload.system_prompt), validation_state={"status": "valid"}, release_notes="Initial draft", created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    await db.flush()
    prompt.current_version_id = version.id
    await audit(db, "ai_studio.prompt.created", current.user.id, current.organization_id, "ai_studio_prompt", prompt.id)
    await db.commit()
    return PromptOut(**prompt_out(prompt))


@router.get("/prompts", response_model=list[PromptOut])
async def list_prompts(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AIStudioPrompt).where(AIStudioPrompt.organization_id == current.organization_id, AIStudioPrompt.workspace_id == workspace_id, AIStudioPrompt.deleted_at.is_(None)).order_by(AIStudioPrompt.updated_at.desc()))).scalars().all()
    return [PromptOut(**prompt_out(item)) for item in rows]


@router.post("/prompts/{prompt_id}/versions", response_model=PromptVersionOut, status_code=status.HTTP_201_CREATED)
async def create_version(prompt_id: UUID, payload: PromptVersionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    prompt = await db.get(AIStudioPrompt, prompt_id)
    if prompt is None or prompt.organization_id != current.organization_id or prompt.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    version = AIStudioPromptVersion(organization_id=current.organization_id, workspace_id=prompt.workspace_id, prompt_id=prompt.id, version_number=await next_prompt_version(db, prompt.id), status="draft", system_prompt=payload.system_prompt, developer_prompt=payload.developer_prompt, variables=payload.variables, sections=payload.sections, guardrails=payload.guardrails, dynamic_context=payload.dynamic_context, model_config=payload.model_settings, token_estimate=estimate_tokens(payload.system_prompt, payload.developer_prompt), validation_state={"status": "valid"}, release_notes=payload.release_notes, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    await db.flush()
    prompt.current_version_id = version.id
    await audit(db, "ai_studio.prompt.version_created", current.user.id, current.organization_id, "ai_studio_prompt_version", version.id)
    await db.commit()
    return PromptVersionOut(**version_out(version))


@router.get("/prompts/{prompt_id}/versions", response_model=list[PromptVersionOut])
async def list_versions(prompt_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AIStudioPromptVersion).where(AIStudioPromptVersion.organization_id == current.organization_id, AIStudioPromptVersion.prompt_id == prompt_id).order_by(AIStudioPromptVersion.version_number.desc()))).scalars().all()
    return [PromptVersionOut(**version_out(item)) for item in rows]


@router.post("/templates", response_model=TemplateOut, status_code=status.HTTP_201_CREATED)
async def create_template(payload: TemplateCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioPromptTemplate(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, category=payload.category, description=payload.description, template_body=payload.template_body, variables=payload.variables, recommended_guardrails=payload.recommended_guardrails, metadata_json={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return TemplateOut(**template_out(item))


@router.get("/templates", response_model=list[TemplateOut])
async def list_templates(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AIStudioPromptTemplate).where(AIStudioPromptTemplate.organization_id == current.organization_id, AIStudioPromptTemplate.workspace_id == workspace_id, AIStudioPromptTemplate.deleted_at.is_(None)).order_by(AIStudioPromptTemplate.category.asc(), AIStudioPromptTemplate.name.asc()))).scalars().all()
    return [TemplateOut(**template_out(item)) for item in rows]


@router.post("/playground/runs", response_model=PlaygroundRunOut, status_code=status.HTTP_201_CREATED)
async def create_playground_run(payload: PlaygroundRunCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioPlaygroundRun(organization_id=current.organization_id, workspace_id=payload.workspace_id, prompt_id=payload.prompt_id, prompt_version_id=payload.prompt_version_id, agent_id=payload.agent_id, channel=payload.channel, input_payload=payload.input_payload, output_payload={"preview": "Runtime execution is deferred to provider adapters."}, execution_trace={"timeline": ["prompt", "context", "tools", "response"]}, status="completed", latency_ms=0, cost_usd=0, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return PlaygroundRunOut(id=item.id, workspace_id=item.workspace_id, prompt_id=item.prompt_id, prompt_version_id=item.prompt_version_id, agent_id=item.agent_id, channel=item.channel, status=item.status, output_payload=item.output_payload, execution_trace=item.execution_trace, latency_ms=item.latency_ms, cost_usd=float(item.cost_usd or 0), created_at=item.created_at)


@router.post("/simulations", response_model=SimulationOut, status_code=status.HTTP_201_CREATED)
async def create_simulation(payload: SimulationCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioSimulationScenario(organization_id=current.organization_id, workspace_id=payload.workspace_id, prompt_id=payload.prompt_id, name=payload.name, scenario_type=payload.scenario_type, persona=payload.persona, conversation_script=payload.conversation_script, assertions=payload.assertions, metadata_json={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return SimulationOut(id=item.id, workspace_id=item.workspace_id, prompt_id=item.prompt_id, name=item.name, scenario_type=item.scenario_type, status=item.status, persona=item.persona, conversation_script=item.conversation_script, assertions=item.assertions, created_at=item.created_at)


@router.get("/simulations", response_model=list[SimulationOut])
async def list_simulations(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AIStudioSimulationScenario).where(AIStudioSimulationScenario.organization_id == current.organization_id, AIStudioSimulationScenario.workspace_id == workspace_id, AIStudioSimulationScenario.deleted_at.is_(None)).order_by(AIStudioSimulationScenario.created_at.desc()))).scalars().all()
    return [SimulationOut(id=item.id, workspace_id=item.workspace_id, prompt_id=item.prompt_id, name=item.name, scenario_type=item.scenario_type, status=item.status, persona=item.persona, conversation_script=item.conversation_script, assertions=item.assertions, created_at=item.created_at) for item in rows]


@router.post("/evaluations", response_model=EvaluationOut, status_code=status.HTTP_201_CREATED)
async def create_evaluation(payload: EvaluationCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioEvaluationRun(organization_id=current.organization_id, workspace_id=payload.workspace_id, prompt_id=payload.prompt_id, prompt_version_id=payload.prompt_version_id, scenario_id=payload.scenario_id, status="completed", score=payload.score, metric_results=payload.metric_results, regression_summary=payload.regression_summary, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return EvaluationOut(id=item.id, workspace_id=item.workspace_id, prompt_id=item.prompt_id, prompt_version_id=item.prompt_version_id, scenario_id=item.scenario_id, status=item.status, score=float(item.score) if item.score is not None else None, metric_results=item.metric_results, regression_summary=item.regression_summary, created_at=item.created_at)


@router.post("/test-suites", response_model=TestSuiteOut, status_code=status.HTTP_201_CREATED)
async def create_test_suite(payload: TestSuiteCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioTestSuite(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, description=payload.description, schedule_config=payload.schedule_config, deployment_gate=payload.deployment_gate, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return TestSuiteOut(id=item.id, workspace_id=item.workspace_id, name=item.name, description=item.description, status=item.status, deployment_gate=item.deployment_gate, schedule_config=item.schedule_config, created_at=item.created_at)


@router.post("/benchmarks", status_code=status.HTTP_201_CREATED)
async def create_benchmark(payload: BenchmarkCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioBenchmark(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, baseline_prompt_version_id=payload.baseline_prompt_version_id, candidate_prompt_version_id=payload.candidate_prompt_version_id, metrics=payload.metrics, comparison_summary={}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "name": item.name, "status": item.status}


@router.post("/deployments", status_code=status.HTTP_201_CREATED)
async def create_deployment(payload: DeploymentCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioDeployment(organization_id=current.organization_id, workspace_id=payload.workspace_id, prompt_id=payload.prompt_id, prompt_version_id=payload.prompt_version_id, environment=payload.environment, approval_state=payload.approval_state, rollout_config=payload.rollout_config, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "environment": item.environment, "status": item.status}


@router.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(payload: CommentCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = AIStudioComment(organization_id=current.organization_id, workspace_id=payload.workspace_id, prompt_id=payload.prompt_id, prompt_version_id=payload.prompt_version_id, parent_comment_id=payload.parent_comment_id, body=payload.body, mentions=payload.mentions, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "status": item.status}


@router.get("/prompt-diff")
async def prompt_diff(left_version_id: UUID, right_version_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    left = await db.get(AIStudioPromptVersion, left_version_id)
    right = await db.get(AIStudioPromptVersion, right_version_id)
    if left is None or right is None or left.organization_id != current.organization_id or right.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Prompt version not found")
    return {"left_version_id": left.id, "right_version_id": right.id, "token_delta": right.token_estimate - left.token_estimate, "status": "diff_ready", "sections": ["system_prompt", "variables", "guardrails", "model_config"]}


@router.get("/replay/{run_id}")
async def replay(run_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    run = await db.get(AIStudioPlaygroundRun, run_id)
    if run is None or run.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run.id, "transcript": run.output_payload, "timeline": run.execution_trace.get("timeline", []), "status": "replay_ready"}