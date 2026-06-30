"use client";

import { AlertTriangle, AudioWaveform, CheckCircle2, Mic2, Play, RadioTower, RefreshCw, Settings, ShieldCheck, Volume2, Zap } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { activeVoiceSessions, latencyBudget, monitoringChecks, providerMatrix, streamEvents, voicePipeline, voiceSettings, voiceStats } from "../../../lib/voice-data";

export default function VoiceEnginePage() {
  return (
    <div className="voice-page">
      <header className="voice-hero">
        <div><p className="ws-kicker">Real-time voice engine</p><h1>Operate low-latency voice sessions, provider routing, interruptions, and streaming telemetry.</h1><p>The Voice Engine foundation keeps audio streaming, VAD, STT, conversation state, AI orchestration placeholders, TTS, monitoring, and recovery independently replaceable.</p></div>
        <div className="voice-actions"><Button><Play size={16} />Run test</Button><Button variant="outline"><Settings size={16} />Voice settings</Button></div>
      </header>

      <section className="voice-stat-grid" aria-label="Voice summary">{voiceStats.map((stat) => <article className={`voice-card voice-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="voice-main-grid">
        <div className="voice-left-stack">
          <VoicePanel title="Streaming pipeline" action={<Badge>Full duplex</Badge>}>
            <div className="voice-pipeline">{voicePipeline.map((stage, index) => <div className="voice-pipeline-step" key={stage.label}><span>{index + 1}</span><stage.icon size={18} /><div><strong>{stage.label}</strong><p>{stage.detail}</p></div><Badge variant="info">{stage.latency}</Badge></div>)}</div>
          </VoicePanel>

          <VoicePanel title="Active sessions" action={<div className="voice-search"><SearchInput placeholder="Search sessions" /><Button variant="outline" size="sm"><RefreshCw size={15} />Refresh</Button></div>}>
            <div className="voice-session-table" role="table" aria-label="Active voice sessions"><div className="voice-session-row voice-session-head" role="row"><span>Session</span><span>Employee</span><span>Channel</span><span>Status</span><span>Latency</span><span>Interrupts</span></div>{activeVoiceSessions.map((session) => <div className="voice-session-row" role="row" key={session.id}><span><RadioTower size={16} />{session.id}</span><span>{session.employee}</span><span>{session.channel}</span><span><Badge variant={session.status === "Active" ? "success" : session.status === "Recovering" ? "warning" : "neutral"}>{session.status}</Badge></span><span>{session.latency}</span><span>{session.interrupts}</span></div>)}</div>
          </VoicePanel>

          <VoicePanel title="Latency budget"><div className="voice-latency-list">{latencyBudget.map((item) => <div key={item.stage}><div><strong>{item.stage}</strong><span>{item.actual} / {item.target} ms</span></div><Progress value={Math.min(100, Math.round((item.actual / item.target) * 100))} /></div>)}</div></VoicePanel>
        </div>

        <aside className="voice-side-stack">
          <VoicePanel title="Provider abstraction"><div className="voice-provider-list">{providerMatrix.map((provider) => <div className="voice-provider" key={provider.type}><div><strong>{provider.type}</strong><p>{provider.primary} to {provider.fallback}</p></div><Badge variant={provider.status === "Ready" ? "success" : "info"}>{provider.status}</Badge><div className="voice-chip-row">{provider.capabilities.map((capability) => <span key={capability}>{capability}</span>)}</div></div>)}</div></VoicePanel>
          <VoicePanel title="Voice configuration"><div className="voice-settings-grid">{voiceSettings.map((item) => <div key={item.label}><item.icon size={17} /><span>{item.label}</span><strong>{item.value}</strong></div>)}</div></VoicePanel>
          <VoicePanel title="Monitoring checks"><div className="voice-check-list">{monitoringChecks.map((check) => <div key={check.label}><check.icon size={16} /><span>{check.label}</span><strong>{check.state}</strong></div>)}</div></VoicePanel>
        </aside>
      </section>

      <section className="voice-event-grid">
        <VoicePanel title="Stream event timeline" action={<Badge>Simulation</Badge>}><div className="voice-event-list">{streamEvents.map((event) => <div className="voice-event" key={`${event.time}-${event.event}`}><span>{event.time}</span><event.icon size={16} /><div><strong>{event.event}</strong><p>{event.stage} - {event.detail}</p></div></div>)}</div></VoicePanel>
        <VoicePanel title="Voice test console"><div className="voice-test-console"><div><Mic2 size={20} /><strong>Inbound audio test</strong><p>Send a simulated audio chunk through VAD and STT without calling external providers.</p></div><div><Volume2 size={20} /><strong>Outbound speech test</strong><p>Generate placeholder TTS chunk refs and inspect latency budgets.</p></div><Button><Zap size={15} />Simulate stream</Button></div></VoicePanel>
        <EmptyState title="No raw recordings stored" description="Task 013 stores metadata only by default. Raw audio storage must be explicitly enabled by policy later." action={<Button variant="outline" size="sm"><ShieldCheck size={15} />Review policy</Button>} />
        <div className="voice-card"><Skeleton className="voice-skeleton" /><Skeleton className="voice-skeleton-line" /><Skeleton className="voice-skeleton-line" /></div>
        <ErrorState title="Provider failover placeholder" description="Provider errors should trigger configured fallback chains while preserving conversation state." onRetry={() => undefined} />
      </section>
    </div>
  );
}

function VoicePanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="voice-card"><div className="voice-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}