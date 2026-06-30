from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event
from app.omnichannel.models import ChannelConfiguration, ChannelSession, CustomerIdentity, CustomerTimelineEvent, DeliveryEvent, OmnichannelMessage

CHANNEL_CATALOG = ["voice", "web_chat", "whatsapp", "sms", "email", "slack", "microsoft_teams", "telegram", "facebook_messenger", "instagram", "mobile_sdk", "discord"]
PROVIDER_CATALOG = ["telephony", "twilio", "telnyx", "sendgrid", "mailgun", "whatsapp_business", "slack", "microsoft_graph", "telegram", "meta", "custom_webhook", "mobile_sdk"]


def channel_dict(item: ChannelConfiguration) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "channel_type": item.channel_type, "provider": item.provider, "status": item.status, "priority": item.priority, "region": item.region, "secret_ref": item.secret_ref, "capabilities": item.capabilities, "formatter_policy": item.formatter_policy, "health_state": item.health_state, "config": item.config, "created_at": item.created_at, "updated_at": item.updated_at}


def identity_dict(item: CustomerIdentity) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "display_name": item.display_name, "identity_type": item.identity_type, "identity_value": item.identity_value, "canonical_customer_ref": item.canonical_customer_ref, "confidence_score": float(item.confidence_score) if item.confidence_score is not None else None, "source": item.source, "merge_state": item.merge_state, "profile": item.profile, "preferences": item.preferences, "created_at": item.created_at, "updated_at": item.updated_at}


def session_dict(item: ChannelSession) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "channel_config_id": item.channel_config_id, "customer_identity_id": item.customer_identity_id, "conversation_id": item.conversation_id, "agent_id": item.agent_id, "external_thread_id": item.external_thread_id, "channel_type": item.channel_type, "status": item.status, "subject": item.subject, "context_state": item.context_state, "workflow_state": item.workflow_state, "last_message_at": item.last_message_at, "expires_at": item.expires_at, "created_at": item.created_at, "updated_at": item.updated_at}


def message_dict(item: OmnichannelMessage) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "channel_session_id": item.channel_session_id, "channel_config_id": item.channel_config_id, "customer_identity_id": item.customer_identity_id, "conversation_id": item.conversation_id, "agent_id": item.agent_id, "direction": item.direction, "channel_type": item.channel_type, "message_type": item.message_type, "provider_message_id": item.provider_message_id, "sender_ref": item.sender_ref, "recipient_ref": item.recipient_ref, "subject": item.subject, "text_body": item.text_body, "normalized_payload": item.normalized_payload, "formatted_payload": item.formatted_payload, "status": item.status, "sent_at": item.sent_at, "delivered_at": item.delivered_at, "read_at": item.read_at, "created_at": item.created_at, "updated_at": item.updated_at}


def delivery_dict(item: DeliveryEvent) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "message_id": item.message_id, "event_type": item.event_type, "provider": item.provider, "provider_event_id": item.provider_event_id, "status": item.status, "attempt": item.attempt, "latency_ms": item.latency_ms, "error_code": item.error_code, "payload": item.payload, "created_at": item.created_at}


def timeline_dict(item: CustomerTimelineEvent) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "customer_identity_id": item.customer_identity_id, "channel_session_id": item.channel_session_id, "message_id": item.message_id, "conversation_id": item.conversation_id, "event_type": item.event_type, "channel_type": item.channel_type, "title": item.title, "summary": item.summary, "event_payload": item.event_payload, "occurred_at": item.occurred_at, "created_at": item.created_at}


async def emit_event(db: AsyncSession, current: CurrentUser, workspace_id: UUID, name: str, aggregate_type: str, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"omnichannel.{name}", aggregate_type=aggregate_type, aggregate_id=aggregate_id, source="omnichannel-platform", payload=payload, metadata={"layer": "omnichannel"}))


async def resolve_identity(db: AsyncSession, current: CurrentUser, payload) -> CustomerIdentity:
    existing = (await db.execute(select(CustomerIdentity).where(CustomerIdentity.organization_id == current.organization_id, CustomerIdentity.workspace_id == payload.workspace_id, CustomerIdentity.identity_type == payload.identity_type, CustomerIdentity.identity_value == payload.identity_value, CustomerIdentity.deleted_at.is_(None)))).scalar_one_or_none()
    if existing:
        existing.display_name = payload.display_name or existing.display_name
        existing.canonical_customer_ref = payload.canonical_customer_ref or existing.canonical_customer_ref
        existing.profile = {**(existing.profile or {}), **payload.profile}
        existing.preferences = {**(existing.preferences or {}), **payload.preferences}
        return existing
    identity = CustomerIdentity(organization_id=current.organization_id, workspace_id=payload.workspace_id, display_name=payload.display_name, identity_type=payload.identity_type, identity_value=payload.identity_value, canonical_customer_ref=payload.canonical_customer_ref or payload.identity_value, confidence_score=1, source="identity_resolver", profile=payload.profile, preferences=payload.preferences, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(identity)
    await db.flush()
    return identity


async def create_message(db: AsyncSession, current: CurrentUser, payload) -> OmnichannelMessage:
    now = datetime.now(UTC)
    status = "received" if payload.direction == "inbound" else "sent"
    message = OmnichannelMessage(organization_id=current.organization_id, workspace_id=payload.workspace_id, channel_session_id=payload.channel_session_id, channel_config_id=payload.channel_config_id, customer_identity_id=payload.customer_identity_id, conversation_id=payload.conversation_id, agent_id=payload.agent_id, direction=payload.direction, channel_type=payload.channel_type, message_type=payload.message_type, sender_ref=payload.sender_ref, recipient_ref=payload.recipient_ref, subject=payload.subject, text_body=payload.text_body, normalized_payload=payload.normalized_payload, formatted_payload=payload.formatted_payload or {"channel": payload.channel_type, "body": payload.text_body}, status=status, sent_at=now if payload.direction == "outbound" else None)
    db.add(message)
    await db.flush()
    if payload.channel_session_id:
        session = await db.get(ChannelSession, payload.channel_session_id)
        if session and session.organization_id == current.organization_id:
            session.last_message_at = now
    db.add(CustomerTimelineEvent(organization_id=current.organization_id, workspace_id=payload.workspace_id, customer_identity_id=payload.customer_identity_id, channel_session_id=payload.channel_session_id, message_id=message.id, conversation_id=payload.conversation_id, event_type=f"message.{payload.direction}", channel_type=payload.channel_type, title="Message received" if payload.direction == "inbound" else "Message sent", summary=payload.text_body, event_payload={"message_type": payload.message_type}, occurred_at=now))
    await emit_event(db, current, payload.workspace_id, "message.created", "omnichannel_message", message.id, {"direction": payload.direction, "channel_type": payload.channel_type})
    return message


async def analytics(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    channels = int((await db.execute(select(func.count()).select_from(ChannelConfiguration).where(ChannelConfiguration.organization_id == current.organization_id, ChannelConfiguration.workspace_id == workspace_id, ChannelConfiguration.deleted_at.is_(None)))).scalar_one() or 0)
    sessions = int((await db.execute(select(func.count()).select_from(ChannelSession).where(ChannelSession.organization_id == current.organization_id, ChannelSession.workspace_id == workspace_id, ChannelSession.deleted_at.is_(None)))).scalar_one() or 0)
    messages = int((await db.execute(select(func.count()).select_from(OmnichannelMessage).where(OmnichannelMessage.organization_id == current.organization_id, OmnichannelMessage.workspace_id == workspace_id))).scalar_one() or 0)
    identities = int((await db.execute(select(func.count()).select_from(CustomerIdentity).where(CustomerIdentity.organization_id == current.organization_id, CustomerIdentity.workspace_id == workspace_id, CustomerIdentity.deleted_at.is_(None)))).scalar_one() or 0)
    delivered = int((await db.execute(select(func.count()).select_from(DeliveryEvent).where(DeliveryEvent.organization_id == current.organization_id, DeliveryEvent.workspace_id == workspace_id, DeliveryEvent.status == "delivered"))).scalar_one() or 0)
    return {"channels": channels, "sessions": sessions, "messages": messages, "customer_identities": identities, "delivered_events": delivered, "channel_catalog": CHANNEL_CATALOG, "provider_catalog": PROVIDER_CATALOG, "smart_channel_selection": "policy_ready", "timeline": "unified"}
