from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.knowledge.models import DataSource, Document, DocumentVersion, KnowledgeActivity, KnowledgeBase, KnowledgeCategory, KnowledgePermission, KnowledgeSyncJob, WebsiteSource
from app.knowledge.schemas import ActivityOut, CategoryCreate, CategoryOut, DocumentCreate, DocumentOut, DocumentUpdate, DocumentVersionOut, KnowledgeBaseCreate, KnowledgeBaseOut, KnowledgeBaseUpdate, KnowledgeDashboard, KnowledgeSearchQuery, PermissionCreate, PermissionOut, SourceCreate, SourceOut, SyncJobOut, SyncRequest, WebsiteSourceCreate, WebsiteSourceOut
from app.knowledge.service import activity, activity_dict, category_dict, create_document_version, dashboard_stats, detect_duplicate, document_dict, emit_knowledge_event, get_owned_document, get_owned_kb, kb_dict, permission_dict, slugify, source_dict, sync_dict, version_dict, website_dict

router = APIRouter(prefix="/knowledge", tags=["knowledge-platform"])


@router.get("/dashboard", response_model=KnowledgeDashboard)
async def dashboard(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    kbs = (await db.execute(select(KnowledgeBase).where(KnowledgeBase.organization_id == current.organization_id, KnowledgeBase.workspace_id == workspace_id, KnowledgeBase.deleted_at.is_(None)).order_by(KnowledgeBase.updated_at.desc()).limit(8))).scalars().all()
    docs = (await db.execute(select(Document).where(Document.organization_id == current.organization_id, Document.workspace_id == workspace_id, Document.deleted_at.is_(None)).order_by(Document.updated_at.desc()).limit(12))).scalars().all()
    sources = (await db.execute(select(DataSource).where(DataSource.organization_id == current.organization_id, DataSource.workspace_id == workspace_id, DataSource.deleted_at.is_(None)).order_by(DataSource.updated_at.desc()).limit(8))).scalars().all()
    logs = (await db.execute(select(KnowledgeActivity).where(KnowledgeActivity.organization_id == current.organization_id, KnowledgeActivity.workspace_id == workspace_id).order_by(KnowledgeActivity.created_at.desc()).limit(10))).scalars().all()
    return KnowledgeDashboard(knowledge_bases=[KnowledgeBaseOut(**kb_dict(item)) for item in kbs], documents=[DocumentOut(**document_dict(item)) for item in docs], sources=[SourceOut(**source_dict(item)) for item in sources], recent_activity=[ActivityOut(**activity_dict(item)) for item in logs], stats=await dashboard_stats(db, current, workspace_id))


@router.get("/bases", response_model=list[KnowledgeBaseOut])
async def list_bases(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(KnowledgeBase).where(KnowledgeBase.organization_id == current.organization_id, KnowledgeBase.workspace_id == workspace_id, KnowledgeBase.deleted_at.is_(None)).order_by(KnowledgeBase.name.asc()))).scalars().all()
    return [KnowledgeBaseOut(**kb_dict(item)) for item in rows]


@router.post("/bases", response_model=KnowledgeBaseOut, status_code=status.HTTP_201_CREATED)
async def create_base(payload: KnowledgeBaseCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = KnowledgeBase(organization_id=current.organization_id, workspace_id=payload.workspace_id, project_id=payload.project_id, owner_user_id=current.user.id, name=payload.name, slug=payload.slug or slugify(payload.name), description=payload.description, visibility=payload.visibility, status=payload.status, stats={"documents": 0, "sources": 0, "health": "new"}, permissions=payload.permissions, settings=payload.settings, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(kb)
    await db.flush()
    await activity(db, current, "knowledge_base.created", f"Created knowledge base {kb.name}", kb.workspace_id, knowledge_base_id=kb.id)
    await emit_knowledge_event(db, current, "base.created", kb.workspace_id, "knowledge_base", kb.id, {"name": kb.name})
    await audit(db, "knowledge_base.created", current.user.id, current.organization_id, "knowledge_base", kb.id)
    await db.commit()
    return KnowledgeBaseOut(**kb_dict(kb))


@router.patch("/bases/{knowledge_base_id}", response_model=KnowledgeBaseOut)
async def update_base(knowledge_base_id: UUID, payload: KnowledgeBaseUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, knowledge_base_id, current)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(kb, field, value)
    kb.updated_by_user_id = current.user.id
    await activity(db, current, "knowledge_base.updated", f"Updated knowledge base {kb.name}", kb.workspace_id, knowledge_base_id=kb.id)
    await db.commit()
    return KnowledgeBaseOut(**kb_dict(kb))


@router.post("/bases/{knowledge_base_id}/publish", response_model=KnowledgeBaseOut)
async def publish_base(knowledge_base_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, knowledge_base_id, current)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    kb.status = "published"
    kb.published_at = datetime.now(UTC)
    await activity(db, current, "knowledge_base.published", f"Published {kb.name}", kb.workspace_id, knowledge_base_id=kb.id)
    await db.commit()
    return KnowledgeBaseOut(**kb_dict(kb))

@router.post("/sources", response_model=SourceOut, status_code=status.HTTP_201_CREATED)
async def create_source(payload: SourceCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, payload.knowledge_base_id, current)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    source = DataSource(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, type=payload.type, provider=payload.provider, name=payload.name, uri=payload.uri, sync_status="pending", health_status="unknown", config=payload.config, sync_config=payload.sync_config, credentials_ref=payload.credentials_ref, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(source)
    await db.flush()
    await activity(db, current, "source.created", f"Added source {source.name}", source.workspace_id, knowledge_base_id=source.knowledge_base_id, data_source_id=source.id)
    await db.commit()
    return SourceOut(**source_dict(source))


@router.post("/websites", response_model=WebsiteSourceOut, status_code=status.HTTP_201_CREATED)
async def create_website(payload: WebsiteSourceCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, payload.knowledge_base_id, current)
    source = await db.get(DataSource, payload.data_source_id)
    if kb is None or source is None or source.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Source not found")
    website = WebsiteSource(organization_id=current.organization_id, workspace_id=payload.workspace_id, data_source_id=payload.data_source_id, knowledge_base_id=payload.knowledge_base_id, base_url=payload.base_url, crawl_status="registered", allowed_paths=payload.allowed_paths, blocked_paths=payload.blocked_paths, refresh_schedule=payload.refresh_schedule, crawl_config=payload.crawl_config, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(website)
    await db.flush()
    await activity(db, current, "website.registered", f"Registered website {payload.base_url}", payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, data_source_id=payload.data_source_id)
    await db.commit()
    return WebsiteSourceOut(**website_dict(website))


@router.get("/documents", response_model=list[DocumentOut])
async def list_documents(workspace_id: UUID, knowledge_base_id: UUID | None = None, q: str | None = None, status_filter: str | None = Query(default=None, alias="status"), current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Document).where(Document.organization_id == current.organization_id, Document.workspace_id == workspace_id, Document.deleted_at.is_(None))
    if knowledge_base_id:
        query = query.where(Document.knowledge_base_id == knowledge_base_id)
    if status_filter:
        query = query.where(Document.status == status_filter)
    if q:
        query = query.where(or_(Document.title.ilike(f"%{q}%"), Document.content_type.ilike(f"%{q}%")))
    rows = (await db.execute(query.order_by(Document.updated_at.desc()).limit(100))).scalars().all()
    return [DocumentOut(**document_dict(item)) for item in rows]


@router.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def create_document(payload: DocumentCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, payload.knowledge_base_id, current)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    doc = Document(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, data_source_id=payload.data_source_id, folder_id=payload.folder_id, category_id=payload.category_id, title=payload.title, slug=slugify(payload.title), content_type=payload.content_type, source_kind=payload.source_kind, status="draft", validation_status="pending", freshness_status="new", storage_file_id=payload.storage_file_id, checksum=payload.checksum, size_bytes=payload.size_bytes, owner_user_id=current.user.id, custom_metadata=payload.custom_metadata, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(doc)
    await db.flush()
    await detect_duplicate(db, doc)
    await create_document_version(db, current, doc, "Initial content created")
    await activity(db, current, "document.created", f"Created document {doc.title}", doc.workspace_id, knowledge_base_id=doc.knowledge_base_id, document_id=doc.id)
    await emit_knowledge_event(db, current, "document.created", doc.workspace_id, "document", doc.id, {"title": doc.title})
    await audit(db, "knowledge_document.created", current.user.id, current.organization_id, "document", doc.id)
    await db.commit()
    return DocumentOut(**document_dict(doc))


@router.patch("/documents/{document_id}", response_model=DocumentOut)
async def update_document(document_id: UUID, payload: DocumentUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    doc = await get_owned_document(db, document_id, current)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    for field, value in payload.model_dump(exclude_unset=True, exclude={"change_summary"}).items():
        setattr(doc, field, value)
    doc.updated_by_user_id = current.user.id
    await create_document_version(db, current, doc, payload.change_summary or "Document updated")
    await activity(db, current, "document.updated", f"Updated document {doc.title}", doc.workspace_id, knowledge_base_id=doc.knowledge_base_id, document_id=doc.id)
    await db.commit()
    return DocumentOut(**document_dict(doc))


@router.post("/documents/{document_id}/publish", response_model=DocumentOut)
async def publish_document(document_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    doc = await get_owned_document(db, document_id, current)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    version = await create_document_version(db, current, doc, "Published document", "published")
    doc.status = "published"
    doc.published_at = datetime.now(UTC)
    await db.flush()
    doc.published_version_id = version.id
    await activity(db, current, "document.published", f"Published document {doc.title}", doc.workspace_id, knowledge_base_id=doc.knowledge_base_id, document_id=doc.id)
    await db.commit()
    return DocumentOut(**document_dict(doc))


@router.get("/documents/{document_id}/versions", response_model=list[DocumentVersionOut])
async def list_versions(document_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    doc = await get_owned_document(db, document_id, current)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    versions = (await db.execute(select(DocumentVersion).where(DocumentVersion.document_id == doc.id).order_by(DocumentVersion.version_number.desc()))).scalars().all()
    return [DocumentVersionOut(**version_dict(item)) for item in versions]


@router.post("/permissions", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
async def create_permission(payload: PermissionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    permission = KnowledgePermission(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, document_id=payload.document_id, principal_type=payload.principal_type, principal_id=payload.principal_id, role=payload.role, permissions=payload.permissions, expires_at=payload.expires_at, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(permission)
    await db.flush()
    await audit(db, "knowledge_permission.created", current.user.id, current.organization_id, "knowledge_permission", permission.id)
    await db.commit()
    return PermissionOut(**permission_dict(permission))


@router.post("/sync", response_model=SyncJobOut, status_code=status.HTTP_201_CREATED)
async def trigger_sync(payload: SyncRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, payload.knowledge_base_id, current)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    job = KnowledgeSyncJob(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, data_source_id=payload.data_source_id, sync_type=payload.sync_type, status="queued", strategy=payload.strategy, metadata_json={"note": "Architecture-ready sync job. Crawling and connector execution are not implemented in Task 016A."}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(job)
    await db.flush()
    await activity(db, current, "sync.queued", f"Queued {payload.strategy} sync", payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, data_source_id=payload.data_source_id)
    await db.commit()
    return SyncJobOut(**sync_dict(job))


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    kb = await get_owned_kb(db, payload.knowledge_base_id, current)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    category = KnowledgeCategory(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, parent_id=payload.parent_id, name=payload.name, slug=payload.slug or slugify(payload.name), description=payload.description, color=payload.color, sort_order=payload.sort_order, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(category)
    await db.flush()
    await db.commit()
    return CategoryOut(**category_dict(category))


@router.post("/search", response_model=list[DocumentOut])
async def search_documents(payload: KnowledgeSearchQuery, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Document).where(Document.organization_id == current.organization_id, Document.workspace_id == payload.workspace_id, Document.deleted_at.is_(None))
    if payload.knowledge_base_id:
        query = query.where(Document.knowledge_base_id == payload.knowledge_base_id)
    if payload.status:
        query = query.where(Document.status == payload.status)
    if payload.source_kind:
        query = query.where(Document.source_kind == payload.source_kind)
    if payload.q:
        query = query.where(or_(Document.title.ilike(f"%{payload.q}%"), Document.content_type.ilike(f"%{payload.q}%")))
    rows = (await db.execute(query.order_by(Document.updated_at.desc()).limit(payload.limit))).scalars().all()
    return [DocumentOut(**document_dict(item)) for item in rows]
