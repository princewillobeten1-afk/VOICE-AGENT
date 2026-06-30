from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class StorageProvider(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "storage_providers"
    provider: Mapped[str] = mapped_column(String(60), index=True)
    name: Mapped[str] = mapped_column(String(160))
    environment: Mapped[str] = mapped_column(String(40), default="development")
    bucket: Mapped[str | None] = mapped_column(String(180))
    region: Mapped[str | None] = mapped_column(String(80))
    config_ref: Mapped[str | None] = mapped_column(Text)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    is_default: Mapped[bool] = mapped_column(default=False)


class Folder(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "folders"
    __table_args__ = (UniqueConstraint("workspace_id", "parent_folder_id", "name", name="uq_folder_parent_name"),)
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    parent_folder_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("folders.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    path: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class File(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "files"
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    folder_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("folders.id", ondelete="SET NULL"), index=True)
    storage_provider_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("storage_providers.id", ondelete="SET NULL"), index=True)
    provider: Mapped[str] = mapped_column(String(60))
    bucket: Mapped[str] = mapped_column(String(180))
    object_key: Mapped[str] = mapped_column(Text)
    original_name: Mapped[str] = mapped_column(String(300))
    stored_name: Mapped[str] = mapped_column(String(300))
    filename: Mapped[str] = mapped_column(String(300))
    content_type: Mapped[str | None] = mapped_column(String(120))
    extension: Mapped[str | None] = mapped_column(String(24), index=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    checksum: Mapped[str | None] = mapped_column(String(128))
    purpose: Mapped[str] = mapped_column(String(80), default="general")
    status: Mapped[str] = mapped_column(String(40), default="pending")
    version: Mapped[int] = mapped_column(Integer, default=1)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    scanned_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    scan_status: Mapped[str | None] = mapped_column(String(40))


class FileVersion(IdMixin, TimestampMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "file_versions"
    __table_args__ = (UniqueConstraint("file_id", "version", name="uq_file_version"),)
    file_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    provider: Mapped[str] = mapped_column(String(60))
    bucket: Mapped[str] = mapped_column(String(180))
    object_key: Mapped[str] = mapped_column(Text)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    checksum: Mapped[str | None] = mapped_column(String(128))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class UploadSession(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "upload_sessions"
    project_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    folder_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("folders.id", ondelete="SET NULL"), index=True)
    file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    provider: Mapped[str] = mapped_column(String(60), default="local")
    original_name: Mapped[str] = mapped_column(String(300))
    content_type: Mapped[str | None] = mapped_column(String(120))
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(40), default="initiated")
    upload_url_ref: Mapped[str | None] = mapped_column(Text)
    resumable_token_hash: Mapped[str | None] = mapped_column(String(128))
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class FileTag(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "file_tags"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_file_tag_workspace_name"),)
    name: Mapped[str] = mapped_column(String(80))
    color: Mapped[str | None] = mapped_column(String(24))


class FileTagAssignment(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "file_tag_assignments"
    __table_args__ = (UniqueConstraint("file_id", "tag_id", name="uq_file_tag_assignment"),)
    file_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), index=True)
    tag_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("file_tags.id", ondelete="CASCADE"), index=True)


class Upload(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "uploads"
    file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="pending")
    upload_url_ref: Mapped[str | None] = mapped_column(Text)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


Index("ix_storage_providers_provider_env", StorageProvider.provider, StorageProvider.environment, StorageProvider.deleted_at)
Index("ix_folders_workspace_parent", Folder.workspace_id, Folder.parent_folder_id, Folder.deleted_at)
Index("ix_files_workspace_purpose", File.workspace_id, File.purpose, File.deleted_at)
Index("ix_files_workspace_folder", File.workspace_id, File.folder_id, File.deleted_at)
Index("ix_files_workspace_status", File.workspace_id, File.status, File.deleted_at)
Index("ix_file_versions_file_version", FileVersion.file_id, FileVersion.version)
Index("ix_upload_sessions_workspace_status", UploadSession.workspace_id, UploadSession.status, UploadSession.deleted_at)
Index("ix_uploads_workspace_status", Upload.workspace_id, Upload.status, Upload.deleted_at)