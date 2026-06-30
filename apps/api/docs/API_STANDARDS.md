# API Standards

## Versioning

All public REST endpoints live under `/v1`. Breaking changes require a new version prefix.

## Response Format

New APIs should return a consistent envelope:

```json
{
  "ok": true,
  "data": {},
  "message": null,
  "request_id": "..."
}
```

Errors should return:

```json
{
  "ok": false,
  "error": {
    "code": "validation_error",
    "message": "Invalid request",
    "field": "email"
  },
  "request_id": "..."
}
```

## Pagination

Use `page` and `page_size` for standard list endpoints. Maximum `page_size` is 200.

```text
GET /v1/conversations?page=1&page_size=25
```

## Filtering, Sorting, Search

- Filtering: explicit query params such as `status`, `channel`, `agent_id`.
- Sorting: `sort=created_at` and `direction=desc`.
- Search: `q=<term>`.
- Date ranges: `created_after`, `created_before`.

## Validation

Use Pydantic schemas at API boundaries. Do not trust client-provided tenant IDs without membership checks.

## Idempotency

Future mutation endpoints that may be retried should support an `Idempotency-Key` header.

## Security

Protected endpoints require bearer tokens and must enforce organization/workspace access in the service layer.