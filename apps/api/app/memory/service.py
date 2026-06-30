from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.memory.models import Memory, MemoryCategory, MemoryEvent, MemoryLink, MemoryPolicy, MemoryStatistic, MemoryVersion
from app.notifications.service import publish_domain_event

IMPORTANT_KEYWORDS = {"preference", "prefers", "important", "vip", "billing", "renewal", "appointment", "blocked", "cancel", "support", "decision", "approval"}
DEFAULT_CATEGORIES = ["personal", "business", "preferences", "tasks", "contacts", "conversations", "meetings", "support", "sales", "billing", "technical", "organizational"]


def memory_dict(memory: Memory) -> dict:
    return {"id": memory.id, "organization_id": memory.organization_id, "workspace_id": memory.workspace_id, "agent_id": memory.agent_id, "conversation_id": memory.conversation_id, "user_id": memory.user_id, "category_id": memory.category_id, "policy_id": memory.policy_id, "memory_type": memory.memory_type, "title": memory.title, "content": memory.content, "summary": memory.summary, "status": memory.status, "privacy_level": memory.privacy_level, "visibility": memory.visibility, "source_type": memory.source_type, "source_ref": memory.source_ref, "importance_score": float(memory.importance_score or 0), "confidence_score": float(memory.confidence_score or 0), "recency_score": float(memory.recency_score or 0), "retrieval_count": memory.retrieval_count, "pinned": memory.pinned, "encrypted": memory.encrypted, "tags": memory.tags, "facts": memory.facts, "evaluation": memory.evaluation, "index_state": memory.index_state, "expires_at": memory.expires_at, "archived_at": memory.archived_at, "forgotten_at": memory.forgotten_at, "created_at": memory.created_at, "updated_at": memory.updated_at}


def category_dict(category: MemoryCategory) -> dict:
    return {"id": category.id, "workspace_id": category.workspace_id, "name": category.name, "slug": category.slug, "description": category.description, "color": category.color, "retention_days": category.retention_days, "default_privacy_level": category.default_privacy_level, "metadata_json": category.metadata_json, "created_at": category.created_at, "updated_at": category.updated_at}


def policy_dict(policy: MemoryPolicy) -> dict:
    return {"id": policy.id, "workspace_id": policy.workspace_id, "name": policy.name, "status": policy.status, "scope": policy.scope, "memory_types": policy.memory_types, "retention_days": policy.retention_days, "expiration_rules": policy.expiration_rules, "auto_cleanup_enabled": policy.auto_cleanup_enabled, "max_memory_size": policy.max_memory_size, "privacy_rules": policy.privacy_rules, "metadata_json": policy.metadata_json, "created_at": policy.created_at, "updated_at": policy.updated_at}


def version_dict(version: MemoryVersion) -> dict:
    return {"id": version.id, "memory_id": version.memory_id, "version_number": version.version_number, "title": version.title, "content": version.content, "summary": version.summary, "change_type": version.change_type, "change_summary": version.change_summary, "evaluation": version.evaluation, "created_at": version.created_at}


def link_dict(link: MemoryLink) -> dict:
    return {"id": link.id, "source_memory_id": link.source_memory_id, "target_memory_id": link.target_memory_id, "link_type": link.link_type, "strength": float(link.strength or 0), "metadata_json": link.metadata_json}


async def emit_memory_event(db: AsyncSession, current: CurrentUser, event_type: str, memory: Memory | None, payload: dict, latency_ms: int | None = None) -> None:
    db.add(MemoryEvent(organization_id=current.organization_id, workspace_id=(memory.workspace_id if memory else payload.get("workspace_id")), memory_id=(memory.id if memory else None), event_type=event_type, actor_user_id=current.user.id, payload=payload, latency_ms=latency_ms))
    if memory is not None:
        await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=memory.workspace_id, actor_user_id=current.user.id, name=f"memory.{event_type}", aggregate_type="memory", aggregate_id=memory.id, source="memory-system", payload=payload, metadata={"memory_type": memory.memory_type, "privacy_level": memory.privacy_level}))


def evaluate_memory(payload) -> dict:
    text = f"{payload.title} {payload.content} {' '.join(payload.tags or [])}".lower()
    matches = sorted(keyword for keyword in IMPORTANT_KEYWORDS if keyword in text)
    importance = payload.importance_score if payload.importance_score is not None else min(1.0, 0.35 + (len(matches) * 0.1) + (0.15 if payload.memory_type in {"long_term", "semantic", "organizational"} else 0))
    confidence = payload.confidence_score if payload.confidence_score is not None else 0.8 if payload.source_type in {"manual", "conversation"} else 0.65
    category_hint = payload.memory_type
    retention = "policy_controlled" if payload.expires_at is None else "explicit_expiration"
    return {"importance_score": round(float(importance), 2), "confidence_score": round(float(confidence), 2), "category_hint": category_hint, "matched_keywords": matches, "retention": retention, "privacy_level": payload.privacy_level, "store": importance >= 0.25 or bool(payload.tags)}


async def create_version(db: AsyncSession, current: CurrentUser, memory: Memory, change_type: str, change_summary: str | None) -> MemoryVersion:
    max_version = (await db.execute(select(func.max(MemoryVersion.version_number)).where(MemoryVersion.memory_id == memory.id))).scalar_one_or_none() or 0
    version = MemoryVersion(organization_id=current.organization_id, workspace_id=memory.workspace_id, memory_id=memory.id, version_number=int(max_version) + 1, title=memory.title, content=memory.content, summary=memory.summary, change_type=change_type, change_summary=change_summary, evaluation=memory.evaluation, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(version)
    return version


async def get_owned_memory(db: AsyncSession, memory_id: UUID, current: CurrentUser) -> Memory | None:
    return (await db.execute(select(Memory).where(Memory.id == memory_id, Memory.organization_id == current.organization_id, Memory.deleted_at.is_(None)))).scalar_one_or_none()


async def create_memory_record(db: AsyncSession, current: CurrentUser, payload) -> Memory:
    evaluation = evaluate_memory(payload)
    memory = Memory(organization_id=current.organization_id, workspace_id=payload.workspace_id, agent_id=payload.agent_id, conversation_id=payload.conversation_id, user_id=payload.user_id, category_id=payload.category_id, policy_id=payload.policy_id, memory_type=payload.memory_type, title=payload.title, content=payload.content, summary=payload.summary, status="active" if evaluation["store"] else "pending_review", privacy_level=payload.privacy_level, visibility=payload.visibility, source_type=payload.source_type, source_ref=payload.source_ref, importance_score=evaluation["importance_score"], confidence_score=evaluation["confidence_score"], recency_score=1.0, tags=payload.tags, facts=payload.facts, evaluation=evaluation, index_state={"status": "metadata_indexed", "embedding": "not_configured"}, expires_at=payload.expires_at, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(memory)
    await db.flush()
    await create_version(db, current, memory, "created", "Initial memory created")
    await emit_memory_event(db, current, "created", memory, {"memory_type": memory.memory_type, "importance_score": evaluation["importance_score"]})
    return memory


def score_memory(memory: Memory, query: str | None) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if memory.pinned:
        score += 0.25
        reasons.append("pinned")
    importance = float(memory.importance_score or 0)
    confidence = float(memory.confidence_score or 0)
    recency = float(memory.recency_score or 0)
    score += importance * 0.35 + confidence * 0.25 + recency * 0.15
    if importance >= 0.7:
        reasons.append("high importance")
    if query:
        haystack = f"{memory.title} {memory.content} {memory.summary or ''} {' '.join(memory.tags or [])}".lower()
        terms = [term for term in query.lower().split() if len(term) > 2]
        matches = sum(1 for term in terms if term in haystack)
        if terms:
            score += min(0.4, matches / len(terms) * 0.4)
        if matches:
            reasons.append("text match")
    return round(score, 4), reasons or ["policy eligible"]


async def search_memories(db: AsyncSession, current: CurrentUser, payload) -> list[dict]:
    query = select(Memory).where(Memory.organization_id == current.organization_id, Memory.workspace_id == payload.workspace_id, Memory.deleted_at.is_(None), Memory.forgotten_at.is_(None))
    if not payload.include_archived:
        query = query.where(Memory.status == "active")
    if payload.memory_types:
        query = query.where(Memory.memory_type.in_(payload.memory_types))
    if payload.categories:
        query = query.where(Memory.category_id.in_(payload.categories))
    if payload.agent_id:
        query = query.where(or_(Memory.agent_id == payload.agent_id, Memory.visibility.in_(["workspace", "organization", "shared"])))
    if payload.user_id:
        query = query.where(or_(Memory.user_id == payload.user_id, Memory.visibility.in_(["workspace", "organization", "shared"])))
    if payload.privacy_levels:
        query = query.where(Memory.privacy_level.in_(payload.privacy_levels))
    if payload.q:
        pattern = f"%{payload.q}%"
        query = query.where(or_(Memory.title.ilike(pattern), Memory.content.ilike(pattern), Memory.summary.ilike(pattern)))
    rows = (await db.execute(query.order_by(Memory.pinned.desc(), Memory.importance_score.desc(), Memory.updated_at.desc()).limit(max(payload.limit * 3, payload.limit)))).scalars().all()
    ranked = []
    for memory in rows:
        score, reasons = score_memory(memory, payload.q)
        ranked.append({"memory": memory, "score": score, "reasons": reasons})
        memory.retrieval_count += 1
    ranked.sort(key=lambda item: item["score"], reverse=True)
    await emit_memory_event(db, current, "retrieved", None, {"workspace_id": payload.workspace_id, "query": payload.q, "result_count": min(len(ranked), payload.limit)})
    return ranked[: payload.limit]


async def ensure_default_categories(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> None:
    existing = (await db.execute(select(MemoryCategory.slug).where(MemoryCategory.organization_id == current.organization_id, MemoryCategory.workspace_id == workspace_id))).scalars().all()
    existing_set = set(existing)
    for slug in DEFAULT_CATEGORIES:
        if slug not in existing_set:
            db.add(MemoryCategory(organization_id=current.organization_id, workspace_id=workspace_id, name=slug.replace("_", " ").title(), slug=slug, description=f"Default {slug} memories", default_privacy_level="internal", created_by_user_id=current.user.id, updated_by_user_id=current.user.id))


async def analytics(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    rows = (await db.execute(select(Memory.memory_type, func.count()).where(Memory.organization_id == current.organization_id, Memory.workspace_id == workspace_id, Memory.deleted_at.is_(None)).group_by(Memory.memory_type))).all()
    privacy = (await db.execute(select(Memory.privacy_level, func.count()).where(Memory.organization_id == current.organization_id, Memory.workspace_id == workspace_id, Memory.deleted_at.is_(None)).group_by(Memory.privacy_level))).all()
    total = sum(int(row[1]) for row in rows)
    active = (await db.execute(select(func.count()).select_from(Memory).where(Memory.organization_id == current.organization_id, Memory.workspace_id == workspace_id, Memory.status == "active", Memory.deleted_at.is_(None)))).scalar_one()
    archived = (await db.execute(select(func.count()).select_from(Memory).where(Memory.organization_id == current.organization_id, Memory.workspace_id == workspace_id, Memory.status == "archived", Memory.deleted_at.is_(None)))).scalar_one()
    pinned = (await db.execute(select(func.count()).select_from(Memory).where(Memory.organization_id == current.organization_id, Memory.workspace_id == workspace_id, Memory.pinned.is_(True), Memory.deleted_at.is_(None)))).scalar_one()
    return {"total_memories": int(total), "active_memories": int(active or 0), "archived_memories": int(archived or 0), "pinned_memories": int(pinned or 0), "by_type": {row[0]: int(row[1]) for row in rows}, "by_privacy": {row[0]: int(row[1]) for row in privacy}, "observability": {"retrieval_latency_ms": "tracked_by_memory_events", "cache_hit_rate": "future", "growth": "memory_statistics", "embedding_provider": "not_configured"}}