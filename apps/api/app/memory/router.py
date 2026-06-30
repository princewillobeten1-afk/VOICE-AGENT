from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.memory.models import Memory, MemoryCategory, MemoryLink, MemoryPolicy, MemoryVersion
from app.memory.schemas import MemoryActionRequest, MemoryAnalyticsOut, MemoryCategoryCreate, MemoryCategoryOut, MemoryCreate, MemoryDetail, MemoryLinkCreate, MemoryLinkOut, MemoryMergeRequest, MemoryOut, MemoryPolicyCreate, MemoryPolicyOut, MemorySearchQuery, MemorySearchResult, MemoryUpdate, MemoryVersionOut
from app.memory.service import analytics, category_dict, create_memory_record, create_version, emit_memory_event, ensure_default_categories, get_owned_memory, link_dict, memory_dict, policy_dict, search_memories, version_dict

router = APIRouter(prefix="/memory", tags=["memory-system"])


@router.get("/categories", response_model=list[MemoryCategoryOut])
async def list_categories(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    await ensure_default_categories(db, current, workspace_id)
    rows = (await db.execute(select(MemoryCategory).where(MemoryCategory.organization_id == current.organization_id, MemoryCategory.workspace_id == workspace_id, MemoryCategory.deleted_at.is_(None)).order_by(MemoryCategory.name.asc()))).scalars().all()
    await db.commit()
    return [MemoryCategoryOut(**category_dict(item)) for item in rows]


@router.post("/categories", response_model=MemoryCategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(payload: MemoryCategoryCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    category = MemoryCategory(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, slug=payload.slug, description=payload.description, color=payload.color, retention_days=payload.retention_days, default_privacy_level=payload.default_privacy_level, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(category)
    await db.flush()
    await audit(db, "memory.category.created", current.user.id, current.organization_id, "memory_category", category.id)
    await db.commit()
    return MemoryCategoryOut(**category_dict(category))


@router.get("/policies", response_model=list[MemoryPolicyOut])
async def list_policies(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(MemoryPolicy).where(MemoryPolicy.organization_id == current.organization_id, MemoryPolicy.workspace_id == workspace_id, MemoryPolicy.deleted_at.is_(None)).order_by(MemoryPolicy.updated_at.desc()))).scalars().all()
    return [MemoryPolicyOut(**policy_dict(item)) for item in rows]


@router.post("/policies", response_model=MemoryPolicyOut, status_code=status.HTTP_201_CREATED)
async def create_policy(payload: MemoryPolicyCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    policy = MemoryPolicy(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, status=payload.status, scope=payload.scope, memory_types=payload.memory_types, retention_days=payload.retention_days, expiration_rules=payload.expiration_rules, auto_cleanup_enabled=payload.auto_cleanup_enabled, max_memory_size=payload.max_memory_size, privacy_rules=payload.privacy_rules, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(policy)
    await db.flush()
    await audit(db, "memory.policy.created", current.user.id, current.organization_id, "memory_policy", policy.id)
    await db.commit()
    return MemoryPolicyOut(**policy_dict(policy))


@router.get("", response_model=list[MemoryOut])
async def list_memories(workspace_id: UUID, memory_type: str | None = None, status_filter: str | None = Query(default="active", alias="status"), current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(Memory).where(Memory.organization_id == current.organization_id, Memory.workspace_id == workspace_id, Memory.deleted_at.is_(None))
    if memory_type:
        query = query.where(Memory.memory_type == memory_type)
    if status_filter:
        query = query.where(Memory.status == status_filter)
    rows = (await db.execute(query.order_by(Memory.pinned.desc(), Memory.importance_score.desc(), Memory.updated_at.desc()).limit(100))).scalars().all()
    return [MemoryOut(**memory_dict(item)) for item in rows]


@router.post("", response_model=MemoryOut, status_code=status.HTTP_201_CREATED)
async def create_memory(payload: MemoryCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    memory = await create_memory_record(db, current, payload)
    await audit(db, "memory.created", current.user.id, current.organization_id, "memory", memory.id)
    await db.commit()
    return MemoryOut(**memory_dict(memory))


@router.post("/search", response_model=list[MemorySearchResult])
async def search(payload: MemorySearchQuery, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    results = await search_memories(db, current, payload)
    await db.commit()
    return [MemorySearchResult(memory=MemoryOut(**memory_dict(item["memory"])), score=item["score"], reasons=item["reasons"]) for item in results]


@router.get("/analytics", response_model=MemoryAnalyticsOut)
async def memory_analytics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return MemoryAnalyticsOut(**await analytics(db, current, workspace_id))


@router.get("/{memory_id}", response_model=MemoryDetail)
async def get_memory(memory_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    versions = (await db.execute(select(MemoryVersion).where(MemoryVersion.memory_id == memory.id).order_by(MemoryVersion.version_number.desc()))).scalars().all()
    links = (await db.execute(select(MemoryLink).where(MemoryLink.source_memory_id == memory.id).limit(20))).scalars().all()
    related = []
    if memory.tags:
        results = await search_memories(db, current, MemorySearchQuery(workspace_id=memory.workspace_id, q=" ".join(memory.tags[:3]), limit=5))
        related = [MemorySearchResult(memory=MemoryOut(**memory_dict(item["memory"])), score=item["score"], reasons=item["reasons"]) for item in results if item["memory"].id != memory.id]
    await db.commit()
    return MemoryDetail(memory=MemoryOut(**memory_dict(memory)), versions=[MemoryVersionOut(**version_dict(item)) for item in versions], links=[MemoryLinkOut(**link_dict(item)) for item in links], related=related)


@router.patch("/{memory_id}", response_model=MemoryOut)
async def update_memory(memory_id: UUID, payload: MemoryUpdate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    for field, value in payload.model_dump(exclude_unset=True, exclude={"change_summary"}).items():
        setattr(memory, field, value)
    memory.updated_by_user_id = current.user.id
    await create_version(db, current, memory, "updated", payload.change_summary)
    await emit_memory_event(db, current, "updated", memory, {"change_summary": payload.change_summary})
    await audit(db, "memory.updated", current.user.id, current.organization_id, "memory", memory.id)
    await db.commit()
    return MemoryOut(**memory_dict(memory))


@router.post("/{memory_id}/pin", response_model=MemoryOut)
async def pin_memory(memory_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory.pinned = True
    await emit_memory_event(db, current, "pinned", memory, {})
    await db.commit()
    return MemoryOut(**memory_dict(memory))


@router.post("/{memory_id}/archive", response_model=MemoryOut)
async def archive_memory(memory_id: UUID, payload: MemoryActionRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory.status = "archived"
    memory.archived_at = datetime.now(UTC)
    await create_version(db, current, memory, "archived", payload.reason)
    await emit_memory_event(db, current, "archived", memory, {"reason": payload.reason})
    await db.commit()
    return MemoryOut(**memory_dict(memory))


@router.post("/{memory_id}/restore", response_model=MemoryOut)
async def restore_memory(memory_id: UUID, payload: MemoryActionRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory.status = "active"
    memory.archived_at = None
    memory.forgotten_at = None
    await create_version(db, current, memory, "restored", payload.reason)
    await emit_memory_event(db, current, "restored", memory, {"reason": payload.reason})
    await db.commit()
    return MemoryOut(**memory_dict(memory))


@router.post("/{memory_id}/forget", response_model=MemoryOut)
async def forget_memory(memory_id: UUID, payload: MemoryActionRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory.status = "forgotten"
    memory.content = "[forgotten]"
    memory.summary = payload.reason or "Memory content forgotten by request."
    memory.forgotten_at = datetime.now(UTC)
    await create_version(db, current, memory, "forgotten", payload.reason)
    await emit_memory_event(db, current, "forgotten", memory, {"reason": payload.reason})
    await audit(db, "memory.forgotten", current.user.id, current.organization_id, "memory", memory.id)
    await db.commit()
    return MemoryOut(**memory_dict(memory))


@router.delete("/{memory_id}", status_code=204)
async def delete_memory(memory_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_DELETE)), db: AsyncSession = Depends(get_db)):
    memory = await get_owned_memory(db, memory_id, current)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory.deleted_at = datetime.now(UTC)
    await emit_memory_event(db, current, "deleted", memory, {})
    await audit(db, "memory.deleted", current.user.id, current.organization_id, "memory", memory.id)
    await db.commit()


@router.post("/{memory_id}/merge", response_model=MemoryOut)
async def merge_memory(memory_id: UUID, payload: MemoryMergeRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    source = await get_owned_memory(db, memory_id, current)
    target = await get_owned_memory(db, payload.target_memory_id, current)
    if source is None or target is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    if payload.strategy == "append_summary":
        target.summary = f"{target.summary or ''}\nMerged note: {source.summary or source.title}".strip()
    target.tags = sorted(set((target.tags or []) + (source.tags or [])))
    source.status = "merged"
    source.archived_at = datetime.now(UTC)
    db.add(MemoryLink(organization_id=current.organization_id, workspace_id=target.workspace_id, source_memory_id=target.id, target_memory_id=source.id, link_type="merged_from", strength=1.0, metadata_json={"reason": payload.reason}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id))
    await create_version(db, current, target, "merged", payload.reason)
    await emit_memory_event(db, current, "merged", target, {"source_memory_id": str(source.id), "strategy": payload.strategy})
    await db.commit()
    return MemoryOut(**memory_dict(target))


@router.post("/{memory_id}/links", response_model=MemoryLinkOut, status_code=status.HTTP_201_CREATED)
async def link_memory(memory_id: UUID, payload: MemoryLinkCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    source = await get_owned_memory(db, memory_id, current)
    target = await get_owned_memory(db, payload.target_memory_id, current)
    if source is None or target is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    link = MemoryLink(organization_id=current.organization_id, workspace_id=source.workspace_id, source_memory_id=source.id, target_memory_id=target.id, link_type=payload.link_type, strength=payload.strength, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(link)
    await emit_memory_event(db, current, "linked", source, {"target_memory_id": str(target.id), "link_type": payload.link_type})
    await db.commit()
    return MemoryLinkOut(**link_dict(link))