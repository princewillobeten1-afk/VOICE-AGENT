from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class RealtimeNotificationMessage:
    organization_id: UUID
    user_id: UUID | None
    event: str
    payload: dict


class RealtimeTransport(Protocol):
    async def publish(self, message: RealtimeNotificationMessage) -> None:
        ...


class NoopRealtimeTransport:
    async def publish(self, message: RealtimeNotificationMessage) -> None:
        return None


class RealtimeHub:
    def __init__(self, transport: RealtimeTransport | None = None) -> None:
        self.transport = transport or NoopRealtimeTransport()

    async def publish_notification(self, message: RealtimeNotificationMessage) -> None:
        await self.transport.publish(message)


realtime_hub = RealtimeHub()