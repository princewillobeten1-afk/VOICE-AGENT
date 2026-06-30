from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class FolderCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID | None = None
    parent_folder_id: UUID | None = None
    name: str = Field(min_length=1, max_length=180)


class FolderOut(BaseModel):
    id: UUID
    workspace_id: UUID
    project_id: UUID | None = None
    parent_folder_id: UUID | None = None
    name: str
    path: str
    created_at: datetime


class FileOut(BaseModel):
    id: UUID
    workspace_id: UUID
    project_id: UUID | None = None
    folder_id: UUID | None = None
    original_name: str
    stored_name: str
    content_type: str | None = None
    extension: str | None = None
    size_bytes: int | None = None
    provider: str
    purpose: str
    status: str
    version: int
    tags: list[str]
    checksum: str | None = None
    created_at: datetime
    deleted_at: datetime | None = None


class UploadInitiate(BaseModel):
    workspace_id: UUID
    project_id: UUID | None = None
    folder_id: UUID | None = None
    original_name: str = Field(min_length=1, max_length=300)
    content_type: str | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    purpose: str = "general"
    provider: str = "local"
    tags: list[str] = Field(default_factory=list)


class UploadInitiated(BaseModel):
    upload_session_id: UUID
    file: FileOut
    upload_url: str
    expires_in: int


class UploadComplete(BaseModel):
    checksum: str | None = None
    size_bytes: int | None = None


class FileRename(BaseModel):
    name: str = Field(min_length=1, max_length=300)


class FileMove(BaseModel):
    folder_id: UUID | None = None
    project_id: UUID | None = None


class FileCopy(BaseModel):
    folder_id: UUID | None = None
    name: str | None = Field(default=None, max_length=300)


class FileMetadataUpdate(BaseModel):
    tags: list[str] | None = None
    metadata_json: dict | None = None


class FileDownload(BaseModel):
    file_id: UUID
    url: str
    expires_in: int


class BulkAction(BaseModel):
    file_ids: list[UUID]
    action: str
    folder_id: UUID | None = None


class BulkActionResult(BaseModel):
    affected: int
    action: str