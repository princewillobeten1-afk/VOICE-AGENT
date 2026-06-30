from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.storage.models import File, Folder, UploadSession
from app.storage.providers import get_storage_provider
from app.storage.schemas import BulkAction, BulkActionResult, FileCopy, FileDownload, FileMetadataUpdate, FileMove, FileOut, FileRename, FolderCreate, FolderOut, UploadComplete, UploadInitiate, UploadInitiated
from app.storage.service import create_upload_session, file_out_dict, get_owned_file, get_owned_folder

router = APIRouter(prefix="/storage", tags=["storage"])


def folder_out(folder: Folder) -> FolderOut:
    return FolderOut(id=folder.id, workspace_id=folder.workspace_id, project_id=folder.project_id, parent_folder_id=folder.parent_folder_id, name=folder.name, path=folder.path, created_at=folder.created_at)


def file_out(file: File) -> FileOut:
    return FileOut(**file_out_dict(file))


@router.get("/files", response_model=list[FileOut])
async def list_files(workspace_id: UUID, q: str | None = None, folder_id: UUID | None = None, status_filter: str | None = Query(default=None, alias="status"), sort: str = "created_at", direction: str = "desc", current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(File).where(File.organization_id == current.organization_id, File.workspace_id == workspace_id)
    if folder_id:
        query = query.where(File.folder_id == folder_id)
    if status_filter:
        query = query.where(File.status == status_filter)
    else:
        query = query.where(File.deleted_at.is_(None))
    if q:
        query = query.where(or_(File.original_name.ilike(f"%{q}%"), File.filename.ilike(f"%{q}%")))
    if sort == "name":
        order_col = File.original_name
    elif sort == "size":
        order_col = File.size_bytes
    else:
        order_col = File.created_at
    query = query.order_by(order_col.asc() if direction == "asc" else order_col.desc()).limit(100)
    return [file_out(item) for item in (await db.execute(query)).scalars().all()]


@router.post("/uploads", response_model=UploadInitiated, status_code=201)
async def initiate_upload(payload: UploadInitiate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    try:
        session, file, upload_url = await create_upload_session(db, payload, current)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return UploadInitiated(upload_session_id=session.id, file=file_out(file), upload_url=upload_url, expires_in=900)


@router.post("/uploads/{upload_session_id}/complete", response_model=FileOut)
async def complete_upload(upload_session_id: UUID, payload: UploadComplete, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    session = await db.get(UploadSession, upload_session_id)
    if session is None or session.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Upload session not found")
    file = await db.get(File, session.file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file.status = "ready"
    file.checksum = payload.checksum or file.checksum
    file.size_bytes = payload.size_bytes or file.size_bytes
    session.status = "completed"
    await audit(db, "storage.upload.completed", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(file)


@router.get("/files/{file_id}/download", response_model=FileDownload)
async def download_file(file_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None or file.deleted_at is not None:
        raise HTTPException(status_code=404, detail="File not found")
    url = await get_storage_provider(file.provider).create_download_url(file.object_key)
    await audit(db, "storage.file.download_url.created", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return FileDownload(file_id=file.id, url=url, expires_in=900)


@router.patch("/files/{file_id}/rename", response_model=FileOut)
async def rename_file(file_id: UUID, payload: FileRename, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file.original_name = payload.name
    file.filename = payload.name
    file.updated_by_user_id = current.user.id
    await audit(db, "storage.file.renamed", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(file)


@router.patch("/files/{file_id}/move", response_model=FileOut)
async def move_file(file_id: UUID, payload: FileMove, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file.folder_id = payload.folder_id
    file.project_id = payload.project_id or file.project_id
    file.updated_by_user_id = current.user.id
    await audit(db, "storage.file.moved", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(file)


@router.post("/files/{file_id}/copy", response_model=FileOut, status_code=201)
async def copy_file(file_id: UUID, payload: FileCopy, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    copied = File(organization_id=file.organization_id, workspace_id=file.workspace_id, project_id=file.project_id, folder_id=payload.folder_id, provider=file.provider, bucket=file.bucket, object_key=f"{file.object_key}.copy", original_name=payload.name or f"Copy of {file.original_name}", stored_name=file.stored_name, filename=payload.name or f"Copy of {file.filename}", content_type=file.content_type, extension=file.extension, size_bytes=file.size_bytes, checksum=file.checksum, purpose=file.purpose, status=file.status, version=1, tags=file.tags, metadata_json=file.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(copied)
    await audit(db, "storage.file.copied", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(copied)


@router.patch("/files/{file_id}/metadata", response_model=FileOut)
async def update_metadata(file_id: UUID, payload: FileMetadataUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    if payload.tags is not None:
        file.tags = payload.tags
    if payload.metadata_json is not None:
        file.metadata_json = payload.metadata_json
    await audit(db, "storage.file.metadata.updated", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(file)


@router.delete("/files/{file_id}", response_model=FileOut)
async def delete_file(file_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file.deleted_at = datetime.now(UTC)
    file.status = "deleted"
    await audit(db, "storage.file.deleted", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(file)


@router.post("/files/{file_id}/restore", response_model=FileOut)
async def restore_file(file_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file.deleted_at = None
    file.status = "ready"
    await audit(db, "storage.file.restored", current.user.id, current.organization_id, "file", file.id)
    await db.commit()
    return file_out(file)


@router.delete("/files/{file_id}/permanent", status_code=204)
async def permanently_delete_file(file_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_DELETE)), db: AsyncSession = Depends(get_db)):
    file = await get_owned_file(db, file_id, current)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    await get_storage_provider(file.provider).delete_object(file.object_key)
    await db.delete(file)
    await audit(db, "storage.file.permanently_deleted", current.user.id, current.organization_id, "file", file.id)
    await db.commit()


@router.post("/folders", response_model=FolderOut, status_code=201)
async def create_folder(payload: FolderCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    parent_path = ""
    if payload.parent_folder_id:
        parent = await get_owned_folder(db, payload.parent_folder_id, current)
        if parent is None:
            raise HTTPException(status_code=404, detail="Parent folder not found")
        parent_path = parent.path
    path = f"{parent_path}/{payload.name}".strip("/")
    folder = Folder(organization_id=current.organization_id, workspace_id=payload.workspace_id, project_id=payload.project_id, parent_folder_id=payload.parent_folder_id, name=payload.name, path=path, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(folder)
    await audit(db, "storage.folder.created", current.user.id, current.organization_id, "folder", folder.id)
    await db.commit()
    return folder_out(folder)


@router.get("/folders", response_model=list[FolderOut])
async def list_folders(workspace_id: UUID, parent_folder_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Folder).where(Folder.organization_id == current.organization_id, Folder.workspace_id == workspace_id, Folder.deleted_at.is_(None))
    if parent_folder_id:
        query = query.where(Folder.parent_folder_id == parent_folder_id)
    return [folder_out(item) for item in (await db.execute(query.order_by(Folder.name.asc()))).scalars().all()]


@router.post("/bulk", response_model=BulkActionResult)
async def bulk_action(payload: BulkAction, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    affected = 0
    for file_id in payload.file_ids:
        file = await get_owned_file(db, file_id, current)
        if file is None:
            continue
        if payload.action == "delete":
            file.deleted_at = datetime.now(UTC)
            file.status = "deleted"
        elif payload.action == "restore":
            file.deleted_at = None
            file.status = "ready"
        elif payload.action == "move":
            file.folder_id = payload.folder_id
        affected += 1
    await audit(db, f"storage.bulk.{payload.action}", current.user.id, current.organization_id, metadata={"affected": affected})
    await db.commit()
    return BulkActionResult(affected=affected, action=payload.action)