# Memory API

Base path: `/v1/memory`

## Core

- `GET /memory?workspace_id=...`
- `POST /memory`
- `GET /memory/{memory_id}`
- `PATCH /memory/{memory_id}`
- `DELETE /memory/{memory_id}`
- `POST /memory/search`

## Actions

- `POST /memory/{memory_id}/pin`
- `POST /memory/{memory_id}/archive`
- `POST /memory/{memory_id}/restore`
- `POST /memory/{memory_id}/forget`
- `POST /memory/{memory_id}/merge`
- `POST /memory/{memory_id}/links`

## Governance

- `GET /memory/categories`
- `POST /memory/categories`
- `GET /memory/policies`
- `POST /memory/policies`
- `GET /memory/analytics`