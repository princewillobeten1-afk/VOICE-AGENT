# Integration API

Base path: `/v1/integrations`

## Marketplace

- `GET /marketplace` returns category, featured, available, and installed summaries.
- `GET /available` lists available integrations with search and category filters.

## Connections

- `GET /connections?workspace_id=` lists installed connections.
- `POST /connections` creates a connection.
- `PATCH /connections/{connection_id}` updates connection settings.
- `DELETE /connections/{connection_id}` soft deletes a connection.
- `POST /connections/{connection_id}/enable` enables a connection.
- `POST /connections/{connection_id}/disable` disables a connection.
- `POST /connections/{connection_id}/test` runs a connector health test.
- `POST /connections/{connection_id}/reconnect` requests reconnect.

## Credentials

- `POST /connections/{connection_id}/credentials/rotate` rotates credential references and fingerprints.

## Execution

- `POST /connections/{connection_id}/actions` executes a connector action placeholder.
- `POST /connections/{connection_id}/triggers` fires/registers a connector trigger placeholder.

## Observability

- `GET /connections/{connection_id}/health` returns health check history.
- `GET /connections/{connection_id}/logs` returns connection lifecycle and execution logs.