"use client";

import { Archive, FileText, FolderOpen, Globe2, History, KeyRound, Plus, RefreshCw, Search, Settings, UploadCloud } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { activityFeed, categories, documents, knowledgeBases, knowledgeStats, qualityChecks, sourceTypes, uploadItems, websiteConfigs } from "../../../lib/knowledge-data";

export default function KnowledgePage() {
  return (
    <div className="knowledge-page">
      <header className="knowledge-hero">
        <div><p className="ws-kicker">Enterprise knowledge</p><h1>Manage every business knowledge asset AI employees will eventually learn from.</h1><p>Create knowledge bases, organize content, govern permissions, manage versions, configure sync sources, and prepare clean assets for the future RAG engine.</p></div>
        <div className="knowledge-actions"><Button><UploadCloud size={16} />Upload</Button><Button variant="outline"><Plus size={16} />New base</Button><Button variant="outline"><Settings size={16} />Settings</Button></div>
      </header>

      <section className="knowledge-stat-grid">{knowledgeStats.map((stat) => <article className={`knowledge-card knowledge-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="knowledge-toolbar"><div className="knowledge-category-row">{categories.slice(0, 7).map((category) => <button className={category === "All" ? "is-active" : ""} type="button" key={category}>{category}</button>)}</div><div className="knowledge-search"><SearchInput placeholder="Search documents, websites, FAQs" /><Button variant="outline" size="sm"><Search size={15} />Search</Button></div></section>

      <section className="knowledge-main-grid">
        <div className="knowledge-left-stack">
          <KnowledgePanel title="Knowledge bases" action={<Button variant="outline" size="sm"><Plus size={15} />Create</Button>}><div className="knowledge-base-grid">{knowledgeBases.map((base) => <article className="knowledge-base-card" key={base.name}><div><FolderOpen size={18} /><Badge variant={base.status === "Published" ? "success" : base.status === "Review" ? "warning" : "info"}>{base.status}</Badge></div><strong>{base.name}</strong><p>{base.owner} - {base.visibility}</p><span>{base.docs} documents</span><Progress value={base.health} /></article>)}</div></KnowledgePanel>
          <KnowledgePanel title="Content explorer" action={<Button variant="outline" size="sm"><Archive size={15} />Bulk actions</Button>}><div className="knowledge-table"><div className="knowledge-row knowledge-head"><span>Document</span><span>Type</span><span>Base</span><span>Status</span><span>Freshness</span><span>Updated</span></div>{documents.map((doc) => <div className="knowledge-row" key={doc.title}><span><FileText size={16} />{doc.title}</span><span>{doc.type}</span><span>{doc.base}</span><span><Badge variant={doc.status === "Published" ? "success" : doc.status === "Validation" ? "warning" : "info"}>{doc.status}</Badge></span><span>{doc.freshness}</span><span>{doc.updated}</span></div>)}</div></KnowledgePanel>
          <KnowledgePanel title="Source architecture"><div className="knowledge-source-grid">{sourceTypes.map((source) => <article className="knowledge-source" key={source.label}><source.icon size={18} /><strong>{source.label}</strong><p>{source.detail}</p><Badge>{source.status}</Badge></article>)}</div></KnowledgePanel>
        </div>

        <aside className="knowledge-side-stack">
          <KnowledgePanel title="Upload center"><div className="knowledge-upload-zone"><UploadCloud size={26} /><strong>Drop files or folders</strong><p>Multi-file, folder upload, validation, duplicate detection, resume, and cancel states are modeled.</p><Button variant="outline" size="sm">Browse files</Button></div><div className="knowledge-upload-list">{uploadItems.map((item) => <div key={item.name}><div><strong>{item.name}</strong><span>{item.status}</span></div><Progress value={item.progress} /></div>)}</div></KnowledgePanel>
          <KnowledgePanel title="Website management"><div className="knowledge-website-list">{websiteConfigs.map((site) => <div key={site.url}><Globe2 size={16} /><span><strong>{site.url}</strong><small>{site.paths} - {site.schedule}</small></span><Badge>{site.status}</Badge></div>)}</div></KnowledgePanel>
          <KnowledgePanel title="Quality checks"><div className="knowledge-quality-grid">{qualityChecks.map((check) => <div key={check.label}><check.icon size={16} /><span>{check.label}</span><strong>{check.value}</strong></div>)}</div></KnowledgePanel>
        </aside>
      </section>

      <section className="knowledge-bottom-grid"><KnowledgePanel title="Activity feed"><div className="knowledge-activity-list">{activityFeed.map((event) => <div className="knowledge-activity" key={`${event.time}-${event.title}`}><span>{event.time}</span><event.icon size={16} /><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></KnowledgePanel><KnowledgePanel title="Version governance"><div className="knowledge-version-box"><History size={22} /><strong>Draft, publish, rollback-ready</strong><p>Every content update creates version history and activity records. Rollback is API-ready for future workflow polish.</p><Button variant="outline" size="sm"><History size={15} />View versions</Button></div></KnowledgePanel><KnowledgePanel title="Permissions"><div className="knowledge-version-box"><KeyRound size={22} /><strong>Enterprise access model</strong><p>Organization, workspace, team, role, reader, editor, and administrator grants are modeled for knowledge assets.</p><Button variant="outline" size="sm"><KeyRound size={15} />Manage access</Button></div></KnowledgePanel></section>

      <section className="knowledge-state-grid"><EmptyState title="RAG is intentionally disabled" description="This platform prepares governed content. Embeddings, semantic search, vector databases, and AI retrieval come later." action={<Button variant="outline" size="sm"><RefreshCw size={15} />Review sync plan</Button>} /><div className="knowledge-card"><Skeleton className="knowledge-skeleton" /><Skeleton className="knowledge-skeleton-line" /><Skeleton className="knowledge-skeleton-line" /></div><ErrorState title="Crawler not implemented" description="Website registration and crawl configuration are ready, but crawling is out of scope for Task 016A." onRetry={() => undefined} /></section>
    </div>
  );
}

function KnowledgePanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="knowledge-card"><div className="knowledge-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}