# Knowledge API

Base path: `/v1/knowledge`

## Dashboard

- `GET /dashboard?workspace_id=...`

## Knowledge Bases

- `GET /bases?workspace_id=...`
- `POST /bases`
- `PATCH /bases/{knowledge_base_id}`
- `POST /bases/{knowledge_base_id}/publish`

## Sources and Websites

- `POST /sources`
- `POST /websites`
- `POST /sync`

## Documents

- `GET /documents?workspace_id=...`
- `POST /documents`
- `PATCH /documents/{document_id}`
- `POST /documents/{document_id}/publish`
- `GET /documents/{document_id}/versions`

## Organization

- `POST /categories`
- `POST /permissions`
- `POST /search`