from datetime import UTC, datetime, timedelta
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event
from app.voice.models import VoiceAudioMetadata, VoiceConfiguration, VoiceProviderSetting, VoiceSession, VoiceSessionMetric, VoiceStreamEvent
from app.voice.providers import AudioChunk, provider_registry

DEFAULT_AUDIO_FORMAT = {"codec": "pcm16", "sample_rate_hz": 16000, "channels": 1, "chunk_ms": 20}
DEFAULT_VAD = {"provider": "energy_threshold", "min_speech_ms": 120, "silence_timeout_ms": 650, "noise_suppression": "provider"}
DEFAULT_INTERRUPTION = {"barge_in_enabled": True, "stop_playback_on_speech": True, "preserve_partial_response": True, "resume_strategy": "immediate"}
DEFAULT_LATENCY_BUDGET = {"audio_ingest_ms": 30, "vad_ms": 20, "stt_ms": 250, "reasoning_ms": 700, "tts_ms": 250, "total_ms": 1200}


def configuration_dict(config: VoiceConfiguration) -> dict:
    return {
        "id": config.id,
        "organization_id": config.organization_id,
        "workspace_id": config.workspace_id,
        "agent_id": config.agent_id,
        "name": config.name,
        "status": config.status,
        "language": config.language,
        "accent": config.accent,
        "stt_provider": config.stt_provider,
        "stt_model": config.stt_model,
        "tts_provider": config.tts_provider,
        "tts_model": config.tts_model,
        "voice_id": config.voice_id,
        "speaking_speed": config.speaking_speed,
        "stability": config.stability,
        "emotion": config.emotion,
        "streaming_mode": config.streaming_mode,
        "audio_format": config.audio_format,
        "vad_config": config.vad_config,
        "interruption_config": config.interruption_config,
        "latency_budget": config.latency_budget,
        "fallback_chain": config.fallback_chain,
        "metadata_json": config.metadata_json,
        "created_at": config.created_at,
        "updated_at": config.updated_at,
    }


def session_dict(session: VoiceSession) -> dict:
    return {
        "id": session.id,
        "organization_id": session.organization_id,
        "workspace_id": session.workspace_id,
        "agent_id": session.agent_id,
        "voice_configuration_id": session.voice_configuration_id,
        "user_id": session.user_id,
        "channel": session.channel,
        "direction": session.direction,
        "status": session.status,
        "current_speaker": session.current_speaker,
        "active_response_id": session.active_response_id,
        "interrupt_count": session.interrupt_count,
        "pending_tool_calls": session.pending_tool_calls,
        "context_snapshot": session.context_snapshot,
        "memory_updates": session.memory_updates,
        "conversation_state": session.conversation_state,
        "transport_state": session.transport_state,
        "started_at": session.started_at,
        "last_activity_at": session.last_activity_at,
        "timeout_at": session.timeout_at,
        "ended_at": session.ended_at,
        "termination_reason": session.termination_reason,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


def provider_setting_dict(setting: VoiceProviderSetting) -> dict:
    return {
        "id": setting.id,
        "workspace_id": setting.workspace_id,
        "name": setting.name,
        "provider_type": setting.provider_type,
        "provider": setting.provider,
        "status": setting.status,
        "priority": setting.priority,
        "secret_ref": setting.secret_ref,
        "config": setting.config,
        "capabilities": setting.capabilities,
        "health_state": setting.health_state,
        "created_at": setting.created_at,
        "updated_at": setting.updated_at,
    }


def metric_dict(metric: VoiceSessionMetric) -> dict:
    return {
        "id": metric.id,
        "session_id": metric.session_id,
        "metric_name": metric.metric_name,
        "metric_value": float(metric.metric_value),
        "unit": metric.unit,
        "stage": metric.stage,
        "provider": metric.provider,
        "captured_at": metric.captured_at,
        "metadata_json": metric.metadata_json,
    }


def event_dict(event: VoiceStreamEvent) -> dict:
    return {
        "id": event.id,
        "session_id": event.session_id,
        "event_type": event.event_type,
        "sequence_number": event.sequence_number,
        "source": event.source,
        "stage": event.stage,
        "payload": event.payload,
        "latency_ms": event.latency_ms,
        "provider": event.provider,
        "trace_id": event.trace_id,
        "created_at": event.created_at,
    }


async def emit_voice_event(db: AsyncSession, current: CurrentUser, name: str, session: VoiceSession, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=session.workspace_id, actor_user_id=current.user.id, name=name, aggregate_type="voice_session", aggregate_id=session.id, source="voice-engine", payload=payload, metadata={"channel": session.channel, "status": session.status}))


async def create_default_configuration(db: AsyncSession, current: CurrentUser, payload) -> VoiceConfiguration:
    config = VoiceConfiguration(
        organization_id=current.organization_id,
        workspace_id=payload.workspace_id,
        agent_id=payload.agent_id,
        name=payload.name,
        status=payload.status,
        language=payload.language,
        accent=payload.accent,
        stt_provider=payload.stt_provider,
        stt_model=payload.stt_model,
        tts_provider=payload.tts_provider,
        tts_model=payload.tts_model,
        voice_id=payload.voice_id,
        speaking_speed=payload.speaking_speed,
        stability=payload.stability,
        emotion=payload.emotion,
        streaming_mode=payload.streaming_mode,
        audio_format=payload.audio_format or DEFAULT_AUDIO_FORMAT,
        vad_config=payload.vad_config or DEFAULT_VAD,
        interruption_config=payload.interruption_config or DEFAULT_INTERRUPTION,
        latency_budget=payload.latency_budget or DEFAULT_LATENCY_BUDGET,
        fallback_chain=payload.fallback_chain,
        metadata_json=payload.metadata_json,
        created_by_user_id=current.user.id,
        updated_by_user_id=current.user.id,
    )
    db.add(config)
    await db.flush()
    return config


async def get_owned_configuration(db: AsyncSession, config_id: UUID, current: CurrentUser) -> VoiceConfiguration | None:
    return (await db.execute(select(VoiceConfiguration).where(VoiceConfiguration.id == config_id, VoiceConfiguration.organization_id == current.organization_id, VoiceConfiguration.deleted_at.is_(None)))).scalar_one_or_none()


async def get_owned_session(db: AsyncSession, session_id: UUID, current: CurrentUser) -> VoiceSession | None:
    return (await db.execute(select(VoiceSession).where(VoiceSession.id == session_id, VoiceSession.organization_id == current.organization_id))).scalar_one_or_none()


async def start_voice_session(db: AsyncSession, current: CurrentUser, payload) -> VoiceSession:
    now = datetime.now(UTC)
    config = await get_owned_configuration(db, payload.voice_configuration_id, current) if payload.voice_configuration_id else None
    session = VoiceSession(
        organization_id=current.organization_id,
        workspace_id=payload.workspace_id,
        agent_id=payload.agent_id or (config.agent_id if config else None),
        voice_configuration_id=config.id if config else None,
        user_id=current.user.id,
        channel=payload.channel,
        direction=payload.direction,
        status="active",
        current_speaker="none",
        pending_tool_calls=[],
        context_snapshot=payload.context_snapshot,
        memory_updates=[],
        conversation_state={"turns": [], "pipeline": "audio->vad->stt->conversation->orchestrator->tts->audio", "streaming": True},
        transport_state={"mode": payload.transport_mode, "connection_id": payload.connection_id, "secure_transport_required": True},
        started_at=now,
        last_activity_at=now,
        timeout_at=now + timedelta(minutes=payload.timeout_minutes),
    )
    db.add(session)
    await db.flush()
    db.add(VoiceAudioMetadata(organization_id=current.organization_id, workspace_id=session.workspace_id, session_id=session.id, direction="inbound", codec="pcm16", sample_rate_hz=16000, channels=1, storage_policy="metadata_only"))
    db.add(VoiceAudioMetadata(organization_id=current.organization_id, workspace_id=session.workspace_id, session_id=session.id, direction="outbound", codec="pcm16", sample_rate_hz=16000, channels=1, storage_policy="metadata_only"))
    await append_stream_event(db, current, session, "session.started", "system", "session", {"channel": session.channel, "direction": session.direction})
    return session


async def append_stream_event(db: AsyncSession, current: CurrentUser, session: VoiceSession, event_type: str, source: str, stage: str | None, payload: dict, latency_ms: int | None = None, provider: str | None = None) -> VoiceStreamEvent:
    max_sequence = (await db.execute(select(func.max(VoiceStreamEvent.sequence_number)).where(VoiceStreamEvent.session_id == session.id))).scalar_one_or_none() or 0
    event = VoiceStreamEvent(organization_id=current.organization_id, workspace_id=session.workspace_id, session_id=session.id, event_type=event_type, sequence_number=int(max_sequence) + 1, source=source, stage=stage, payload=payload, latency_ms=latency_ms, provider=provider, trace_id=payload.get("trace_id"))
    db.add(event)
    session.last_activity_at = datetime.now(UTC)
    return event


async def process_stream_event(db: AsyncSession, current: CurrentUser, session: VoiceSession, payload) -> list[VoiceStreamEvent]:
    emitted: list[VoiceStreamEvent] = []
    incoming = await append_stream_event(db, current, session, payload.event_type, payload.source, payload.stage, payload.payload, payload.latency_ms, payload.provider)
    emitted.append(incoming)
    if payload.event_type == "audio.chunk":
        config = await db.get(VoiceConfiguration, session.voice_configuration_id) if session.voice_configuration_id else None
        vad_config = config.vad_config if config else DEFAULT_VAD
        audio_config = config.audio_format if config else DEFAULT_AUDIO_FORMAT
        chunk = AudioChunk(sequence_number=incoming.sequence_number, payload_ref=payload.payload.get("payload_ref"), duration_ms=int(payload.payload.get("duration_ms", audio_config.get("chunk_ms", 20))), codec=audio_config.get("codec", "pcm16"), sample_rate_hz=int(audio_config.get("sample_rate_hz", 16000)))
        vad = await provider_registry.vad(vad_config.get("provider", "energy_threshold")).detect(chunk, vad_config)
        emitted.append(await append_stream_event(db, current, session, f"vad.{vad.event}", "voice-engine", "vad", {"confidence": vad.confidence, "silence_ms": vad.silence_ms, "noise_score": vad.noise_score}, 12, vad_config.get("provider")))
        if vad.event == "speech_detected":
            session.current_speaker = "user"
            transcript = await provider_registry.stt((config.stt_provider if config else "placeholder")).transcribe_stream(chunk, {"language": config.language if config else "en"})
            emitted.append(await append_stream_event(db, current, session, "stt.partial", "voice-engine", "stt", {"text": transcript.text, "is_final": transcript.is_final, "confidence": transcript.confidence, "language": transcript.language}, transcript.latency_ms, config.stt_provider if config else "placeholder"))
    if payload.event_type == "user.interrupt":
        session.interrupt_count += 1
        session.current_speaker = "user"
        session.active_response_id = None
        session.conversation_state = {**(session.conversation_state or {}), "interrupted_at": datetime.now(UTC).isoformat(), "barge_in": "playback_stopped"}
        emitted.append(await append_stream_event(db, current, session, "playback.stop", "voice-engine", "interruption", {"reason": "barge_in", "preserve_state": True}))
    return emitted


async def record_latency_metric(db: AsyncSession, session: VoiceSession, name: str, value: float, stage: str | None = None, provider: str | None = None, unit: str = "ms", metadata: dict | None = None) -> VoiceSessionMetric:
    metric = VoiceSessionMetric(organization_id=session.organization_id, workspace_id=session.workspace_id, session_id=session.id, metric_name=name, metric_value=value, unit=unit, stage=stage, provider=provider, captured_at=datetime.now(UTC), metadata_json=metadata or {})
    db.add(metric)
    return metric


async def terminate_session(db: AsyncSession, current: CurrentUser, session: VoiceSession, reason: str) -> VoiceSession:
    session.status = "ended"
    session.ended_at = datetime.now(UTC)
    session.termination_reason = reason
    await append_stream_event(db, current, session, "session.ended", "system", "session", {"reason": reason})
    return session