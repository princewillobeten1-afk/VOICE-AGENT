from datetime import UTC, datetime
from time import perf_counter
from uuid import UUID
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import DomainEvent
from app.identity.dependencies import CurrentUser
from app.knowledge.models import Document, KnowledgeBase, KnowledgePermission
from app.notifications.service import publish_domain_event
from app.retrieval.models import EmbeddingJob, RetrievalChunk, RetrievalIndex, RetrievalMetric, RetrievalProviderConfig, RetrievalRequest, RetrievalSetting, SearchLog
from app.retrieval.providers import provider_registry


def provider_config_dict(item: RetrievalProviderConfig) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "name": item.name, "provider_type": item.provider_type, "provider": item.provider, "status": item.status, "priority": item.priority, "secret_ref": item.secret_ref, "model": item.model, "dimensions": item.dimensions, "capabilities": item.capabilities, "config": item.config, "health_state": item.health_state, "created_at": item.created_at, "updated_at": item.updated_at}


def setting_dict(item: RetrievalSetting) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "knowledge_base_id": item.knowledge_base_id, "chunking_strategy": item.chunking_strategy, "chunk_size": item.chunk_size, "chunk_overlap": item.chunk_overlap, "embedding_provider_config_id": item.embedding_provider_config_id, "vector_provider_config_id": item.vector_provider_config_id, "reranker_provider_config_id": item.reranker_provider_config_id, "hybrid_weights": item.hybrid_weights, "token_budget": item.token_budget, "metadata_filters": item.metadata_filters, "permission_mode": item.permission_mode, "cache_policy": item.cache_policy, "created_at": item.created_at, "updated_at": item.updated_at}


def index_dict(item: RetrievalIndex) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "knowledge_base_id": item.knowledge_base_id, "name": item.name, "status": item.status, "vector_store_provider": item.vector_store_provider, "vector_store_ref": item.vector_store_ref, "embedding_provider": item.embedding_provider, "embedding_model": item.embedding_model, "dimensions": item.dimensions, "chunk_count": item.chunk_count, "document_count": item.document_count, "size_bytes": item.size_bytes, "last_indexed_at": item.last_indexed_at, "metadata_json": item.metadata_json, "created_at": item.created_at, "updated_at": item.updated_at}


def chunk_dict(item: RetrievalChunk) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "document_id": item.document_id, "index_id": item.index_id, "chunk_index": item.chunk_index, "chunk_strategy": item.chunk_strategy, "content_ref": item.content_ref, "text_preview": item.text_preview, "token_count": item.token_count, "char_count": item.char_count, "language": item.language, "section_title": item.section_title, "metadata_json": item.metadata_json, "embedding_state": item.embedding_state, "vector_ref": item.vector_ref, "checksum": item.checksum, "status": item.status, "created_at": item.created_at}


def job_dict(item: EmbeddingJob) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "document_id": item.document_id, "index_id": item.index_id, "job_type": item.job_type, "status": item.status, "provider": item.provider, "model": item.model, "chunk_count": item.chunk_count, "processed_chunks": item.processed_chunks, "error_message": item.error_message, "started_at": item.started_at, "finished_at": item.finished_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


def request_dict(item: RetrievalRequest) -> dict:
    return {"id": item.id, "knowledge_base_id": item.knowledge_base_id, "agent_id": item.agent_id, "conversation_id": item.conversation_id, "query": item.query, "search_mode": item.search_mode, "status": item.status, "filters": item.filters, "weights": item.weights, "result_count": item.result_count, "latency_ms": item.latency_ms, "token_budget": item.token_budget, "context_tokens": item.context_tokens, "permission_summary": item.permission_summary, "metadata_json": item.metadata_json, "created_at": item.created_at}


async def emit_retrieval_event(db: AsyncSession, current: CurrentUser, name: str, workspace_id: UUID, aggregate_id: UUID, payload: dict) -> None:
    await publish_domain_event(db, DomainEvent(organization_id=current.organization_id, workspace_id=workspace_id, actor_user_id=current.user.id, name=f"retrieval.{name}", aggregate_type="retrieval", aggregate_id=aggregate_id, source="retrieval-engine", payload=payload, metadata={"engine": "rag"}))


def split_text(text: str, strategy: str, chunk_size: int, overlap: int) -> list[str]:
    raw = (text or "").replace("\r", "").strip()
    clean = " ".join(raw.split())
    if not clean:
        return []
    if strategy in {"paragraph_aware", "section_aware", "semantic"}:
        parts = [" ".join(part.split()) for part in raw.split("\n\n") if part.strip()]
        if len(parts) > 1:
            return parts
    chunks: list[str] = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(clean), step):
        chunks.append(clean[start : start + chunk_size])
        if start + chunk_size >= len(clean):
            break
    return chunks


def document_text(document: Document) -> str:
    metadata = document.metadata_json or {}
    custom = document.custom_metadata or {}
    return metadata.get("content") or custom.get("content") or f"{document.title}. Content body is managed by the Knowledge Platform and will be loaded by ingestion workers in production."


async def create_index_job(db: AsyncSession, current: CurrentUser, payload) -> EmbeddingJob:
    index = await db.get(RetrievalIndex, payload.index_id) if payload.index_id else None
    if index is None:
        kb = await db.get(KnowledgeBase, payload.knowledge_base_id)
        index = RetrievalIndex(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, name=f"{kb.name if kb else 'Knowledge'} Index", status="indexing", vector_store_provider="metadata_only", embedding_provider="placeholder", metadata_json={"strategy": payload.strategy}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
        db.add(index)
        await db.flush()
    docs_query = select(Document).where(Document.organization_id == current.organization_id, Document.workspace_id == payload.workspace_id, Document.knowledge_base_id == payload.knowledge_base_id, Document.deleted_at.is_(None))
    if payload.document_id:
        docs_query = docs_query.where(Document.id == payload.document_id)
    docs = (await db.execute(docs_query.limit(200))).scalars().all()
    job = EmbeddingJob(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, document_id=payload.document_id, index_id=index.id, job_type="reindex" if payload.strategy == "full" else "index", status="completed", provider="placeholder", model="metadata-scorer", started_at=datetime.now(UTC), metadata_json={"chunking_strategy": payload.chunking_strategy, "note": "No real embeddings generated in this foundation task."}, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(job)
    chunk_total = 0
    for doc in docs:
        chunks = split_text(document_text(doc), payload.chunking_strategy, payload.chunk_size, payload.chunk_overlap)
        for idx, text in enumerate(chunks):
            embedding = await provider_registry.embedding.embed(text, {"model": "metadata-scorer"})
            chunk = RetrievalChunk(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=doc.knowledge_base_id, document_id=doc.id, index_id=index.id, chunk_index=idx, chunk_strategy=payload.chunking_strategy, text_preview=text[:600], token_count=embedding.token_count, char_count=len(text), language="en", metadata_json={"document_title": doc.title, "content_type": doc.content_type, "status": doc.status}, embedding_state={"status": "placeholder", "provider": embedding.provider, "dimensions": embedding.dimensions}, vector_ref=embedding.vector_ref, checksum=doc.checksum, status="ready", created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
            db.add(chunk)
            chunk_total += 1
    job.chunk_count = chunk_total
    job.processed_chunks = chunk_total
    job.finished_at = datetime.now(UTC)
    index.status = "ready"
    index.chunk_count += chunk_total
    index.document_count = len(docs)
    index.last_indexed_at = datetime.now(UTC)
    await emit_retrieval_event(db, current, "index.completed", payload.workspace_id, index.id, {"chunk_count": chunk_total, "document_count": len(docs)})
    return job


def score_chunk(chunk: RetrievalChunk, query: str, weights: dict) -> tuple[float, list[str]]:
    text = f"{chunk.text_preview or ''} {chunk.metadata_json.get('document_title', '')}".lower()
    terms = [term for term in query.lower().split() if len(term) > 2]
    matches = sum(1 for term in terms if term in text)
    keyword = (matches / max(1, len(terms))) if terms else 0
    semantic = min(1.0, keyword + 0.18)
    metadata = 0.2 if chunk.metadata_json.get("status") == "published" else 0.1
    recency = 0.1
    score = semantic * float(weights.get("semantic", 0.45)) + keyword * float(weights.get("keyword", 0.35)) + metadata * float(weights.get("metadata", 0.1)) + recency * float(weights.get("recency", 0.1))
    reasons = []
    if matches:
        reasons.append("keyword overlap")
    if semantic > keyword:
        reasons.append("semantic placeholder boost")
    if metadata:
        reasons.append("metadata eligible")
    return round(score, 4), reasons or ["eligible chunk"]


async def search_and_assemble(db: AsyncSession, current: CurrentUser, payload) -> dict:
    started = perf_counter()
    query = select(RetrievalChunk).where(RetrievalChunk.organization_id == current.organization_id, RetrievalChunk.workspace_id == payload.workspace_id, RetrievalChunk.deleted_at.is_(None), RetrievalChunk.status == "ready")
    if payload.knowledge_base_id:
        query = query.where(RetrievalChunk.knowledge_base_id == payload.knowledge_base_id)
    if payload.filters.get("document_id"):
        query = query.where(RetrievalChunk.document_id == payload.filters["document_id"])
    chunks = (await db.execute(query.order_by(RetrievalChunk.created_at.desc()).limit(300))).scalars().all()
    candidates = []
    for chunk in chunks:
        score, reasons = score_chunk(chunk, payload.query, payload.weights)
        candidates.append({"chunk": chunk, "score": score, "reasons": reasons, "id": chunk.id, "title": chunk.metadata_json.get("document_title"), "text_preview": chunk.text_preview})
    candidates.sort(key=lambda item: item["score"], reverse=True)
    selected = candidates[: payload.limit]
    if payload.rerank:
        reranked = await provider_registry.reranker.rerank(payload.query, selected, {})
        score_map = {item.chunk_id: item for item in reranked}
        for candidate in selected:
            rerank = score_map.get(str(candidate["chunk"].id))
            if rerank:
                candidate["score"] = rerank.score
                candidate["reasons"].append(rerank.reason)
        selected.sort(key=lambda item: item["score"], reverse=True)
    context_parts = []
    citations = []
    used_tokens = 0
    for item in selected:
        chunk = item["chunk"]
        tokens = int(chunk.token_count or 0)
        if used_tokens + tokens > payload.token_budget:
            continue
        used_tokens += tokens
        citation = {"document_id": str(chunk.document_id), "chunk_id": str(chunk.id), "title": chunk.metadata_json.get("document_title"), "score": item["score"]}
        citations.append(citation)
        context_parts.append(f"[{len(citations)}] {chunk.text_preview}")
    latency = int((perf_counter() - started) * 1000)
    req = RetrievalRequest(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, agent_id=payload.agent_id, conversation_id=payload.conversation_id, query=payload.query, search_mode=payload.search_mode, status="completed", filters=payload.filters, weights=payload.weights, result_count=len(selected), latency_ms=latency, token_budget=payload.token_budget, context_tokens=used_tokens, permission_summary={"mode": "strict", "organization_id": str(current.organization_id), "workspace_id": str(payload.workspace_id), "filtered": True}, metadata_json={"rerank": payload.rerank})
    db.add(req)
    await db.flush()
    db.add(SearchLog(organization_id=current.organization_id, workspace_id=payload.workspace_id, retrieval_request_id=req.id, event_type="search.completed", stage="context_assembly", payload={"result_count": len(selected), "citations": citations}, latency_ms=latency))
    return {"request": req, "selected": selected, "context": "\n\n".join(context_parts), "citations": citations, "tokens": used_tokens, "latency": latency}


async def metrics(db: AsyncSession, current: CurrentUser, workspace_id: UUID) -> dict:
    indexes = (await db.execute(select(func.count()).select_from(RetrievalIndex).where(RetrievalIndex.organization_id == current.organization_id, RetrievalIndex.workspace_id == workspace_id, RetrievalIndex.deleted_at.is_(None)))).scalar_one()
    chunks = (await db.execute(select(func.count()).select_from(RetrievalChunk).where(RetrievalChunk.organization_id == current.organization_id, RetrievalChunk.workspace_id == workspace_id, RetrievalChunk.deleted_at.is_(None)))).scalar_one()
    jobs = (await db.execute(select(func.count()).select_from(EmbeddingJob).where(EmbeddingJob.organization_id == current.organization_id, EmbeddingJob.workspace_id == workspace_id))).scalar_one()
    requests = (await db.execute(select(func.count()).select_from(RetrievalRequest).where(RetrievalRequest.organization_id == current.organization_id, RetrievalRequest.workspace_id == workspace_id))).scalar_one()
    avg_latency = (await db.execute(select(func.avg(RetrievalRequest.latency_ms)).where(RetrievalRequest.organization_id == current.organization_id, RetrievalRequest.workspace_id == workspace_id, RetrievalRequest.latency_ms.is_not(None)))).scalar_one_or_none()
    return {"indexes": int(indexes or 0), "chunks": int(chunks or 0), "embedding_jobs": int(jobs or 0), "retrieval_requests": int(requests or 0), "average_latency_ms": int(avg_latency) if avg_latency else None, "provider_catalog": provider_registry.catalog(), "observability": {"cache_hit_rate": "future", "embedding_usage": "tracked_by_jobs", "cost_estimates": "future", "permission_filtering": "strict"}}
