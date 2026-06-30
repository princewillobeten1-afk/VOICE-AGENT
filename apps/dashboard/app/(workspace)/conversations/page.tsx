"use client";

import { AlertTriangle, BrainCircuit, Filter, Handshake, MessageSquareText, Play, RefreshCw, Search, Settings } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { activeSessions, analyticsCards, channelAdapters, contextSources, conversationStats, conversationTimeline, engineChecks, goals, historyRows } from "../../../lib/conversation-data";

export default function ConversationsPage() {
  return (
    <div className="conversation-page">
      <header className="conversation-hero">
        <div><p className="ws-kicker">Universal conversation engine</p><h1>Manage every AI employee interaction across voice, chat, email, SMS, and future channels.</h1><p>The engine keeps conversation state, sessions, context, goals, turn taking, handoff readiness, and analytics consistent across all communication adapters.</p></div>
        <div className="conversation-actions"><Button><Play size={16} />Open live viewer</Button><Button variant="outline"><Settings size={16} />Engine settings</Button></div>
      </header>

      <section className="conversation-stat-grid" aria-label="Conversation summary">{conversationStats.map((stat) => <article className={`conversation-card conversation-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="conversation-main-grid">
        <div className="conversation-left-stack">
          <ConversationPanel title="Live conversation timeline" action={<Badge>Simulation</Badge>}><div className="conversation-timeline">{conversationTimeline.map((item) => <div className="conversation-event" key={`${item.time}-${item.event}`}><span>{item.time}</span><item.icon size={16} /><div><strong>{item.event}</strong><p>{item.detail}</p></div></div>)}</div></ConversationPanel>

          <ConversationPanel title="Conversation history" action={<div className="conversation-search"><SearchInput placeholder="Search conversations" /><Button variant="outline" size="sm"><Filter size={15} />Filter</Button></div>}><div className="conversation-table" role="table" aria-label="Conversation history"><div className="conversation-row conversation-head" role="row"><span>Subject</span><span>Channel</span><span>Status</span><span>Employee</span><span>Updated</span></div>{historyRows.map((row) => <div className="conversation-row" role="row" key={`${row.subject}-${row.channel}`}><span><MessageSquareText size={16} />{row.subject}</span><span>{row.channel}</span><span><Badge variant={row.status === "Completed" ? "success" : row.status === "Handoff" ? "warning" : "info"}>{row.status}</Badge></span><span>{row.employee}</span><span>{row.updated}</span></div>)}</div></ConversationPanel>

          <ConversationPanel title="Goal progress"><div className="conversation-goal-list">{goals.map((goal) => <div key={goal.name}><div><strong>{goal.name}</strong><Badge variant={goal.status === "Complete" ? "success" : "info"}>{goal.status}</Badge></div><p>{goal.detail}</p><Progress value={goal.progress} /></div>)}</div></ConversationPanel>
        </div>

        <aside className="conversation-side-stack">
          <ConversationPanel title="Active sessions"><div className="conversation-session-list">{activeSessions.map((session) => <div className="conversation-session" key={session.id}><div><strong>{session.id}</strong><p>{session.channel} - {session.topic}</p></div><Badge variant={session.state === "Paused" ? "warning" : "success"}>{session.state}</Badge><span>{session.speaker}</span><small>{session.expires}</small></div>)}</div></ConversationPanel>
          <ConversationPanel title="Context flow"><div className="conversation-context-grid">{contextSources.map((source) => <div key={source.label}><source.icon size={16} /><span>{source.label}</span><strong>{source.value}</strong></div>)}</div></ConversationPanel>
          <ConversationPanel title="Analytics"><div className="conversation-analytics-grid">{analyticsCards.map((item) => <div key={item.label}><item.icon size={16} /><span>{item.label}</span><strong>{item.value}</strong></div>)}</div></ConversationPanel>
        </aside>
      </section>

      <section className="conversation-channel-grid"><ConversationPanel title="Channel adapters"><div className="conversation-adapter-grid">{channelAdapters.map((adapter) => <article className="conversation-adapter" key={adapter.channel}><div><adapter.icon size={18} /><Badge variant={adapter.status === "Ready" ? "success" : adapter.status === "Future" ? "neutral" : "info"}>{adapter.status}</Badge></div><strong>{adapter.channel}</strong><p>{adapter.adapter}</p><div>{adapter.capabilities.map((capability) => <span key={capability}>{capability}</span>)}</div></article>)}</div></ConversationPanel><ConversationPanel title="Engine readiness"><div className="conversation-check-grid">{engineChecks.map((check) => <div key={check.label}><check.icon size={16} /><span>{check.label}</span><strong>{check.state}</strong></div>)}</div></ConversationPanel></section>

      <section className="conversation-state-grid"><EmptyState title="No live human handoff" description="Live agent transfer is architecture-ready. This task prepares summaries and state transfer without implementing live agents." action={<Button variant="outline" size="sm"><Handshake size={15} />Review handoff</Button>} /><div className="conversation-card"><Skeleton className="conversation-skeleton" /><Skeleton className="conversation-skeleton-line" /><Skeleton className="conversation-skeleton-line" /></div><ErrorState title="Workflow execution disabled" description="Workflow hooks are tracked in state, but execution remains out of scope for Task 014." onRetry={() => undefined} /></section>
    </div>
  );
}

function ConversationPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="conversation-card"><div className="conversation-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}