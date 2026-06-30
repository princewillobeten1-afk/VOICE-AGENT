"use client";

import { Activity, DatabaseZap, Eye, FileSearch, Play, RefreshCw, Search, Settings, ShieldCheck, SlidersHorizontal } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { chunkSamples, providerReadiness, retrievalEvents, retrievalIndexes, retrievalMetrics, retrievalStats, searchResults } from "../../../lib/retrieval-data";

export default function RetrievalPage() {
  return (
    <div className="retrieval-page">
      <header className="retrieval-hero">
        <div>
          <p className="ws-kicker">Enterprise retrieval</p>
          <h1>Govern indexing, hybrid search, chunk inspection, and context assembly for AI employees.</h1>
          <p>Manage the provider-agnostic RAG foundation that turns approved knowledge into permission-aware, citation-rich context without implementing LLM reasoning yet.</p>
        </div>
        <div className="retrieval-actions">
          <Button><Play size={16} />Run search</Button>
          <Button variant="outline"><RefreshCw size={16} />Reindex</Button>
          <Button variant="outline"><Settings size={16} />Providers</Button>
        </div>
      </header>

      <section className="retrieval-stat-grid">
        {retrievalStats.map((stat) => <article className={`retrieval-card retrieval-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}
      </section>

      <section className="retrieval-toolbar">
        <div className="retrieval-category-row"><button className="is-active" type="button">Hybrid</button><button type="button">Semantic</button><button type="button">Keyword</button><button type="button">Reranked</button><button type="button">Filtered</button></div>
        <div className="retrieval-search"><SearchInput placeholder="Search indexes, chunks, providers" /><Button variant="outline" size="sm"><Search size={15} />Search</Button></div>
      </section>

      <section className="retrieval-main-grid">
        <div className="retrieval-left-stack">
          <RetrievalPanel title="Index status" action={<Button variant="outline" size="sm"><RefreshCw size={15} />Refresh</Button>}>
            <div className="retrieval-table">
              <div className="retrieval-row retrieval-head"><span>Index</span><span>Base</span><span>Provider</span><span>Status</span><span>Chunks</span><span>Coverage</span></div>
              {retrievalIndexes.map((item) => <div className="retrieval-row" key={item.name}><span><DatabaseZap size={16} />{item.name}</span><span>{item.base}</span><span>{item.provider}</span><span><Badge variant={item.status === "Ready" ? "success" : item.status === "Indexing" ? "warning" : "info"}>{item.status}</Badge></span><span>{item.chunks}</span><span><Progress value={item.coverage} /></span></div>)}
            </div>
          </RetrievalPanel>

          <RetrievalPanel title="Search playground" action={<Button variant="outline" size="sm"><SlidersHorizontal size={15} />Tune</Button>}>
            <div className="retrieval-playground">
              <div className="retrieval-query-box"><SearchInput placeholder="How do we handle enterprise refund exceptions?" /><Button size="sm"><Play size={15} />Run</Button></div>
              <div className="retrieval-result-list">{searchResults.map((result) => <article key={result.title}><div><strong>{result.title}</strong><Badge>{result.score}</Badge></div><p>{result.reason} - {result.tokens} tokens - {result.citation}</p><span><ShieldCheck size={14} />{result.permission}</span></article>)}</div>
            </div>
          </RetrievalPanel>

          <RetrievalPanel title="Chunk viewer" action={<Button variant="outline" size="sm"><Eye size={15} />Inspect</Button>}>
            <div className="retrieval-chunk-grid">{chunkSamples.map((chunk) => <article key={chunk.title}><FileSearch size={18} /><strong>{chunk.title}</strong><p>{chunk.source}</p><div><Badge>{chunk.strategy}</Badge><span>{chunk.tokens} tokens</span></div><small>{chunk.checksum} - {chunk.state}</small></article>)}</div>
          </RetrievalPanel>
        </div>

        <aside className="retrieval-side-stack">
          <RetrievalPanel title="Retrieval inspector"><div className="retrieval-inspector"><strong>Pipeline</strong><p>Query normalization to permission filtering to hybrid candidate search to metadata boost to rerank to context assembly with citations.</p><div><span>Token budget</span><strong>4,000</strong></div><div><span>Selected chunks</span><strong>3 / 12</strong></div><div><span>Omitted</span><strong>9</strong></div></div></RetrievalPanel>
          <RetrievalPanel title="Provider settings"><div className="retrieval-provider-list">{providerReadiness.map((provider) => <div key={provider.name}><provider.icon size={16} /><span><strong>{provider.name}</strong><small>{provider.active}</small></span><Badge>{provider.status}</Badge><p>{provider.future}</p></div>)}</div></RetrievalPanel>
          <RetrievalPanel title="Index metrics"><div className="retrieval-metric-grid">{retrievalMetrics.map((metric) => <div key={metric.label}><metric.icon size={16} /><span>{metric.label}</span><strong>{metric.value}</strong></div>)}</div></RetrievalPanel>
        </aside>
      </section>

      <section className="retrieval-bottom-grid">
        <RetrievalPanel title="Recent retrieval activity"><div className="retrieval-event-list">{retrievalEvents.map((event) => <div className="retrieval-event" key={`${event.time}-${event.title}`}><span>{event.time}</span><event.icon size={16} /><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></RetrievalPanel>
        <EmptyState title="No production vector store connected" description="The engine is provider-ready, but this environment uses metadata-only retrieval until a real vector provider is configured." action={<Button variant="outline" size="sm"><Settings size={15} />Configure provider</Button>} />
        <div className="retrieval-card"><Skeleton className="retrieval-skeleton" /><Skeleton className="retrieval-skeleton-line" /><Skeleton className="retrieval-skeleton-line" /></div>
      </section>

      <section className="retrieval-state-grid"><ErrorState title="LLM generation intentionally disabled" description="Task 016B assembles retrieval context only. Conversation reasoning and response generation are owned by later AI runtime work." onRetry={() => undefined} /><EmptyState title="No chunk selected" description="Select a chunk in the inspector to review metadata, scores, permissions, and citation output." action={<Button variant="outline" size="sm"><Activity size={15} />Open inspector</Button>} /></section>
    </div>
  );
}

function RetrievalPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="retrieval-card"><div className="retrieval-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}

