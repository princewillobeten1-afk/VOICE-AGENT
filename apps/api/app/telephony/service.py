from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.service import publish_domain_event
from app.telephony.models import CallMetric, CallQueue, CallRoutingRule, PhoneNumber, SipEndpoint, TelephonyCall, TelephonyCallEvent, TelephonyProviderConfig

PROVIDER_CATALOG = ["twilio", "telnyx", "plivo", "vonage", "signalwire", "amazon_connect", "azure_communication_services", "custom_sip"]


def provider_dict(item: TelephonyProviderConfig) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "provider": item.provider, "status": item.status, "priority": item.priority, "region": item.region, "secret_ref": item.secret_ref, "capabilities": item.capabilities, "failover_policy": item.failover_policy, "health_state": item.health_state, "config": item.config, "created_at": item.created_at, "updated_at": item.updated_at}


def number_dict(item: PhoneNumber) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "provider_config_id": item.provider_config_id, "assigned_agent_id": item.assigned_agent_id, "queue_id": item.queue_id, "e164": item.e164, "label": item.label, "number_type": item.number_type, "country": item.country, "region": item.region, "status": item.status, "routing_config": item.routing_config, "compliance_config": item.compliance_config, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


def queue_dict(item: CallQueue) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "slug": item.slug, "priority": item.priority, "overflow_policy": item.overflow_policy, "assignment_policy": item.assignment_policy, "estimated_wait_seconds": item.estimated_wait_seconds, "status": item.status, "analytics_state": item.analytics_state, "created_at": item.created_at, "updated_at": item.updated_at}


def call_dict(item: TelephonyCall) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "provider_config_id": item.provider_config_id, "phone_number_id": item.phone_number_id, "queue_id": item.queue_id, "voice_session_id": item.voice_session_id, "conversation_id": item.conversation_id, "workflow_run_id": item.workflow_run_id, "agent_id": item.agent_id, "provider_call_id": item.provider_call_id, "direction": item.direction, "call_type": item.call_type, "status": item.status, "from_number": item.from_number, "to_number": item.to_number, "customer_ref": item.customer_ref, "routing_result": item.routing_result, "timeline_state": item.timeline_state, "cost_state": item.cost_state, "started_at": item.started_at, "answered_at": item.answered_at, "ended_at": item.ended_at, "duration_seconds": item.duration_seconds, "end_reason": item.end_reason, "created_at": item.created_at}


def event_dict(item: TelephonyCallEvent) -> dict:
    return {"id": item.id, "call_id": item.call_id, "event_type": item.event_type, "sequence_number": item.sequence_number, "source": item.source, "payload": item.payload, "latency_ms": item.latency_ms, "created_at": item.created_at}


async def emit_call_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, call_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"telephony.{name}", aggregate_type="telephony_call", aggregate_id=call_id, source="telephony-platform", payload=payload, metadata={"backbone": "telephony"}))


async def choose_provider(db: AsyncSession, current: CurrentUser, workspace_id: UUID, region: str | None = None) -> TelephonyProviderConfig | None:
    query = select(TelephonyProviderConfig).where(TelephonyProviderConfig.organization_id == current.organization_id, TelephonyProviderConfig.workspace_id == workspace_id, TelephonyProviderConfig.status == "enabled", TelephonyProviderConfig.deleted_at.is_(None))
    if region:
        query = query.where((TelephonyProviderConfig.region == region) | (TelephonyProviderConfig.region.is_(None)))
    return (await db.execute(query.order_by(TelephonyProviderConfig.priority.asc()).limit(1))).scalar_one_or_none()


async def route_call(db: AsyncSession, current: CurrentUser, workspace_id: UUID, to_number: str | None, metadata: dict) -> dict:
    number = None
    if to_number:
        number = (await db.execute(select(PhoneNumber).where(PhoneNumber.organization_id == current.organization_id, PhoneNumber.workspace_id == workspace_id, PhoneNumber.e164 == to_number, PhoneNumber.deleted_at.is_(None)))).scalar_one_or_none()
    rule_query = select(CallRoutingRule).where(CallRoutingRule.organization_id == current.organization_id, CallRoutingRule.workspace_id == workspace_id, CallRoutingRule.status == "active", CallRoutingRule.deleted_at.is_(None))
    if number:
        rule_query = rule_query.where((CallRoutingRule.phone_number_id == number.id) | (CallRoutingRule.phone_number_id.is_(None)))
    rule = (await db.execute(rule_query.order_by(CallRoutingRule.priority.asc()).limit(1))).scalar_one_or_none()
    return {"phone_number_id": str(number.id) if number else None, "queue_id": str(rule.queue_id) if rule and rule.queue_id else str(number.queue_id) if number and number.queue_id else None, "destination_type": rule.destination_type if rule else "agent", "destination_ref": rule.destination_ref if rule else str(number.assigned_agent_id) if number and number.assigned_agent_id else None, "reason": "matched routing rule" if rule else "number default route", "metadata": metadata}


async def create_call(db: AsyncSession, current: CurrentUser, payload) -> TelephonyCall:
    provider = await choose_provider(db, current, payload.workspace_id, payload.region)
    routing = await route_call(db, current, payload.workspace_id, payload.to_number, payload.metadata_json)
    call = TelephonyCall(organization_id=current.organization_id, workspace_id=payload.workspace_id, provider_config_id=provider.id if provider else None, phone_number_id=UUID(routing["phone_number_id"]) if routing.get("phone_number_id") else None, queue_id=UUID(routing["queue_id"]) if routing.get("queue_id") else None, agent_id=UUID(routing["destination_ref"]) if routing.get("destination_type") == "agent" and routing.get("destination_ref") else payload.agent_id, direction=payload.direction, call_type=payload.call_type, status="started", from_number=payload.from_number, to_number=payload.to_number, customer_ref=payload.customer_ref, routing_result=routing, timeline_state={"events": ["call.started"]}, cost_state={"estimated": True}, started_at=datetime.now(UTC))
    db.add(call)
    await db.flush()
    db.add(TelephonyCallEvent(organization_id=current.organization_id, workspace_id=payload.workspace_id, call_id=call.id, event_type="call.started", sequence_number=1, source="api", payload={"provider": provider.provider if provider else "unassigned", "routing": routing}))
    await emit_call_event(db, current, "call.started", payload.workspace_id, call.id, {"direction": payload.direction, "routing": routing})
    return call


async def analytics(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    calls = int((await db.execute(select(func.count()).select_from(TelephonyCall).where(TelephonyCall.organization_id == current.organization_id, TelephonyCall.workspace_id == workspace_id))).scalar_one() or 0)
    active = int((await db.execute(select(func.count()).select_from(TelephonyCall).where(TelephonyCall.organization_id == current.organization_id, TelephonyCall.workspace_id == workspace_id, TelephonyCall.status.in_(["started", "answered", "queued", "held"])))).scalar_one() or 0)
    queues = int((await db.execute(select(func.count()).select_from(CallQueue).where(CallQueue.organization_id == current.organization_id, CallQueue.workspace_id == workspace_id, CallQueue.deleted_at.is_(None)))).scalar_one() or 0)
    numbers = int((await db.execute(select(func.count()).select_from(PhoneNumber).where(PhoneNumber.organization_id == current.organization_id, PhoneNumber.workspace_id == workspace_id, PhoneNumber.deleted_at.is_(None)))).scalar_one() or 0)
    avg_duration = (await db.execute(select(func.avg(TelephonyCall.duration_seconds)).where(TelephonyCall.organization_id == current.organization_id, TelephonyCall.workspace_id == workspace_id, TelephonyCall.duration_seconds.is_not(None)))).scalar_one_or_none()
    return {"calls": calls, "active_calls": active, "queues": queues, "phone_numbers": numbers, "average_duration_seconds": int(avg_duration) if avg_duration else None, "provider_catalog": PROVIDER_CATALOG, "streaming": "delegated_to_voice_engine", "recording": "metadata_and_policy_ready"}
