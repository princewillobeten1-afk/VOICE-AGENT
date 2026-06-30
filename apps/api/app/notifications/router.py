from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.events import DomainEvent
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.notifications.models import EventLog, Notification, PlatformEvent
from app.notifications.schemas import EventLogOut, EventOut, EventPublish, MarkAllReadResult, NotificationList, NotificationOut, NotificationPreferenceOut, NotificationPreferenceUpdate, NotificationSettings, UnreadCount
from app.notifications.service import DEFAULT_CATEGORIES, DEFAULT_CHANNELS, DEFAULT_FREQUENCIES, get_or_create_preferences, list_notifications, mark_all_read, mark_notification_read, notification_dict, preference_dict, publish_domain_event

router = APIRouter(prefix="/notifications", tags=["notifications"])
events_router = APIRouter(prefix="/events", tags=["events"])


def notification_out(notification: Notification) -> NotificationOut:
    return NotificationOut(**notification_dict(notification))


def event_out(event: PlatformEvent) -> EventOut:
    return EventOut(id=event.id, name=event.name, organization_id=event.organization_id, workspace_id=event.workspace_id, aggregate_type=event.aggregate_type, aggregate_id=event.aggregate_id, occurred_at=event.occurred_at, event_version=event.event_version, correlation_id=event.correlation_id, status=event.status)


@router.get("", response_model=NotificationList)
async def get_notifications(limit: int = Query(default=25, ge=1, le=100), offset: int = Query(default=0, ge=0), status_filter: str | None = Query(default=None, alias="status"), category: str | None = None, q: str | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    items, total, unread = await list_notifications(db, current, limit, offset, status_filter, category, q)
    return NotificationList(items=[notification_out(item) for item in items], total=total, unread_count=unread, limit=limit, offset=offset)


@router.get("/unread-count", response_model=UnreadCount)
async def unread_count(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    _, _, unread = await list_notifications(db, current, 1, 0, None, None, None)
    return UnreadCount(unread_count=unread)


@router.patch("/{notification_id}/read", response_model=NotificationOut)
async def read_notification(notification_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    notification = (await db.execute(select(Notification).where(Notification.id == notification_id, Notification.organization_id == current.organization_id, Notification.user_id == current.user.id, Notification.deleted_at.is_(None)))).scalar_one_or_none()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    await mark_notification_read(db, notification)
    await audit(db, "notification.read", current.user.id, current.organization_id, "notification", notification.id)
    await db.commit()
    return notification_out(notification)


@router.post("/read-all", response_model=MarkAllReadResult)
async def read_all_notifications(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    updated = await mark_all_read(db, current)
    await audit(db, "notification.read_all", current.user.id, current.organization_id, metadata={"updated": updated})
    await db.commit()
    return MarkAllReadResult(updated=updated)


@router.post("/{notification_id}/archive", response_model=NotificationOut)
async def archive_notification(notification_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    notification = (await db.execute(select(Notification).where(Notification.id == notification_id, Notification.organization_id == current.organization_id, Notification.user_id == current.user.id, Notification.deleted_at.is_(None)))).scalar_one_or_none()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.status = "archived"
    notification.archived_at = datetime.now(UTC)
    await audit(db, "notification.archived", current.user.id, current.organization_id, "notification", notification.id)
    await db.commit()
    return notification_out(notification)


@router.delete("/{notification_id}", status_code=204)
async def delete_notification(notification_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    notification = (await db.execute(select(Notification).where(Notification.id == notification_id, Notification.organization_id == current.organization_id, Notification.user_id == current.user.id, Notification.deleted_at.is_(None)))).scalar_one_or_none()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.deleted_at = datetime.now(UTC)
    notification.status = "deleted"
    await audit(db, "notification.deleted", current.user.id, current.organization_id, "notification", notification.id)
    await db.commit()


@router.get("/preferences", response_model=NotificationPreferenceOut)
async def get_preferences(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    preference = await get_or_create_preferences(db, current)
    await db.commit()
    return NotificationPreferenceOut(**preference_dict(preference))


@router.put("/preferences", response_model=NotificationPreferenceOut)
async def update_preferences(payload: NotificationPreferenceUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    preference = await get_or_create_preferences(db, current)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(preference, field, value)
    await audit(db, "notification.preferences.updated", current.user.id, current.organization_id, "notification_preference", preference.id)
    await db.commit()
    return NotificationPreferenceOut(**preference_dict(preference))


@router.get("/settings", response_model=NotificationSettings)
async def notification_settings(current: CurrentUser = Depends(require_permission(Permission.ORG_READ))):
    return NotificationSettings(channels=DEFAULT_CHANNELS, categories=DEFAULT_CATEGORIES, frequencies=DEFAULT_FREQUENCIES, real_time_transports=["websocket_ready", "sse_ready"])


@events_router.post("", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def publish_event(payload: EventPublish, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    event = DomainEvent(name=payload.name, organization_id=current.organization_id, workspace_id=payload.workspace_id, actor_user_id=current.user.id, aggregate_type=payload.aggregate_type, aggregate_id=payload.aggregate_id, payload=payload.payload, metadata=payload.metadata_json, correlation_id=payload.correlation_id, event_version=payload.event_version, source=payload.source)
    record = await publish_domain_event(db, event)
    await audit(db, "event.published", current.user.id, current.organization_id, "event", record.id, metadata={"event_name": record.name})
    await db.commit()
    return event_out(record)


@events_router.get("", response_model=list[EventOut])
async def list_events(limit: int = Query(default=25, ge=1, le=100), offset: int = Query(default=0, ge=0), name: str | None = None, current: CurrentUser = Depends(require_permission(Permission.AUDIT_READ)), db: AsyncSession = Depends(get_db)):
    query = select(PlatformEvent).where(PlatformEvent.organization_id == current.organization_id)
    if name:
        query = query.where(PlatformEvent.name == name)
    items = (await db.execute(query.order_by(PlatformEvent.occurred_at.desc()).limit(limit).offset(offset))).scalars().all()
    return [event_out(item) for item in items]


@events_router.get("/{event_id}/logs", response_model=list[EventLogOut])
async def event_logs(event_id: UUID, current: CurrentUser = Depends(require_permission(Permission.AUDIT_READ)), db: AsyncSession = Depends(get_db)):
    event = await db.get(PlatformEvent, event_id)
    if event is None or event.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Event not found")
    logs = (await db.execute(select(EventLog).where(EventLog.event_id == event_id).order_by(EventLog.created_at.desc()))).scalars().all()
    return [EventLogOut(id=log.id, event_id=log.event_id, status=log.status, retry_count=log.retry_count, processing_time_ms=log.processing_time_ms, error_message=log.error_message, created_at=log.created_at) for log in logs]