# Storage API

Base path: `/v1/storage`

All endpoints require an authenticated session and organization context.

## Files

- `GET /files?workspace_id=&q=&folder_id=&status=&sort=&direction=` lists files with search, filtering, sorting, and soft-delete awareness.
- `GET /files/{file_id}/download` creates a temporary download or preview URL.
- `PATCH /files/{file_id}/rename` renames the display filename.
- `PATCH /files/{file_id}/move` moves a file to a folder or project context.
- `POST /files/{file_id}/copy` creates a metadata-level copy placeholder.
- `PATCH /files/{file_id}/metadata` updates tags and metadata JSON.
- `DELETE /files/{file_id}` soft deletes a file.
- `POST /files/{file_id}/restore` restores a soft-deleted file.
- `DELETE /files/{file_id}/permanent` removes provider bytes and deletes metadata.

## Folders

- `POST /folders` creates a folder in a workspace, optionally nested under another folder.
- `GET /folders?workspace_id=&parent_folder_id=` lists folders.

## Upload Sessions

- `POST /uploads` initiates a provider-backed upload session.
- `POST /uploads/{upload_session_id}/complete` marks an upload complete and makes the file ready.

## Bulk Actions

- `POST /bulk` supports `delete`, `restore`, and `move` actions for selected file IDs.

## Response Principles

- Responses return stable UUIDs.
- File responses expose metadata only, never provider credentials.
- Provider URLs are temporary references and should be treated as sensitive.
- Errors use the platform error handler and clear HTTP status codes.