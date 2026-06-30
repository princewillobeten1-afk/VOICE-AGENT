from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_opaque_token, hash_token
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser
from app.storage.models import File, Folder, UploadSession
from app.storage.providers import UploadRequest, get_storage_provider, object_key_for
from app.storage.schemas import UploadInitiate
from app.storage.validation import validate_upload


def file_out_dict(file: File) -> dict:
    return {
        "id": file.id,
        "workspace_id": file.workspace_id,
        "project_id": file.project_id,
        "folder_id": file.folder_id,
        "original_name": file.original_name,
        "stored_name": file.stored_name,
        "content_type": file.content_type,
        "extension": file.extension,
        "size_bytes": file.size_bytes,
        "provider": file.provider,
        "purpose": file.purpose,
        "status": file.status,
        "version": file.version,
        "tags": file.tags,
        "checksum": file.checksum,
        "created_at": file.created_at,
        "deleted_at": file.deleted_at,
    }


async def create_upload_session(db: AsyncSession, payload: UploadInitiate, current: CurrentUser) -> tuple[UploadSession, File, str]:
    validate_upload(payload.content_type, payload.size_bytes)
    provider = get_storage_provider(payload.provider)
    object_key = object_key_for(str(payload.workspace_id), payload.original_name)
    upload = await provider.create_upload_url(UploadRequest(object_key=object_key, content_type=payload.content_type, size_bytes=payload.size_bytes))
    extension = Path(payload.original_name).suffix.lower().lstrip(".") or None
    stored_name = object_key.rsplit("/", 1)[-1]
    file = File(
        organization_id=current.organization_id,
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        folder_id=payload.folder_id,
        provider=upload.provider,
        bucket=upload.bucket,
        object_key=upload.object_key,
        original_name=payload.original_name,
        stored_name=stored_name,
        filename=payload.original_name,
        content_type=payload.content_type,
        extension=extension,
        size_bytes=payload.size_bytes,
        purpose=payload.purpose,
        status="uploading",
        version=1,
        tags=payload.tags,
        created_by_user_id=current.user.id,
        updated_by_user_id=current.user.id,
    )
    db.add(file)
    await db.flush()
    token = create_opaque_token()
    session = UploadSession(
        organization_id=current.organization_id,
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        folder_id=payload.folder_id,
        file_id=file.id,
        provider=upload.provider,
        original_name=payload.original_name,
        content_type=payload.content_type,
        size_bytes=payload.size_bytes,
        status="initiated",
        upload_url_ref=upload.url,
        resumable_token_hash=hash_token(token),
        expires_at=datetime.now(UTC) + timedelta(minutes=30),
        created_by_user_id=current.user.id,
        updated_by_user_id=current.user.id,
    )
    db.add(session)
    await audit(db, "storage.upload.initiated", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return session, file, upload.url or ""


async def get_owned_file(db: AsyncSession, file_id: UUID, current: CurrentUser) -> File | None:
    result = await db.execute(select(File).where(File.id == file_id, File.organization_id == current.organization_id))
    return result.scalar_one_or_none()


async def get_owned_folder(db: AsyncSession, folder_id: UUID, current: CurrentUser) -> Folder | None:
    result = await db.execute(select(Folder).where(Folder.id == folder_id, Folder.organization_id == current.organization_id))
    return result.scalar_one_or_none()