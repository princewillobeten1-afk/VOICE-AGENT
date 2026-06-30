# Storage Strategy

VoiceSense storage must support documents, images, PDFs, generated files, audio, and call recordings without vendor lock-in.

## Abstraction

The database stores file metadata in `files` and provider references such as `provider`, `bucket`, and `object_key`. Application code should access files through storage adapters rather than direct provider SDK calls inside domain services.

## Provider Examples

- Local filesystem for development.
- S3-compatible object storage for production.
- Cloudflare R2, AWS S3, GCS, or Azure Blob through adapters.

## File Purposes

Examples:

- `document`
- `audio_recording`
- `avatar`
- `generated_export`
- `knowledge_source`

## Security

- Use signed URLs for direct upload/download.
- Keep object storage private by default.
- Scan uploads before use when supported.
- Store checksums and content types.
- Enforce organization/workspace authorization before issuing access URLs.