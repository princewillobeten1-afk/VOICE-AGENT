"use client";

import { Archive, BrainCircuit, Filter, History, Link2, LockKeyhole, Plus, Search, Settings, Tags } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { memoryCategories, memoryHealth, memoryLayers, memoryPolicies, memoryRows, memoryStats, memoryTimeline, relatedMemories } from "../../../lib/memory-data";

export default function MemoryPage() {
  return (
    <div className="memory-page">
      <header className="memory-hero">
        <div><p className="ws-kicker">Advanced memory system</p><h1>Explore, govern, retrieve, and improve AI employee memory across every conversation.</h1><p>Manage short-term, working, long-term, episodic, semantic, organizational, shared, and session memory with privacy boundaries and version history.</p></div>
        <div className="memory-actions"><Button><Plus size={16} />Create memory</Button><Button variant="outline"><Settings size={16} />Policies</Button></div>
      </header>

      <section className="memory-stat-grid" aria-label="Memory summary">{memoryStats.map((stat) => <article className={`memory-card memory-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="memory-toolbar"><div className="memory-category-row">{memoryCategories.slice(0, 8).map((category) => <button className={category === "All" ? "is-active" : ""} type="button" key={category}>{category}</button>)}</div><div className="memory-search"><SearchInput placeholder="Search memories, facts, summaries" /><Button variant="outline" size="sm"><Filter size={15} />Filter</Button></div></section>

      <section className="memory-main-grid">
        <div className="memory-left-stack">
          <MemoryPanel title="Memory explorer" action={<Badge>Provider agnostic</Badge>}><div className="memory-table" role="table" aria-label="Memories"><div className="memory-row memory-head" role="row"><span>Memory</span><span>Type</span><span>Privacy</span><span>Score</span><span>Updated</span></div>{memoryRows.map((memory) => <div className="memory-row" role="row" key={memory.title}><span><BrainCircuit size={16} />{memory.title}{memory.pinned ? <Badge variant="warning">Pinned</Badge> : null}</span><span>{memory.type}</span><span><Badge variant={memory.privacy === "restricted" ? "warning" : memory.privacy === "private" ? "danger" : "info"}>{memory.privacy}</Badge></span><span>{memory.score}</span><span>{memory.updated}</span></div>)}</div></MemoryPanel>
          <MemoryPanel title="Memory layers"><div className="memory-layer-grid">{memoryLayers.map((layer) => <article className="memory-layer" key={layer.name}><layer.icon size={18} /><strong>{layer.name}</strong><p>{layer.detail}</p><Badge>{layer.status}</Badge></article>)}</div></MemoryPanel>
        </div>

        <aside className="memory-side-stack">
          <MemoryPanel title="Selected memory"><div className="memory-detail"><LockKeyhole size={22} /><strong>Ada prefers concise billing updates</strong><p>Long-term preference memory. Internal visibility, pinned, high confidence, version 3.</p><div><Badge>preferences</Badge><Badge>billing</Badge><Badge>customer</Badge></div><Progress value={91} /></div></MemoryPanel>
          <MemoryPanel title="Related memories"><div className="memory-related-list">{relatedMemories.map((item) => <div key={item.title}><Link2 size={16} /><span><strong>{item.title}</strong><small>{item.type} - {item.strength}</small></span></div>)}</div></MemoryPanel>
          <MemoryPanel title="Memory health"><div className="memory-health-grid">{memoryHealth.map((item) => <div key={item.label}><item.icon size={16} /><span>{item.label}</span><strong>{item.state}</strong></div>)}</div></MemoryPanel>
        </aside>
      </section>

      <section className="memory-bottom-grid"><MemoryPanel title="Timeline"><div className="memory-timeline">{memoryTimeline.map((event) => <div className="memory-event" key={`${event.time}-${event.event}`}><span>{event.time}</span><event.icon size={16} /><div><strong>{event.event}</strong><p>{event.detail}</p></div></div>)}</div></MemoryPanel><MemoryPanel title="Policies"><div className="memory-policy-list">{memoryPolicies.map((policy) => <div key={policy.name}><div><strong>{policy.name}</strong><Badge variant={policy.status === "Active" ? "success" : "warning"}>{policy.status}</Badge></div><p>{policy.scope} - {policy.retention}</p></div>)}</div></MemoryPanel><MemoryPanel title="Versioning"><div className="memory-version-box"><History size={22} /><strong>Trace every important update</strong><p>Version history, rollback readiness, merge records, archive events, and forget actions are modeled for enterprise audits.</p><Button variant="outline" size="sm"><Archive size={15} />View history</Button></div></MemoryPanel></section>

      <section className="memory-state-grid"><EmptyState title="No vector index connected" description="Task 015 intentionally avoids embeddings and vector databases. Retrieval uses metadata scoring until a future RAG task connects providers." action={<Button variant="outline" size="sm"><Search size={15} />Review retrieval</Button>} /><div className="memory-card"><Skeleton className="memory-skeleton" /><Skeleton className="memory-skeleton-line" /><Skeleton className="memory-skeleton-line" /></div><ErrorState title="Retention worker placeholder" description="Policies are modeled now. Background cleanup workers can enforce them in a later infrastructure task." onRetry={() => undefined} /></section>
    </div>
  );
}

function MemoryPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="memory-card"><div className="memory-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}