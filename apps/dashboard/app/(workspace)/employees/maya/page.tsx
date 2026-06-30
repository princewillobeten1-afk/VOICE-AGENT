"use client";

import { Archive, Copy, Download, History, Play, Rocket, Settings } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Skeleton } from "@voicesense/ui";
import { profileActivity, profileTabs, versionHistory } from "../../../../lib/employee-builder-data";

export default function MayaProfilePage() {
  return (
    <div className="builder-page">
      <header className="builder-hero"><div><p className="ws-kicker">AI employee profile</p><h1>Maya is configured for customer success conversations with policy-safe escalation.</h1><p>Manage overview, configuration, activity, conversations, analytics, knowledge, integrations, memory, version history, and settings from one profile.</p></div><div className="builder-actions"><Button><Play size={16} />Open playground</Button><Button variant="outline"><Rocket size={16} />Publish changes</Button><Button variant="outline"><Settings size={16} />Settings</Button></div></header>

      <nav className="profile-tabs" aria-label="Profile sections">{profileTabs.map((tab) => <a className={tab === "Overview" ? "is-active" : ""} href="#" key={tab}>{tab}</a>)}</nav>

      <section className="profile-grid">
        <article className="builder-card profile-overview"><div className="builder-avatar large">MA</div><div><p className="ws-kicker">Published employee</p><h2>Maya</h2><p>Customer Success Agent for billing, refunds, subscription retention, and safe handoffs.</p><div className="builder-chip-list"><span>Voice</span><span>Chat</span><span>Email</span><span>CRM read</span><span>Refund approval</span></div></div><Badge variant="success">Live</Badge></article>
        <article className="builder-card"><div className="builder-panel-head"><h2>Readiness</h2><Badge variant="warning">2 warnings</Badge></div><div className="builder-policy-list"><div><strong>Prompt policy</strong><p>Passed validation with approved refund language.</p></div><div><strong>Knowledge</strong><p>Billing policy attached. Help center review due in 4 days.</p></div><div><strong>Tools</strong><p>CRM is read-only. Refund preview requires approval.</p></div></div></article>
      </section>

      <section className="profile-grid three"><ProfilePanel title="Activity">{profileActivity.map((item) => <div className="profile-activity" key={item.title}><span>{item.time}</span><item.icon size={17} /><div><strong>{item.title}</strong><p>{item.detail}</p></div></div>)}</ProfilePanel><ProfilePanel title="Version history">{versionHistory.map((item) => <div className="profile-version" key={item.version}><div><strong>{item.version}</strong><p>{item.summary}</p></div><Badge variant={item.status === "Published" ? "success" : "neutral"}>{item.status}</Badge><small>{item.date}</small></div>)}</ProfilePanel><ProfilePanel title="Management actions"><div className="profile-action-list"><Button variant="outline"><Copy size={15} />Duplicate</Button><Button variant="outline"><Download size={15} />Export configuration</Button><Button variant="outline"><History size={15} />Rollback</Button><Button variant="destructive"><Archive size={15} />Archive</Button></div></ProfilePanel></section>

      <section className="builder-template-strip"><EmptyState title="No live conversations in this preview" description="Conversation management will connect when real channels are implemented." /><div className="builder-card"><Skeleton className="builder-skeleton" /><Skeleton className="builder-skeleton-line" /></div><ErrorState title="Analytics placeholder" description="Analytics panels are wired as layout foundation until real runtime events are available." onRetry={() => undefined} /></section>
    </div>
  );
}

function ProfilePanel({ title, children }: { title: string; children: React.ReactNode }) {
  return <article className="builder-card"><div className="builder-panel-head"><h2>{title}</h2></div><div className="profile-panel-list">{children}</div></article>;
}