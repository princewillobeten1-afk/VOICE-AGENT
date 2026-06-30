from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission
from app.retrieval.models import RetrievalChunk, RetrievalIndex, RetrievalProviderConfig, RetrievalSetting
from app.retrieval.providers import provider_registry
from app.retrieval.schemas import ChunkOut, ContextAssemblyOut, EmbeddingJobOut, IndexContentRequest, IndexCreate, IndexOut, ProviderConfigCreate, ProviderConfigOut, RetrievalMetricsOut, RetrievalRequestOut, RetrievalSettingCreate, RetrievalSettingOut, SearchRequest, SearchResult
from app.retrieval.service import chunk_dict, create_index_job, index_dict, job_dict, metrics, provider_config_dict, request_dict, search_and_assemble, setting_dict

router = APIRouter(prefix="/retrieval", tags=["retrieval-engine"])


@router.get("/providers")
async def provider_catalog(current: CurrentUser = Depends(require_permission(Permission.ORG_READ))):
    return {"providers": provider_registry.catalog(), "note": "Provider catalog only. Real provider calls are configured in future deployment tasks."}


@router.post("/provider-configs", response_model=ProviderConfigOut, status_code=status.HTTP_201_CREATED)
async def create_provider_config(payload: ProviderConfigCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    config = RetrievalProviderConfig(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, provider_type=payload.provider_type, provider=payload.provider, status=payload.status, priority=payload.priority, secret_ref=payload.secret_ref, model=payload.model, dimensions=payload.dimensions, capabilities=payload.capabilities, config=payload.config, health_state=payload.health_state, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(config)
    await db.flush()
    await audit(db, "retrieval.provider_config.created", current.user.id, current.organization_id, "retrieval_provider_config", config.id)
    await db.commit()
    return ProviderConfigOut(**provider_config_dict(config))


@router.get("/settings", response_model=list[RetrievalSettingOut])
async def list_settings(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(RetrievalSetting).where(RetrievalSetting.organization_id == current.organization_id, RetrievalSetting.workspace_id == workspace_id, RetrievalSetting.deleted_at.is_(None)).order_by(RetrievalSetting.updated_at.desc()))).scalars().all()
    return [RetrievalSettingOut(**setting_dict(item)) for item in rows]


@router.post("/settings", response_model=RetrievalSettingOut, status_code=status.HTTP_201_CREATED)
async def create_setting(payload: RetrievalSettingCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    setting = RetrievalSetting(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, chunking_strategy=payload.chunking_strategy, chunk_size=payload.chunk_size, chunk_overlap=payload.chunk_overlap, embedding_provider_config_id=payload.embedding_provider_config_id, vector_provider_config_id=payload.vector_provider_config_id, reranker_provider_config_id=payload.reranker_provider_config_id, hybrid_weights=payload.hybrid_weights, token_budget=payload.token_budget, metadata_filters=payload.metadata_filters, permission_mode=payload.permission_mode, cache_policy=payload.cache_policy, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(setting)
    await db.flush()
    await db.commit()
    return RetrievalSettingOut(**setting_dict(setting))


@router.get("/indexes", response_model=list[IndexOut])
async def list_indexes(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(RetrievalIndex).where(RetrievalIndex.organization_id == current.organization_id, RetrievalIndex.workspace_id == workspace_id, RetrievalIndex.deleted_at.is_(None)).order_by(RetrievalIndex.updated_at.desc()))).scalars().all()
    return [IndexOut(**index_dict(item)) for item in rows]


@router.post("/indexes", response_model=IndexOut, status_code=status.HTTP_201_CREATED)
async def create_index(payload: IndexCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    index = RetrievalIndex(organization_id=current.organization_id, workspace_id=payload.workspace_id, knowledge_base_id=payload.knowledge_base_id, name=payload.name, status="draft", vector_store_provider=payload.vector_store_provider, vector_store_ref=payload.vector_store_ref, embedding_provider=payload.embedding_provider, embedding_model=payload.embedding_model, dimensions=payload.dimensions, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(index)
    await db.flush()
    await db.commit()
    return IndexOut(**index_dict(index))


@router.post("/index-content", response_model=EmbeddingJobOut, status_code=status.HTTP_201_CREATED)
async def index_content(payload: IndexContentRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    job = await create_index_job(db, current, payload)
    await audit(db, "retrieval.index_content", current.user.id, current.organization_id, "embedding_job", job.id)
    await db.commit()
    return EmbeddingJobOut(**job_dict(job))


@router.post("/reindex", response_model=EmbeddingJobOut, status_code=status.HTTP_201_CREATED)
async def reindex_content(payload: IndexContentRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    full_payload = payload.model_copy(update={"strategy": "full"})
    job = await create_index_job(db, current, full_payload)
    await db.commit()
    return EmbeddingJobOut(**job_dict(job))


@router.get("/chunks", response_model=list[ChunkOut])
async def list_chunks(workspace_id: UUID, knowledge_base_id: UUID | None = None, document_id: UUID | None = None, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    query = select(RetrievalChunk).where(RetrievalChunk.organization_id == current.organization_id, RetrievalChunk.workspace_id == workspace_id, RetrievalChunk.deleted_at.is_(None))
    if knowledge_base_id:
        query = query.where(RetrievalChunk.knowledge_base_id == knowledge_base_id)
    if document_id:
        query = query.where(RetrievalChunk.document_id == document_id)
    rows = (await db.execute(query.order_by(RetrievalChunk.created_at.desc()).limit(100))).scalars().all()
    return [ChunkOut(**chunk_dict(item)) for item in rows]


@router.post("/search", response_model=list[SearchResult])
async def search(payload: SearchRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    assembled = await search_and_assemble(db, current, payload)
    await db.commit()
    return [SearchResult(chunk=ChunkOut(**chunk_dict(item["chunk"])), score=item["score"], reasons=item["reasons"], citation={"document_id": str(item["chunk"].document_id), "chunk_id": str(item["chunk"].id), "title": item["chunk"].metadata_json.get("document_title")}) for item in assembled["selected"]]


@router.post("/context", response_model=ContextAssemblyOut)
async def retrieve_context(payload: SearchRequest, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    assembled = await search_and_assemble(db, current, payload)
    await db.commit()
    return ContextAssemblyOut(retrieval_request_id=assembled["request"].id, query=payload.query, context=assembled["context"], citations=assembled["citations"], chunks=[SearchResult(chunk=ChunkOut(**chunk_dict(item["chunk"])), score=item["score"], reasons=item["reasons"], citation={"document_id": str(item["chunk"].document_id), "chunk_id": str(item["chunk"].id), "title": item["chunk"].metadata_json.get("document_title")}) for item in assembled["selected"]], token_budget=payload.token_budget, context_tokens=assembled["tokens"], permission_summary=assembled["request"].permission_summary, latency_ms=assembled["latency"])


@router.get("/metrics", response_model=RetrievalMetricsOut)
async def retrieval_metrics(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return RetrievalMetricsOut(**await metrics(db, current, workspace_id))

