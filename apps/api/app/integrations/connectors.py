from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ConnectorContext:
    organization_id: str
    workspace_id: str
    connection_id: str | None = None
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConnectorResult:
    ok: bool
    status: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)


class IntegrationConnector(Protocol):
    key: str
    async def connect(self, context: ConnectorContext, credentials_ref: str | None) -> ConnectorResult: ...
    async def disconnect(self, context: ConnectorContext) -> ConnectorResult: ...
    async def validate(self, context: ConnectorContext) -> ConnectorResult: ...
    async def execute_action(self, context: ConnectorContext, action_key: str, payload: dict[str, Any]) -> ConnectorResult: ...
    async def execute_trigger(self, context: ConnectorContext, trigger_key: str, payload: dict[str, Any]) -> ConnectorResult: ...
    async def refresh_credentials(self, context: ConnectorContext) -> ConnectorResult: ...
    async def test_connection(self, context: ConnectorContext) -> ConnectorResult: ...


class PlaceholderConnector:
    key = "placeholder"
    async def connect(self, context: ConnectorContext, credentials_ref: str | None) -> ConnectorResult:
        return ConnectorResult(ok=True, status="connected", message="Connection accepted by placeholder connector.")
    async def disconnect(self, context: ConnectorContext) -> ConnectorResult:
        return ConnectorResult(ok=True, status="disconnected", message="Connection disconnected.")
    async def validate(self, context: ConnectorContext) -> ConnectorResult:
        return ConnectorResult(ok=True, status="valid", message="Configuration shape is valid.")
    async def execute_action(self, context: ConnectorContext, action_key: str, payload: dict[str, Any]) -> ConnectorResult:
        return ConnectorResult(ok=True, status="queued", message=f"Action {action_key} accepted for future provider execution.", data={"action_key": action_key})
    async def execute_trigger(self, context: ConnectorContext, trigger_key: str, payload: dict[str, Any]) -> ConnectorResult:
        return ConnectorResult(ok=True, status="registered", message=f"Trigger {trigger_key} accepted for future provider execution.", data={"trigger_key": trigger_key})
    async def refresh_credentials(self, context: ConnectorContext) -> ConnectorResult:
        return ConnectorResult(ok=True, status="rotation_ready", message="Credential refresh hook is ready for provider implementation.")
    async def test_connection(self, context: ConnectorContext) -> ConnectorResult:
        return ConnectorResult(ok=True, status="healthy", message="Placeholder connector health check passed.")


class ConnectorRegistry:
    def __init__(self) -> None:
        self._connectors: dict[str, IntegrationConnector] = {"placeholder": PlaceholderConnector()}
    def register(self, key: str, connector: IntegrationConnector) -> None:
        self._connectors[key] = connector
    def get(self, key: str | None) -> IntegrationConnector:
        return self._connectors.get(key or "placeholder", self._connectors["placeholder"])


connector_registry = ConnectorRegistry()