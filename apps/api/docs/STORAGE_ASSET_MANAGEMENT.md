# Storage and Asset Management Architecture

VoiceSense storage is the durable asset layer for documents, PDFs, images, audio, archives, exports, reports, and future platform-generated artifacts. It is intentionally separate from AI indexing, RAG, transcription, and processing pipelines.

## Goals

- Keep file metadata organization-scoped and workspace-scoped.
- Support provider portability across local disk, S3, Cloudflare R2, Google Cloud Storage, and Azure Blob Storage.
- Provide predictable file lifecycle operations: upload, download, preview, rename, move, copy, soft delete, restore, and permanent delete.
- Preserve auditability for all sensitive mutations.
- Make bulk actions and resumable upload sessions first-class platform concepts.

## Domain Model

- `storage_providers`: provider registry, environment, bucket, region, capabilities, and secret reference pointer.
- `folders`: hierarchical organization of workspace assets.
- `files`: canonical metadata record for each asset and current version.
- `file_versions`: immutable metadata for previous object versions.
- `upload_sessions`: short-lived upload lifecycle state with resumable token hash and expiration.
- `file_tags`: reusable workspace tags.
- `file_tag_assignments`: normalized file-to-tag relationship.

## Provider Abstraction

Application code calls `StorageProviderAdapter` rather than provider SDKs directly.

Current adapter responsibilities:

- `create_upload_url(request)`: returns an upload destination or local upload reference.
- `create_download_url(object_key)`: returns a temporary download/preview URL.
- `delete_object(object_key)`: deletes provider bytes during permanent deletion.

The local adapter is implemented for development. Cloud adapters currently use placeholders so the interface is stable while credential, networking, and IaC decisions remain isolated.

## Upload Lifecycle

1. Client requests `POST /v1/storage/uploads` with workspace, optional folder, filename, content type, size, purpose, provider, and tags.
2. API validates file policy and creates a `files` row with `status = uploading`.
3. API creates an `upload_sessions` row with expiration and hashed resumable token.
4. Client uploads bytes to the returned provider URL/reference.
5. Client calls `POST /v1/storage/uploads/{id}/complete`.
6. API marks the file `ready`, stores checksum/size if provided, and audits completion.

## Security Model

- All reads and writes are organization scoped through the authenticated user context.
- Storage routes use RBAC permissions: read, write, and delete.
- Sensitive provider credentials must live outside the database; `config_ref` points to a secret manager reference.
- Upload sessions expire and store only hashed resumable tokens.
- File metadata mutations emit audit events.
- Soft delete is the default destructive action; permanent delete requires stronger delete permission.

## Non-Goals

- No AI indexing.
- No RAG ingestion.
- No audio transcription.
- No malware scanning engine implementation yet.
- No real cloud SDK wiring until provider credentials and infrastructure are selected.