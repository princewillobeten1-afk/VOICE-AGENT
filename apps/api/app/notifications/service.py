from datetime import UTC, datetime
from time import perf_counter
from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.notifications.models import DeliveryAttempt, EventLog, EventSubscriber, Notification, NotificationPreference, NotificationTemplate, PlatformEvent

DEFAULT_CATEGORIES = ["success", "warning", "error", "information", "security", "billing", "team", "system"]
DEFAULT_FREQUENCIES = ["instant", "hourly_digest", "daily_digest", "weekly_digest"]
DEFAULT_CHANNELS = [
    {"channel": "in_app", "label": "In-app", "status": "implemented"},
    {"channel": "email", "label": "Email", "status": "architecture_ready"},
    {"channel": "sms", "label": "SMS", "status": "placeholder"},
    {"channel": "push", "label": "Push", "status": "placeholder"},
    {"channel": "whatsapp", "label": "WhatsApp", "status": "placeholder"},
    {"channel": "slack", "label": "Slack", "status": "placeholder"},
    {"channel": "discord", "label": "Discord", "status": "placeholder"},
    {"channel": "webhook", "label": "Webhook", "status": "architecture_ready"},
]
DEFAULT_EVENT_TEMPLATES = {
    "user.created": ("team", "success", "New teammate joined", "{{user_name}} joined {{organization_name}}."),
    "user.logged_in": ("security", "information", "New sign-in", "{{user_name}} signed in at {{timestamp}}."),
    "api_key.created": ("security", "warning", "API key created", "{{user_name}} created an API key for {{organization_name}}."),
    "file.uploaded": ("information", "success", "File uploaded", "{{file_name}} is available in storage."),
    "workflow.executed": ("system", "information", "Workflow executed", "{{workflow_name}} finished with status {{status}}."),
    "billing.updated": ("billing", "information", "Billing updated", "Billing settings changed for {{organization_name}}."),
}


def render_template(template: str | None, values: dict) -> str | None:
    if template is None:
        return None
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    return rendered


def notification_dict(notification: Notification) -> dict:
    return {
        "id": notification.id,
        "organization_id": notification.organization_id,
        "workspace_id": notification.workspace_id,
        "user_id": notification.user_id,
        "event_id": notification.event_id,
        "type": notification.type,
        "category": notification.category,
        "title": notification.title,
        "body": notification.body,
        "severity": notification.severity,
        "status": notification.status,
        "priority": notification.priority,
        "read_at": notification.read_at,
        "archived_at": notification.archived_at,
        "action_url": notification.action_url,
        "metadata_json": notification.metadata_json,
        "created_at": notification.created_at,
    }


def preference_dict(preference: NotificationPreference) -> dict:
    return {
        "email_enabled": preference.email_enabled,
        "in_app_enabled": preference.in_app_enabled,
        "sms_enabled": preference.sms_enabled,
        "push_enabled": preference.push_enabled,
        "webhook_enabled": preference.webhook_enabled,
        "frequency": preference.frequency,
        "quiet_hours": preference.quiet_hours,
        "category_preferences": preference.category_preferences,
        "team_notifications": preference.team_notifications,
    }


async def get_or_create_preferences(db: AsyncSession, current: CurrentUser) -> NotificationPreference:
    result = await db.execute(select(NotificationPreference).where(NotificationPreference.organization_id == current.organization_id, NotificationPreference.user_id == current.user.id))
    preference = result.scalar_one_or_none()
    if preference is not None:
        return preference
    preference = NotificationPreference(organization_id=current.organization_id, user_id=current.user.id)
    db.add(preference)
    await db.flush()
    return preference


async def publish_domain_event(db: AsyncSession, event: DomainEvent) -> PlatformEvent:
    record = PlatformEvent(id=event.id, organization_id=event.organization_id, workspace_id=event.workspace_id, actor_user_id=event.actor_user_id, name=event.name, aggregate_type=event.aggregate_type, aggregate_id=event.aggregate_id, occurred_at=event.occurred_at, event_version=event.event_version, source=event.source, correlation_id=event.correlation_id, causation_id=event.causation_id, idempotency_key=event.idempotency_key, status="published", payload=event.payload, metadata_json=event.metadata)
    db.add(record)
    await db.flush()
    await process_event_for_notifications(db, record)
    return record


async def ensure_notification_subscriber(db: AsyncSession) -> EventSubscriber:
    result = await db.execute(select(EventSubscriber).where(EventSubscriber.name == "notification-engine"))
    subscriber = result.scalar_one_or_none()
    if subscriber is not None:
        return subscriber
    subscriber = EventSubscriber(name="notification-engine", description="Creates in-app notifications from domain events.", event_types=["*"], handler_ref="app.notifications.service.process_event_for_notifications", status="active", max_retries=3)
    db.add(subscriber)
    await db.flush()
    return subscriber


async def process_event_for_notifications(db: AsyncSession, event: PlatformEvent) -> None:
    started = perf_counter()
    subscriber = await ensure_notification_subscriber(db)
    try:
        notification = await create_notification_from_event(db, event)
        if notification:
            db.add(DeliveryAttempt(organization_id=event.organization_id, notification_id=notification.id, event_id=event.id, channel="in_app", status="delivered", provider="internal", attempt_number=1, delivered_at=datetime.now(UTC)))
        event.status = "processed"
        event.processed_at = datetime.now(UTC)
        db.add(EventLog(event_id=event.id, subscriber_id=subscriber.id, status="processed" if notification else "skipped", processing_time_ms=int((perf_counter() - started) * 1000), retry_count=0))
    except Exception as exc:
        event.status = "failed"
        event.error_message = str(exc)
        db.add(EventLog(event_id=event.id, subscriber_id=subscriber.id, status="failed", processing_time_ms=int((perf_counter() - started) * 1000), retry_count=event.retry_count, error_message=str(exc)))
        raise


async def create_notification_from_event(db: AsyncSession, event: PlatformEvent) -> Notification | None:
    if event.organization_id is None or event.workspace_id is None:
        return None
    template = (await db.execute(select(NotificationTemplate).where(NotificationTemplate.organization_id == event.organization_id, NotificationTemplate.event_type == event.name, NotificationTemplate.channel == "in_app", NotificationTemplate.status == "active"))).scalar_one_or_none()
    category, severity, title_template, body_template = DEFAULT_EVENT_TEMPLATES.get(event.name, ("system", "information", event.name.replace(".", " ").title(), "An event occurred in {{organization_name}}."))
    values = {**(event.payload or {}), "timestamp": event.occurred_at, "organization_name": (event.payload or {}).get("organization_name", "this organization")}
    notification = Notification(organization_id=event.organization_id, workspace_id=event.workspace_id, user_id=event.actor_user_id, event_id=event.id, type=event.name, category=template.category if template else category, title=render_template(template.title_template if template else title_template, values) or "VoiceSense update", body=render_template(template.body_template if template else body_template, values), severity=template.severity if template else severity, status="unread", priority="normal", action_url=render_template(template.action_url_template, values) if template else None, metadata_json={"source": event.source, "correlation_id": event.correlation_id})
    db.add(notification)
    await db.flush()
    return notification


async def list_notifications(db: AsyncSession, current: CurrentUser, limit: int, offset: int, status_filter: str | None, category: str | None, q: str | None) -> tuple[list[Notification], int, int]:
    base = select(Notification).where(Notification.organization_id == current.organization_id, Notification.user_id == current.user.id, Notification.deleted_at.is_(None))
    if status_filter:
        base = base.where(Notification.status == status_filter)
    if category:
        base = base.where(Notification.category == category)
    if q:
        base = base.where(or_(Notification.title.ilike(f"%{q}%"), Notification.body.ilike(f"%{q}%")))
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()
    unread = (await db.execute(select(func.count()).select_from(Notification).where(Notification.organization_id == current.organization_id, Notification.user_id == current.user.id, Notification.status == "unread", Notification.deleted_at.is_(None)))).scalar_one()
    items = (await db.execute(base.order_by(Notification.created_at.desc()).limit(limit).offset(offset))).scalars().all()
    return list(items), int(total), int(unread)


async def mark_notification_read(db: AsyncSession, notification: Notification) -> Notification:
    notification.status = "read"
    notification.read_at = datetime.now(UTC)
    return notification


async def mark_all_read(db: AsyncSession, current: CurrentUser) -> int:
    result = await db.execute(update(Notification).where(Notification.organization_id == current.organization_id, Notification.user_id == current.user.id, Notification.status == "unread", Notification.deleted_at.is_(None)).values(status="read", read_at=datetime.now(UTC)))
    return int(result.rowcount or 0)