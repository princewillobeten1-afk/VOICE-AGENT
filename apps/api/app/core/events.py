from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession


class EventName(StrEnum):
    USER_CREATED = "user.created"
    USER_LOGGED_IN = "user.logged_in"
    ORGANIZATION_CREATED = "organization.created"
    WORKSPACE_CREATED = "workspace.created"
    API_KEY_CREATED = "api_key.created"
    FILE_UPLOADED = "file.uploaded"
    AGENT_CREATED = "agent.created"
    CONVERSATION_STARTED = "conversation.started"
    CONVERSATION_ENDED = "conversation.ended"
    CALL_STARTED = "call.started"
    CALL_FINISHED = "call.finished"
    KNOWLEDGE_UPLOADED = "knowledge.uploaded"
    WORKFLOW_EXECUTED = "workflow.executed"
    INTEGRATION_CONNECTED = "integration.connected"
    BILLING_UPDATED = "billing.updated"


class DomainEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    organization_id: UUID | None = None
    workspace_id: UUID | None = None
    actor_user_id: UUID | None = None
    aggregate_type: str
    aggregate_id: UUID
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    event_version: int = 1
    source: str = "platform"
    correlation_id: str | None = None
    causation_id: UUID | None = None
    idempotency_key: str | None = None


class EventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None:
        ...


class InMemoryEventPublisher:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    async def publish(self, event: DomainEvent) -> None:
        self.events.append(event)


class DurableEventPublisher:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def publish(self, event: DomainEvent) -> None:
        from app.notifications.service import publish_domain_event
        await publish_domain_event(self.db, event)