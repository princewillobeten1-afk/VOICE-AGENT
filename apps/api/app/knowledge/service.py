from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.knowledge.models import DataSource, Document, DocumentVersion, KnowledgeActivity, KnowledgeBase, KnowledgeCategory, KnowledgePermission, KnowledgeSyncJob, WebsiteSource
from app.notifications.service import publish_domain_event


def slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "knowledge"


def kb_dict(item: KnowledgeBase) -> dict:
    return {"id": item.id, "organization_id": item.organization_id, "workspace_id": item.workspace_id, "project_id": item.project_id, "owner_user_id": item.owner_user_id, "name": item.name, "slug": item.slug, "description": item.description, "visibility": item.visibility, "status": item.status, "stats": item.stats, "permissions": item.permissions, "settings": item.settings, "published_at": item.published_at, "created_at": item.created_at, "updated_at": item.updated_at}


def source_dict(item: DataSource) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "workspace_id": item.workspace_id, "type": item.type, "provider": item.provider, "name": item.name, "uri": item.uri, "sync_status": item.sync_status, "health_status": item.health_status, "last_synced_at": item.last_synced_at, "next_sync_at": item.next_sync_at, "config": item.config, "sync_config": item.sync_config, "credentials_ref": item.credentials_ref, "created_at": item.created_at, "updated_at": item.updated_at}


def website_dict(item: WebsiteSource) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "data_source_id": item.data_source_id, "workspace_id": item.workspace_id, "base_url": item.base_url, "crawl_status": item.crawl_status, "allowed_paths": item.allowed_paths, "blocked_paths": item.blocked_paths, "refresh_schedule": item.refresh_schedule, "crawl_config": item.crawl_config, "last_crawled_at": item.last_crawled_at}


def document_dict(item: Document) -> dict:
    return {"id": item.id, "organization_id": item.organization_id, "workspace_id": item.workspace_id, "knowledge_base_id": item.knowledge_base_id, "data_source_id": item.data_source_id, "folder_id": item.folder_id, "category_id": item.category_id, "title": item.title, "slug": item.slug, "content_type": item.content_type, "source_kind": item.source_kind, "status": item.status, "validation_status": item.validation_status, "freshness_status": item.freshness_status, "storage_file_id": item.storage_file_id, "checksum": item.checksum, "size_bytes": item.size_bytes, "version_number": item.version_number, "published_version_id": item.published_version_id, "duplicate_of_document_id": item.duplicate_of_document_id, "owner_user_id": item.owner_user_id, "custom_metadata": item.custom_metadata, "metadata_json": item.metadata_json, "published_at": item.published_at, "archived_at": item.archived_at, "created_at": item.created_at, "updated_at": item.updated_at}


def version_dict(item: DocumentVersion) -> dict:
    return {"id": item.id, "document_id": item.document_id, "version_number": item.version_number, "status": item.status, "title": item.title, "content_ref": item.content_ref, "checksum": item.checksum, "size_bytes": item.size_bytes, "change_summary": item.change_summary, "metadata_json": item.metadata_json, "published_at": item.published_at, "created_at": item.created_at}


def permission_dict(item: KnowledgePermission) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "knowledge_base_id": item.knowledge_base_id, "document_id": item.document_id, "principal_type": item.principal_type, "principal_id": item.principal_id, "role": item.role, "permissions": item.permissions, "expires_at": item.expires_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


def sync_dict(item: KnowledgeSyncJob) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "data_source_id": item.data_source_id, "sync_type": item.sync_type, "status": item.status, "strategy": item.strategy, "conflict_count": item.conflict_count, "documents_scanned": item.documents_scanned, "documents_created": item.documents_created, "documents_updated": item.documents_updated, "error_message": item.error_message, "started_at": item.started_at, "finished_at": item.finished_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


def category_dict(item: KnowledgeCategory) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "knowledge_base_id": item.knowledge_base_id, "parent_id": item.parent_id, "name": item.name, "slug": item.slug, "description": item.description, "color": item.color, "sort_order": item.sort_order, "metadata_json": item.metadata_json}


def activity_dict(item: KnowledgeActivity) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "document_id": item.document_id, "data_source_id": item.data_source_id, "actor_user_id": item.actor_user_id, "action": item.action, "summary": item.summary, "payload": item.payload, "created_at": item.created_at}


async def activity(db: AsyncSession, current: CurrentUser, action: str, summary: str, workspace_id: UUID, knowledge_base_id=None, document_id=None, data_source_id=None, payload: dict | None = None) -> None:
    db.add(KnowledgeActivity(organization_id=current.organization_id, workspace_id=workspace_id, knowledge_base_id=knowledge_base_id, document_id=document_id, data_source_id=data_source_id, actor_user_id=current.user.id, action=action, summary=summary, payload=payload or {}))


async def emit_knowledge_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, aggregate_type: str, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"knowledge.{name}", aggregate_type=aggregate_type, aggregate_id=aggregate_id, source="knowledge-platform", payload=payload, metadata={"platform": "knowledge"}))


async def get_owned_kb(db: AsyncSession, kb_id: UUID, current: CurrentUser) -> KnowledgeBase | None:
    return (await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id, KnowledgeBase.organization_id == current.organization_id, KnowledgeBase.deleted_at.is_(None)))).scalar_one_or_none()


async def get_owned_document(db: AsyncSession, document_id: UUID, current: CurrentUser) -> Document | None:
    return (await db.execute(select(Document).where(Document.id == document_id, Document.organization_id == current.organization_id, Document.deleted_at.is_(None)))).scalar_one_or_none()


async def create_document_version(db: AsyncSession, current: CurrentUser, document: Document, change_summary: str | None, status: str = "draft") -> DocumentVersion:
    max_version = (await db.execute(select(func.max(DocumentVersion.version_number)).where(DocumentVersion.document_id == document.id))).scalar_one_or_none() or 0
    version = DocumentVersion(organization_id=current.organization_id, workspace_id=document.workspace_id, document_id=document.id, version_number=int(max_version) + 1, status=status, title=document.title, content_ref=str(document.storage_file_id) if document.storage_file_id else None, checksum=document.checksum, size_bytes=document.size_bytes, change_summary=change_summary, metadata_json=document.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    document.version_number = version.version_number
    return version


async def detect_duplicate(db: AsyncSession, document: Document) -> None:
    if not document.checksum:
        return
    duplicate = (await db.execute(select(Document).where(Document.knowledge_base_id == document.knowledge_base_id, Document.checksum == document.checksum, Document.id != document.id, Document.deleted_at.is_(None)).limit(1))).scalar_one_or_none()
    if duplicate:
        document.duplicate_of_document_id = duplicate.id
        document.validation_status = "duplicate"


async def dashboard_stats(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    kb_count = (await db.execute(select(func.count()).select_from(KnowledgeBase).where(KnowledgeBase.organization_id == current.organization_id, KnowledgeBase.workspace_id == workspace_id, KnowledgeBase.deleted_at.is_(None)))).scalar_one()
    doc_count = (await db.execute(select(func.count()).select_from(Document).where(Document.organization_id == current.organization_id, Document.workspace_id == workspace_id, Document.deleted_at.is_(None)))).scalar_one()
    source_count = (await db.execute(select(func.count()).select_from(DataSource).where(DataSource.organization_id == current.organization_id, DataSource.workspace_id == workspace_id, DataSource.deleted_at.is_(None)))).scalar_one()
    storage = (await db.execute(select(func.coalesce(func.sum(Document.size_bytes), 0)).where(Document.organization_id == current.organization_id, Document.workspace_id == workspace_id, Document.deleted_at.is_(None)))).scalar_one()
    return {"knowledge_bases": int(kb_count or 0), "documents": int(doc_count or 0), "sources": int(source_count or 0), "storage_bytes": int(storage or 0), "freshness": "placeholder", "rag_ready": False}