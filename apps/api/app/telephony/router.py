from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.telephony.models import CallQueue, PhoneNumber, TelephonyCall, TelephonyCallEvent, TelephonyProviderConfig
from app.telephony.schemas import CallCreate, CallEventOut, CallOut, NumberCreate, NumberOut, ProviderCreate, ProviderOut, QueueCreate, QueueOut
from app.telephony.service import analytics, call_dict, create_call, event_dict, number_dict, provider_dict, queue_dict

router = APIRouter(prefix="/telephony", tags=["telephony"])


def _websocket_url_from_base(base_url: str | None) -> str:
    base = (base_url or "https://localhost:8000").rstrip("/")
    if base.startswith("https://"):
        base = "wss://" + base.removeprefix("https://")
    elif base.startswith("http://"):
        base = "ws://" + base.removeprefix("http://")
    return f"{base}/v1/voice/twilio/stream"


@router.post("/twilio/incoming-call", include_in_schema=False)
async def twilio_incoming_call():
    """Public Twilio webhook that connects a phone call to the voice WebSocket."""
    stream_url = _websocket_url_from_base(get_settings().twilio_webhook_base_url)
    twiml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
  <Connect>
    <Stream url=\"{stream_url}\" />
  </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")


@router.get("/providers/catalog")
async def provider_catalog():
    return {"providers": ["twilio", "telnyx", "plivo", "vonage", "signalwire", "amazon_connect", "azure_communication_services", "custom_sip"], "note": "Provider adapters are configured, not hardcoded. Twilio Media Streams is the active realtime phone-call bridge."}


@router.post("/providers", response_model=ProviderOut, status_code=status.HTTP_201_CREATED)
async def create_provider(payload: ProviderCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = TelephonyProviderConfig(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, provider=payload.provider, status=payload.status, priority=payload.priority, region=payload.region, secret_ref=payload.secret_ref, capabilities=payload.capabilities, failover_policy=payload.failover_policy, config=payload.config, health_state={"status": "unknown"}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return ProviderOut(**provider_dict(item))


@router.get("/providers", response_model=list[ProviderOut])
async def list_providers(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(TelephonyProviderConfig).where(TelephonyProviderConfig.organization_id == current.organization_id, TelephonyProviderConfig.workspace_id == workspace_id, TelephonyProviderConfig.deleted_at.is_(None)).order_by(TelephonyProviderConfig.priority.asc()))).scalars().all()
    return [ProviderOut(**provider_dict(item)) for item in rows]


@router.post("/numbers", response_model=NumberOut, status_code=status.HTTP_201_CREATED)
async def create_number(payload: NumberCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = PhoneNumber(organization_id=current.organization_id, workspace_id=payload.workspace_id, provider_config_id=payload.provider_config_id, assigned_agent_id=payload.assigned_agent_id, queue_id=payload.queue_id, e164=payload.e164, label=payload.label, number_type=payload.number_type, country=payload.country, region=payload.region, routing_config=payload.routing_config, compliance_config=payload.compliance_config, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return NumberOut(**number_dict(item))


@router.get("/numbers", response_model=list[NumberOut])
async def list_numbers(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(PhoneNumber).where(PhoneNumber.organization_id == current.organization_id, PhoneNumber.workspace_id == workspace_id, PhoneNumber.deleted_at.is_(None)).order_by(PhoneNumber.created_at.desc()))).scalars().all()
    return [NumberOut(**number_dict(item)) for item in rows]


@router.post("/queues", response_model=QueueOut, status_code=status.HTTP_201_CREATED)
async def create_queue(payload: QueueCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = CallQueue(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, slug=payload.slug, priority=payload.priority, overflow_policy=payload.overflow_policy, assignment_policy=payload.assignment_policy, estimated_wait_seconds=payload.estimated_wait_seconds, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return QueueOut(**queue_dict(item))


@router.get("/queues", response_model=list[QueueOut])
async def list_queues(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(CallQueue).where(CallQueue.organization_id == current.organization_id, CallQueue.workspace_id == workspace_id, CallQueue.deleted_at.is_(None)).order_by(CallQueue.priority.asc()))).scalars().all()
    return [QueueOut(**queue_dict(item)) for item in rows]


@router.post("/calls", response_model=CallOut, status_code=status.HTTP_201_CREATED)
async def start_call(payload: CallCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    call = await create_call(db, current, payload)
    await audit(db, "telephony.call.started", current.user.id, current.organization_id, "telephony_call", call.id)
    await db.commit()
    return CallOut(**call_dict(call))


@router.post("/calls/{call_id}/end", response_model=CallOut)
async def end_call(call_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    call = await db.get(TelephonyCall, call_id)
    if call is None or call.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Call not found")
    now = datetime.now(UTC)
    call.status = "ended"
    call.ended_at = now
    call.duration_seconds = int((now - call.started_at).total_seconds()) if call.started_at else None
    db.add(TelephonyCallEvent(organization_id=current.organization_id, workspace_id=call.workspace_id, call_id=call.id, event_type="call.ended", sequence_number=99, source="api", payload={"reason": "manual"}))
    await db.commit()
    return CallOut(**call_dict(call))


@router.get("/calls", response_model=list[CallOut])
async def list_calls(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(TelephonyCall).where(TelephonyCall.organization_id == current.organization_id, TelephonyCall.workspace_id == workspace_id).order_by(TelephonyCall.created_at.desc()).limit(100))).scalars().all()
    return [CallOut(**call_dict(item)) for item in rows]


@router.get("/calls/{call_id}/events", response_model=list[CallEventOut])
async def call_events(call_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(TelephonyCallEvent).where(TelephonyCallEvent.organization_id == current.organization_id, TelephonyCallEvent.call_id == call_id).order_by(TelephonyCallEvent.sequence_number.asc()))).scalars().all()
    return [CallEventOut(**event_dict(item)) for item in rows]


@router.get("/analytics")
async def telephony_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return await analytics(db, current, workspace_id)
