from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class EventPublish(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    workspace_id: UUID | None = None
    aggregate_type: str = Field(min_length=2, max_length=80)
    aggregate_id: UUID
    payload: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)
    correlation_id: str | None = Field(default=None, max_length=120)
    event_version: int = Field(default=1, ge=1)
    source: str = Field(default="api", max_length=80)


class EventOut(BaseModel):
    id: UUID
    name: str
    organization_id: UUID | None
    workspace_id: UUID | None
    aggregate_type: str
    aggregate_id: UUID
    occurred_at: datetime
    event_version: int
    correlation_id: str | None = None
    status: str


class NotificationOut(BaseModel):
    id: UUID
    organization_id: UUID
    workspace_id: UUID
    user_id: UUID | None = None
    event_id: UUID | None = None
    type: str
    category: str
    title: str
    body: str | None = None
    severity: str
    status: str
    priority: str
    read_at: datetime | None = None
    archived_at: datetime | None = None
    action_url: str | None = None
    metadata_json: dict
    created_at: datetime


class NotificationList(BaseModel):
    items: list[NotificationOut]
    total: int
    unread_count: int
    limit: int
    offset: int


class UnreadCount(BaseModel):
    unread_count: int


class NotificationPreferenceOut(BaseModel):
    email_enabled: bool
    in_app_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    webhook_enabled: bool
    frequency: str
    quiet_hours: dict
    category_preferences: dict
    team_notifications: bool


class NotificationPreferenceUpdate(BaseModel):
    email_enabled: bool | None = None
    in_app_enabled: bool | None = None
    sms_enabled: bool | None = None
    push_enabled: bool | None = None
    webhook_enabled: bool | None = None
    frequency: str | None = Field(default=None, max_length=40)
    quiet_hours: dict | None = None
    category_preferences: dict | None = None
    team_notifications: bool | None = None


class NotificationSettings(BaseModel):
    channels: list[dict]
    categories: list[str]
    frequencies: list[str]
    real_time_transports: list[str]


class MarkAllReadResult(BaseModel):
    updated: int


class EventLogOut(BaseModel):
    id: UUID
    event_id: UUID
    status: str
    retry_count: int
    processing_time_ms: int | None = None
    error_message: str | None = None
    created_at: datetime