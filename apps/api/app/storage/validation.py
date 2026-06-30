ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/json",
    "image/png",
    "image/jpeg",
    "image/svg+xml",
    "image/webp",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "application/zip",
}

MAX_FILE_SIZE_BYTES = 250 * 1024 * 1024


def validate_upload(content_type: str | None, size_bytes: int | None) -> None:
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Unsupported file type: {content_type}")
    if size_bytes is not None and size_bytes > MAX_FILE_SIZE_BYTES:
        raise ValueError("File exceeds maximum size of 250MB")