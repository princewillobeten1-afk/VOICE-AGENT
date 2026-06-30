from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.omnichannel.models import ChannelConfiguration, ChannelSession, CustomerTimelineEvent, DeliveryEvent, OmnichannelMessage
from app.omnichannel.schemas import ChannelCreate, ChannelOut, DeliveryCreate, DeliveryOut, IdentityOut, IdentityResolveRequest, MessageCreate, MessageOut, SessionCreate, SessionOut, TimelineOut
from app.omnichannel.service import CHANNEL_CATALOG, PROVIDER_CATALOG, analytics, channel_dict, create_message, delivery_dict, identity_dict, message_dict, resolve_identity, session_dict, timeline_dict

router = APIRouter(prefix="/omnichannel", tags=["omnichannel"])


@router.get("/channels/catalog")
async def channel_catalog():
    return {"channels": CHANNEL_CATALOG, "providers": PROVIDER_CATALOG, "note": "Channels are normalized before reaching AI employees."}


@router.post("/channels", response_model=ChannelOut, status_code=status.HTTP_201_CREATED)
async def create_channel(payload: ChannelCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = ChannelConfiguration(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, channel_type=payload.channel_type, provider=payload.provider, status=payload.status, priority=payload.priority, region=payload.region, secret_ref=payload.secret_ref, capabilities=payload.capabilities, formatter_policy=payload.formatter_policy, config=payload.config, health_state={"status": "unknown"}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.flush()
    await audit(db, "omnichannel.channel.created", current.user.id, current.organization_id, "channel_configuration", item.id)
    await db.commit()
    return ChannelOut(**channel_dict(item))


@router.get("/channels", response_model=list[ChannelOut])
async def list_channels(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ChannelConfiguration).where(ChannelConfiguration.organization_id == current.organization_id, ChannelConfiguration.workspace_id == workspace_id, ChannelConfiguration.deleted_at.is_(None)).order_by(ChannelConfiguration.priority.asc()))).scalars().all()
    return [ChannelOut(**channel_dict(item)) for item in rows]


@router.post("/identities/resolve", response_model=IdentityOut)
async def resolve_customer_identity(payload: IdentityResolveRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    identity = await resolve_identity(db, current, payload)
    await db.commit()
    return IdentityOut(**identity_dict(identity))


@router.post("/sessions", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def create_session(payload: SessionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = ChannelSession(organization_id=current.organization_id, workspace_id=payload.workspace_id, channel_config_id=payload.channel_config_id, customer_identity_id=payload.customer_identity_id, conversation_id=payload.conversation_id, agent_id=payload.agent_id, external_thread_id=payload.external_thread_id, channel_type=payload.channel_type, subject=payload.subject, context_state=payload.context_state, workflow_state=payload.workflow_state, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return SessionOut(**session_dict(item))


@router.get("/sessions", response_model=list[SessionOut])
async def list_sessions(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ChannelSession).where(ChannelSession.organization_id == current.organization_id, ChannelSession.workspace_id == workspace_id, ChannelSession.deleted_at.is_(None)).order_by(ChannelSession.updated_at.desc()).limit(100))).scalars().all()
    return [SessionOut(**session_dict(item)) for item in rows]


@router.post("/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def send_or_receive_message(payload: MessageCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    message = await create_message(db, current, payload)
    await db.commit()
    return MessageOut(**message_dict(message))


@router.get("/messages", response_model=list[MessageOut])
async def list_messages(workspace_id: UUID, channel_session_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(OmnichannelMessage).where(OmnichannelMessage.organization_id == current.organization_id, OmnichannelMessage.workspace_id == workspace_id)
    if channel_session_id:
        query = query.where(OmnichannelMessage.channel_session_id == channel_session_id)
    rows = (await db.execute(query.order_by(OmnichannelMessage.created_at.desc()).limit(100))).scalars().all()
    return [MessageOut(**message_dict(item)) for item in rows]


@router.post("/delivery-events", response_model=DeliveryOut, status_code=status.HTTP_201_CREATED)
async def track_delivery(payload: DeliveryCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    message = await db.get(OmnichannelMessage, payload.message_id)
    if message is None or message.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Message not found")
    event = DeliveryEvent(organization_id=current.organization_id, workspace_id=payload.workspace_id, message_id=payload.message_id, event_type=payload.event_type, provider=payload.provider, provider_event_id=payload.provider_event_id, status=payload.status, attempt=payload.attempt, latency_ms=payload.latency_ms, error_code=payload.error_code, payload=payload.payload)
    message.status = payload.status
    db.add(event)
    await db.commit()
    return DeliveryOut(**delivery_dict(event))


@router.get("/timeline", response_model=list[TimelineOut])
async def customer_timeline(workspace_id: UUID, customer_identity_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(CustomerTimelineEvent).where(CustomerTimelineEvent.organization_id == current.organization_id, CustomerTimelineEvent.workspace_id == workspace_id)
    if customer_identity_id:
        query = query.where(CustomerTimelineEvent.customer_identity_id == customer_identity_id)
    rows = (await db.execute(query.order_by(CustomerTimelineEvent.occurred_at.desc(), CustomerTimelineEvent.created_at.desc()).limit(150))).scalars().all()
    return [TimelineOut(**timeline_dict(item)) for item in rows]


@router.get("/analytics")
async def omnichannel_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return await analytics(db, current, workspace_id)
