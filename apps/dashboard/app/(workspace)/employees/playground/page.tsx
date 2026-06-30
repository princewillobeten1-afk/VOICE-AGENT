"use client";

import { BrainCircuit, Copy, Eye, Play, RotateCcw, Send, ShieldCheck } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, SearchInput, Skeleton } from "@voicesense/ui";
import { playgroundMetrics, playgroundTurns } from "../../../../lib/employee-builder-data";

export default function EmployeePlaygroundPage() {
  return (
    <div className="builder-page">
      <header className="builder-hero"><div><p className="ws-kicker">AI playground</p><h1>Safely test AI employee behavior before publishing to real channels.</h1><p>Inspect prompts, context, memory previews, placeholder tool logs, response timing, token usage, and conversation history without calling real AI providers.</p></div><div className="builder-actions"><Button><Play size={16} />Run test</Button><Button variant="outline"><RotateCcw size={16} />Reset</Button></div></header>

      <section className="playground-grid">
        <main className="builder-card playground-chat"><div className="builder-panel-head"><h2>Chat testing</h2><Badge>Simulation mode</Badge></div><div className="employees-turn-list">{playgroundTurns.map((turn) => <div className={`employees-turn ${turn.tone}`} key={`${turn.speaker}-${turn.body}`}><span>{turn.speaker}</span><p>{turn.body}</p></div>)}</div><div className="playground-input"><SearchInput placeholder="Ask Maya a test question" /><Button><Send size={15} />Send</Button></div></main>

        <aside className="playground-side"><article className="builder-card"><div className="builder-panel-head"><h2>Run metrics</h2><BrainCircuit size={18} /></div><div className="playground-metrics">{playgroundMetrics.map((metric) => <div key={metric.label}><metric.icon size={16} /><span>{metric.label}</span><strong>{metric.value}</strong></div>)}</div></article><article className="builder-card"><div className="builder-panel-head"><h2>Prompt inspection</h2><Button variant="outline" size="sm"><Copy size={15} />Copy</Button></div><pre>{`System: You are Maya, a calm Customer Success AI Employee.\nPolicy: Request approval before refunds.\nContext: Billing policy v3, CRM account note.`}</pre></article><article className="builder-card"><div className="builder-panel-head"><h2>Safety</h2><ShieldCheck size={18} /></div><div className="builder-policy-list"><div><strong>Tool execution</strong><p>Placeholder only. No real tools execute in Task 012.</p></div><div><strong>Memory</strong><p>Preview only. No memory storage is active.</p></div></div></article></aside>
      </section>

      <section className="builder-template-strip"><EmptyState title="No saved test suite yet" description="Create scored test cases when evaluation infrastructure is added." action={<Button variant="outline" size="sm"><Eye size={15} />Create suite</Button>} /><div className="builder-card"><Skeleton className="builder-skeleton" /><Skeleton className="builder-skeleton-line" /></div><ErrorState title="Provider disabled" description="Real model providers are intentionally disabled in the builder playground foundation." onRetry={() => undefined} /></section>
    </div>
  );
}