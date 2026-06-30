from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.voice.models import VoiceConfiguration, VoiceProviderSetting, VoiceSession, VoiceSessionMetric, VoiceStreamEvent
from app.voice.providers import provider_registry
from app.voice.schemas import VoiceConfigurationCreate, VoiceConfigurationOut, VoiceConfigurationUpdate, VoiceProviderSettingCreate, VoiceProviderSettingOut, VoiceSessionCreate, VoiceSessionDetail, VoiceSessionMetricOut, VoiceSessionOut, VoiceStreamEventBatch, VoiceStreamEventCreate, VoiceStreamEventOut, VoiceTerminateRequest, VoiceTestRunRequest, VoiceTestRunResult
from app.voice.service import append_stream_event, configuration_dict, create_default_configuration, emit_voice_event, event_dict, get_owned_configuration, get_owned_session, metric_dict, process_stream_event, provider_setting_dict, record_latency_metric, session_dict, start_voice_session, terminate_session

router = APIRouter(prefix="/voice", tags=["voice-engine"])


@router.get("/providers")
async def provider_catalog(current: CurrentUser = Depends(require_permission(Permission.ORG_READ))):
    return {"providers": provider_registry.provider_catalog(), "selection_strategy": "workspace configuration with priority-ordered fallback chains"}


@router.get("/configurations", response_model=list[VoiceConfigurationOut])
async def list_configurations(workspace_id: UUID, status_filter: str | None = Query(default=None, alias="status"), current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(VoiceConfiguration).where(VoiceConfiguration.organization_id == current.organization_id, VoiceConfiguration.workspace_id == workspace_id, VoiceConfiguration.deleted_at.is_(None))
    if status_filter:
        query = query.where(VoiceConfiguration.status == status_filter)
    rows = (await db.execute(query.order_by(VoiceConfiguration.updated_at.desc()))).scalars().all()
    return [VoiceConfigurationOut(**configuration_dict(item)) for item in rows]


@router.post("/configurations", response_model=VoiceConfigurationOut, status_code=status.HTTP_201_CREATED)
async def create_configuration(payload: VoiceConfigurationCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    config = await create_default_configuration(db, current, payload)
    await audit(db, "voice.configuration.created", current.user.id, current.organization_id, "voice_configuration", config.id)
    await db.commit()
    return VoiceConfigurationOut(**configuration_dict(config))


@router.patch("/configurations/{configuration_id}", response_model=VoiceConfigurationOut)
async def update_configuration(configuration_id: UUID, payload: VoiceConfigurationUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    config = await get_owned_configuration(db, configuration_id, current)
    if config is None:
        raise HTTPException(status_code=404, detail="Voice configuration not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    config.updated_by_user_id = current.user.id
    await audit(db, "voice.configuration.updated", current.user.id, current.organization_id, "voice_configuration", config.id)
    await db.commit()
    return VoiceConfigurationOut(**configuration_dict(config))


@router.get("/provider-settings", response_model=list[VoiceProviderSettingOut])
async def list_provider_settings(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(VoiceProviderSetting).where(VoiceProviderSetting.organization_id == current.organization_id, VoiceProviderSetting.workspace_id == workspace_id, VoiceProviderSetting.deleted_at.is_(None)).order_by(VoiceProviderSetting.provider_type.asc(), VoiceProviderSetting.priority.asc()))).scalars().all()
    return [VoiceProviderSettingOut(**provider_setting_dict(item)) for item in rows]


@router.post("/provider-settings", response_model=VoiceProviderSettingOut, status_code=status.HTTP_201_CREATED)
async def create_provider_setting(payload: VoiceProviderSettingCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    setting = VoiceProviderSetting(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, provider_type=payload.provider_type, provider=payload.provider, status=payload.status, priority=payload.priority, secret_ref=payload.secret_ref, config=payload.config, capabilities=payload.capabilities, health_state=payload.health_state, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(setting)
    await db.flush()
    await audit(db, "voice.provider_setting.created", current.user.id, current.organization_id, "voice_provider_setting", setting.id)
    await db.commit()
    return VoiceProviderSettingOut(**provider_setting_dict(setting))


@router.get("/sessions", response_model=list[VoiceSessionOut])
async def list_sessions(workspace_id: UUID, status_filter: str | None = Query(default=None, alias="status"), current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(VoiceSession).where(VoiceSession.organization_id == current.organization_id, VoiceSession.workspace_id == workspace_id)
    if status_filter:
        query = query.where(VoiceSession.status == status_filter)
    rows = (await db.execute(query.order_by(VoiceSession.last_activity_at.desc()).limit(100))).scalars().all()
    return [VoiceSessionOut(**session_dict(item)) for item in rows]


@router.post("/sessions", response_model=VoiceSessionOut, status_code=status.HTTP_201_CREATED)
async def create_session(payload: VoiceSessionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    session = await start_voice_session(db, current, payload)
    await record_latency_metric(db, session, "session_start_latency", 38, "session", "internal")
    await emit_voice_event(db, current, "voice.session.started", session, {"channel": session.channel})
    await audit(db, "voice.session.started", current.user.id, current.organization_id, "voice_session", session.id)
    await db.commit()
    return VoiceSessionOut(**session_dict(session))


@router.get("/sessions/{session_id}", response_model=VoiceSessionDetail)
async def get_session(session_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    session = await get_owned_session(db, session_id, current)
    if session is None:
        raise HTTPException(status_code=404, detail="Voice session not found")
    events = (await db.execute(select(VoiceStreamEvent).where(VoiceStreamEvent.session_id == session.id).order_by(VoiceStreamEvent.sequence_number.asc()).limit(200))).scalars().all()
    metrics = (await db.execute(select(VoiceSessionMetric).where(VoiceSessionMetric.session_id == session.id).order_by(VoiceSessionMetric.captured_at.desc()).limit(50))).scalars().all()
    return VoiceSessionDetail(session=VoiceSessionOut(**session_dict(session)), events=[VoiceStreamEventOut(**event_dict(item)) for item in events], metrics=[VoiceSessionMetricOut(**metric_dict(item)) for item in metrics])


@router.post("/sessions/{session_id}/stream-events", response_model=VoiceStreamEventBatch)
async def create_stream_event(session_id: UUID, payload: VoiceStreamEventCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    session = await get_owned_session(db, session_id, current)
    if session is None:
        raise HTTPException(status_code=404, detail="Voice session not found")
    events = await process_stream_event(db, current, session, payload)
    await record_latency_metric(db, session, payload.stage or payload.event_type, payload.latency_ms or 0, payload.stage, payload.provider, metadata={"event_type": payload.event_type})
    await db.commit()
    return VoiceStreamEventBatch(events=[VoiceStreamEventOut(**event_dict(item)) for item in events])


@router.post("/sessions/{session_id}/interrupt", response_model=VoiceStreamEventBatch)
async def interrupt_session(session_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    session = await get_owned_session(db, session_id, current)
    if session is None:
        raise HTTPException(status_code=404, detail="Voice session not found")
    events = await process_stream_event(db, current, session, VoiceStreamEventCreate(event_type="user.interrupt", source="client", stage="interruption", payload={"reason": "barge_in"}))
    await emit_voice_event(db, current, "voice.session.interrupted", session, {"interrupt_count": session.interrupt_count})
    await db.commit()
    return VoiceStreamEventBatch(events=[VoiceStreamEventOut(**event_dict(item)) for item in events])


@router.post("/sessions/{session_id}/resume", response_model=VoiceSessionOut)
async def resume_session(session_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    session = await get_owned_session(db, session_id, current)
    if session is None:
        raise HTTPException(status_code=404, detail="Voice session not found")
    session.status = "active"
    await append_stream_event(db, current, session, "session.resumed", "system", "session", {"recovery": "state_preserved"})
    await db.commit()
    return VoiceSessionOut(**session_dict(session))


@router.post("/sessions/{session_id}/terminate", response_model=VoiceSessionOut)
async def end_session(session_id: UUID, payload: VoiceTerminateRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    session = await get_owned_session(db, session_id, current)
    if session is None:
        raise HTTPException(status_code=404, detail="Voice session not found")
    await terminate_session(db, current, session, payload.reason)
    await emit_voice_event(db, current, "voice.session.ended", session, {"reason": payload.reason})
    await audit(db, "voice.session.ended", current.user.id, current.organization_id, "voice_session", session.id)
    await db.commit()
    return VoiceSessionOut(**session_dict(session))


@router.get("/sessions/{session_id}/metrics", response_model=list[VoiceSessionMetricOut])
async def session_metrics(session_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    session = await get_owned_session(db, session_id, current)
    if session is None:
        raise HTTPException(status_code=404, detail="Voice session not found")
    metrics = (await db.execute(select(VoiceSessionMetric).where(VoiceSessionMetric.session_id == session.id).order_by(VoiceSessionMetric.captured_at.desc()).limit(200))).scalars().all()
    return [VoiceSessionMetricOut(**metric_dict(item)) for item in metrics]


@router.post("/test-run", response_model=VoiceTestRunResult)
async def test_run(payload: VoiceTestRunRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    config = await get_owned_configuration(db, payload.voice_configuration_id, current) if payload.voice_configuration_id else None
    provider_plan = {"stt": config.stt_provider if config else "placeholder", "tts": config.tts_provider if config else "placeholder", "vad": (config.vad_config or {}).get("provider", "energy_threshold") if config else "energy_threshold", "fallback_chain": config.fallback_chain if config else []}
    return VoiceTestRunResult(status="simulation_ready", pipeline=["audio_stream", "vad", "stt", "conversation_manager", "ai_orchestrator_placeholder", "tool_execution_placeholder", "tts", "audio_stream"], transcript_preview="This is a simulated real-time voice test. No provider call was made.", tts_payload_ref="memory://placeholder-audio-chunk", estimated_latency_ms=412, provider_plan=provider_plan, safety_notes=["Raw audio storage is disabled by default.", "Tool execution and advanced reasoning remain placeholders in Task 013.", "Provider credentials are referenced by secret_ref only."])