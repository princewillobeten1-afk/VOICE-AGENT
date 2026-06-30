from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class EmbeddingResult:
    vector_ref: str
    dimensions: int
    token_count: int
    provider: str
    model: str | None = None


@dataclass(frozen=True)
class VectorSearchResult:
    chunk_id: str
    score: float
    provider_payload: dict


@dataclass(frozen=True)
class RerankResult:
    chunk_id: str
    score: float
    reason: str


class EmbeddingProvider(Protocol):
    name: str

    async def embed(self, text: str, config: dict) -> EmbeddingResult:
        ...


class VectorStoreProvider(Protocol):
    name: str

    async def upsert(self, chunk_id: str, vector_ref: str, metadata: dict) -> None:
        ...

    async def search(self, query_ref: str, filters: dict, limit: int) -> list[VectorSearchResult]:
        ...


class RerankerProvider(Protocol):
    name: str

    async def rerank(self, query: str, candidates: list[dict], config: dict) -> list[RerankResult]:
        ...


class PlaceholderEmbeddingProvider:
    name = "placeholder-embedding"

    async def embed(self, text: str, config: dict) -> EmbeddingResult:
        dimensions = int(config.get("dimensions", 1536))
        return EmbeddingResult(vector_ref=f"placeholder://embedding/{abs(hash(text))}", dimensions=dimensions, token_count=max(1, len(text.split())), provider="placeholder", model=config.get("model"))


class MetadataOnlyVectorStore:
    name = "metadata-only-vector-store"

    async def upsert(self, chunk_id: str, vector_ref: str, metadata: dict) -> None:
        return None

    async def search(self, query_ref: str, filters: dict, limit: int) -> list[VectorSearchResult]:
        return []


class PlaceholderReranker:
    name = "placeholder-reranker"

    async def rerank(self, query: str, candidates: list[dict], config: dict) -> list[RerankResult]:
        results = []
        terms = {term.lower() for term in query.split() if len(term) > 2}
        for candidate in candidates:
            text = f"{candidate.get('title', '')} {candidate.get('text_preview', '')}".lower()
            matches = sum(1 for term in terms if term in text)
            score = float(candidate.get("score", 0)) + min(0.25, matches * 0.05)
            results.append(RerankResult(chunk_id=str(candidate["id"]), score=round(score, 4), reason="placeholder text overlap"))
        return sorted(results, key=lambda item: item.score, reverse=True)


class RetrievalProviderRegistry:
    def __init__(self) -> None:
        self.embedding = PlaceholderEmbeddingProvider()
        self.vector_store = MetadataOnlyVectorStore()
        self.reranker = PlaceholderReranker()

    def catalog(self) -> list[dict]:
        return [
            {"type": "embedding", "provider": "openai", "status": "architecture_ready", "capabilities": ["text_embeddings", "batching"]},
            {"type": "embedding", "provider": "cohere", "status": "architecture_ready", "capabilities": ["multilingual", "rerank_pairing"]},
            {"type": "embedding", "provider": "google", "status": "architecture_ready", "capabilities": ["enterprise_regions"]},
            {"type": "embedding", "provider": "voyage", "status": "architecture_ready", "capabilities": ["retrieval_optimized"]},
            {"type": "embedding", "provider": "jina", "status": "architecture_ready", "capabilities": ["long_context"]},
            {"type": "embedding", "provider": "local", "status": "architecture_ready", "capabilities": ["self_hosted"]},
            {"type": "vector_store", "provider": "pinecone", "status": "architecture_ready", "capabilities": ["managed", "metadata_filters"]},
            {"type": "vector_store", "provider": "weaviate", "status": "architecture_ready", "capabilities": ["hybrid", "self_hosted"]},
            {"type": "vector_store", "provider": "qdrant", "status": "architecture_ready", "capabilities": ["filters", "self_hosted"]},
            {"type": "vector_store", "provider": "milvus", "status": "architecture_ready", "capabilities": ["scale"]},
            {"type": "vector_store", "provider": "pgvector", "status": "architecture_ready", "capabilities": ["postgres", "local_dev"]},
            {"type": "vector_store", "provider": "chroma", "status": "architecture_ready", "capabilities": ["local_dev"]},
            {"type": "vector_store", "provider": "elasticsearch", "status": "architecture_ready", "capabilities": ["hybrid", "keyword"]},
            {"type": "reranker", "provider": "cross_encoder", "status": "architecture_ready", "capabilities": ["precision"]},
            {"type": "reranker", "provider": "llm", "status": "architecture_ready", "capabilities": ["reasoned_ranking"]},
        ]


provider_registry = RetrievalProviderRegistry()