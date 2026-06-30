import { Activity, BarChart3, Blocks, CheckCircle2, Clock3, DatabaseZap, FileSearch, Gauge, KeyRound, Layers3, ListFilter, Network, Search, Settings, ShieldCheck, SlidersHorizontal, Sparkles, Zap } from "lucide-react";

export const retrievalStats = [
  { label: "Indexed chunks", value: "1.28M", detail: "42.8k documents", icon: Layers3, tone: "green" },
  { label: "Avg retrieval", value: "86 ms", detail: "p95 142 ms", icon: Gauge, tone: "blue" },
  { label: "Context quality", value: "94%", detail: "+3.2% this week", icon: Sparkles, tone: "purple" },
  { label: "Permission checks", value: "100%", detail: "Strict tenant filtering", icon: ShieldCheck, tone: "amber" },
];

export const retrievalIndexes = [
  { name: "Customer Support Hybrid", base: "Customer Support", provider: "pgvector-ready", embedding: "text-embedding-3-large", status: "Ready", chunks: "684k", freshness: "8 min ago", coverage: 96 },
  { name: "Sales Enablement", base: "Sales Enablement", provider: "metadata-only", embedding: "placeholder", status: "Indexing", chunks: "318k", freshness: "34 min ago", coverage: 74 },
  { name: "Legal Restricted", base: "Legal Policies", provider: "qdrant-ready", embedding: "voyage-ready", status: "Ready", chunks: "88k", freshness: "Yesterday", coverage: 91 },
  { name: "Engineering Docs", base: "Engineering", provider: "weaviate-ready", embedding: "openai-ready", status: "Needs review", chunks: "192k", freshness: "3 days ago", coverage: 67 },
];

export const searchResults = [
  { title: "Refund policy v5.pdf", score: "0.92", reason: "semantic + keyword", tokens: 142, citation: "chunk 18", permission: "workspace" },
  { title: "Billing escalation SOP.docx", score: "0.88", reason: "reranked", tokens: 188, citation: "chunk 04", permission: "support-team" },
  { title: "Enterprise contract FAQ.md", score: "0.81", reason: "metadata boost", tokens: 96, citation: "chunk 11", permission: "sales-admin" },
];

export const chunkSamples = [
  { title: "Refund eligibility window", source: "Refund policy v5.pdf", strategy: "paragraph_aware", tokens: 142, checksum: "a91c...22f", state: "embedded" },
  { title: "Escalation requirements", source: "Billing escalation SOP.docx", strategy: "section_aware", tokens: 188, checksum: "b04a...91d", state: "embedded" },
  { title: "Enterprise exceptions", source: "Enterprise contract FAQ.md", strategy: "semantic", tokens: 96, checksum: "c33f...4a8", state: "queued" },
];

export const providerReadiness = [
  { name: "Embeddings", active: "Placeholder", future: "OpenAI, Cohere, Google, Voyage, Jina, local", icon: Zap, status: "Abstraction ready" },
  { name: "Vector stores", active: "Metadata-only", future: "pgvector, Pinecone, Weaviate, Qdrant, Milvus, Chroma", icon: DatabaseZap, status: "Adapter ready" },
  { name: "Reranking", active: "Heuristic", future: "Cohere, Voyage, Jina, custom rerankers", icon: SlidersHorizontal, status: "Interface ready" },
  { name: "Permissions", active: "Strict tenant scope", future: "Team, role, document, collection grants", icon: KeyRound, status: "Always-on" },
];

export const retrievalEvents = [
  { time: "10:42", title: "Support index refreshed", detail: "8,212 chunks prepared for hybrid retrieval.", icon: CheckCircle2 },
  { time: "10:18", title: "Search request traced", detail: "Query assembled 3 citations inside a 4k token budget.", icon: Search },
  { time: "09:57", title: "Provider config updated", detail: "Voyage adapter priority moved behind placeholder fallback.", icon: Settings },
  { time: "09:31", title: "Permission filter applied", detail: "12 restricted chunks removed before reranking.", icon: ShieldCheck },
];

export const retrievalMetrics = [
  { label: "Cache hit rate", value: "Future", icon: Activity },
  { label: "Embedding spend", value: "Tracked by jobs", icon: BarChart3 },
  { label: "Rerank latency", value: "21 ms", icon: Clock3 },
  { label: "Context tokens", value: "2.7k avg", icon: Blocks },
];

export const retrievalIcons = { FileSearch, ListFilter, Network, Search };
