"use client";

import { AlertTriangle, Braces, CheckCircle2, Copy, KeyRound, LockKeyhole, Play, Plus, RefreshCw, Search, Server, Settings, ShieldCheck, Terminal, Wrench, Zap } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { categories, executions, mcpServers, permissionRules, runtimeStages, toolLogs, toolStats, tools } from "../../../lib/tool-data";

export default function ToolsPage() {
  return (
    <div className="tool-page">
      <header className="tool-hero">
        <div><p className="ws-kicker">Universal tool runtime</p><h1>Discover, validate, execute, and monitor every tool AI employees are allowed to use.</h1><p>The Tool Platform standardizes tool registration, permissions, schemas, runtime execution, observability, chaining, and future MCP compatibility without calling real external providers yet.</p></div>
        <div className="tool-actions"><Button><Plus size={16} />Register tool</Button><Button variant="outline"><Play size={16} />Run test</Button><Button variant="outline"><Server size={16} />MCP server</Button></div>
      </header>

      <section className="tool-stat-grid">{toolStats.map((stat) => <article className={`tool-card tool-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="tool-toolbar"><div className="tool-category-row"><button className="is-active" type="button">All</button><button type="button">AI</button><button type="button">Automation</button><button type="button">Developer</button><button type="button">Custom</button></div><div className="tool-search"><SearchInput placeholder="Search tools, executions, MCP servers" /><Button variant="outline" size="sm"><Search size={15} />Search</Button></div></section>

      <section className="tool-main-grid">
        <div className="tool-left-stack">
          <ToolPanel title="Tool registry" action={<Button variant="outline" size="sm"><RefreshCw size={15} />Refresh</Button>}>
            <div className="tool-table"><div className="tool-row tool-head"><span>Tool</span><span>Category</span><span>Status</span><span>Runtime</span><span>Auth</span><span>Health</span></div>{tools.map((tool) => <div className="tool-row" key={tool.name}><span><Wrench size={16} />{tool.name}</span><span>{tool.category}</span><span><Badge variant={tool.status === "Enabled" ? "success" : "warning"}>{tool.status}</Badge></span><span>{tool.runtime}</span><span>{tool.auth}</span><span><Progress value={tool.health} /></span></div>)}</div>
          </ToolPanel>

          <ToolPanel title="Runtime pipeline" action={<Badge>Guarded execution</Badge>}>
            <div className="tool-runtime-grid">{runtimeStages.map((stage, index) => <div key={stage.label}><span>{index + 1}</span><stage.icon size={17} /><strong>{stage.label}</strong><p>{stage.detail}</p></div>)}</div>
          </ToolPanel>

          <ToolPanel title="Tool playground" action={<Button variant="outline" size="sm"><Braces size={15} />Validate</Button>}>
            <div className="tool-playground"><div className="tool-code-box"><Terminal size={18} /><pre>{`{"query":"refund policy","limit":3}`}</pre></div><div className="tool-play-actions"><Button size="sm"><Play size={15} />Execute simulated</Button><Button variant="outline" size="sm"><Copy size={15} />Copy payload</Button></div></div>
          </ToolPanel>
        </div>

        <aside className="tool-side-stack">
          <ToolPanel title="Execution history"><div className="tool-execution-list">{executions.map((run) => <div key={run.id}><span><strong>{run.id}</strong><small>{run.tool} - {run.source}</small></span><Badge variant={run.status === "Completed" ? "success" : "warning"}>{run.status}</Badge><p>{run.latency} - retries {run.retries}</p></div>)}</div></ToolPanel>
          <ToolPanel title="Permission manager"><div className="tool-permission-list">{permissionRules.map((rule) => <div key={`${rule.principal}-${rule.action}`}><ShieldCheck size={16} /><span><strong>{rule.principal}</strong><small>{rule.action} - {rule.condition}</small></span><Badge variant={rule.effect === "allow" ? "success" : "danger"}>{rule.effect}</Badge></div>)}</div></ToolPanel>
          <ToolPanel title="MCP readiness"><div className="tool-mcp-list">{mcpServers.map((server) => <div key={server.name}><Server size={16} /><span><strong>{server.name}</strong><small>{server.transport} - {server.resources}</small></span><Badge>{server.status}</Badge></div>)}</div></ToolPanel>
        </aside>
      </section>

      <section className="tool-bottom-grid">
        <ToolPanel title="Tool categories"><div className="tool-category-grid">{categories.map((category) => <article key={category.label}><category.icon size={17} /><strong>{category.label}</strong><p>{category.detail}</p></article>)}</div></ToolPanel>
        <ToolPanel title="Runtime logs"><div className="tool-log-list">{toolLogs.map((event) => <div className="tool-log" key={`${event.time}-${event.title}`}><span>{event.time}</span><event.icon size={16} /><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></ToolPanel>
        <div className="tool-card"><Skeleton className="tool-skeleton" /><Skeleton className="tool-skeleton-line" /><Skeleton className="tool-skeleton-line" /></div>
      </section>

      <section className="tool-state-grid"><EmptyState title="External MCP communication deferred" description="MCP server registration, discovery metadata, resources, prompts, sessions, and transports are modeled. Network communication comes later." action={<Button variant="outline" size="sm"><Server size={15} />Review MCP</Button>} /><ErrorState title="Unsafe tool call rejected" description="The runtime rejects invalid parameters, disabled tools, and denied permissions before execution." onRetry={() => undefined} /></section>
    </div>
  );
}

function ToolPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="tool-card"><div className="tool-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}
