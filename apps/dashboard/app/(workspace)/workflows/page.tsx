"use client";

import { AlertTriangle, Copy, Filter, History, LayoutGrid, ListFilter, Maximize2, Play, Plus, RefreshCw, Search, Settings, Undo2, Workflow, ZoomIn } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { builderControls, canvasNodes, executions, nodePalette, templates, versionHistory, workflowLogs, workflows, workflowStats } from "../../../lib/workflow-data";

export default function WorkflowsPage() {
  return (
    <div className="workflow-page">
      <header className="workflow-hero">
        <div><p className="ws-kicker">Visual workflow automation</p><h1>Build, execute, and monitor intelligent business automations across AI employees, approvals, APIs, and integrations.</h1><p>The Workflow Engine foundation models visual workflow design, node orchestration, event triggers, variables, versioning, monitoring, and long-running execution without calling real providers yet.</p></div>
        <div className="workflow-actions"><Button><Plus size={16} />New workflow</Button><Button variant="outline"><Play size={16} />Run test</Button><Button variant="outline"><Settings size={16} />Settings</Button></div>
      </header>

      <section className="workflow-stat-grid">{workflowStats.map((stat) => <article className={`workflow-card workflow-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="workflow-toolbar"><div className="workflow-category-row"><button className="is-active" type="button"><LayoutGrid size={14} />Grid</button><button type="button"><ListFilter size={14} />List</button><button type="button"><Filter size={14} />Filters</button><button type="button"><Copy size={14} />Bulk actions</button></div><div className="workflow-search"><SearchInput placeholder="Search workflows, templates, executions" /><Button variant="outline" size="sm"><Search size={15} />Search</Button></div></section>

      <section className="workflow-main-grid">
        <div className="workflow-left-stack">
          <WorkflowPanel title="Workflow dashboard" action={<Button variant="outline" size="sm"><RefreshCw size={15} />Refresh</Button>}>
            <div className="workflow-table"><div className="workflow-row workflow-head"><span>Workflow</span><span>Category</span><span>Status</span><span>Trigger</span><span>Executions</span><span>Success</span></div>{workflows.map((item) => <div className="workflow-row" key={item.name}><span><Workflow size={16} />{item.name}</span><span>{item.category}</span><span><Badge variant={item.status === "Published" ? "success" : item.status === "Paused" ? "warning" : "info"}>{item.status}</Badge></span><span>{item.trigger}</span><span>{item.executions}</span><span><Progress value={item.success} /></span></div>)}</div>
          </WorkflowPanel>

          <WorkflowPanel title="Visual workflow builder" action={<div className="workflow-canvas-actions"><Button variant="outline" size="sm"><Undo2 size={15} />Undo</Button><Button variant="outline" size="sm"><ZoomIn size={15} />82%</Button><Button variant="outline" size="sm"><Maximize2 size={15} />Fit</Button></div>}>
            <div className="workflow-builder">
              <aside className="workflow-palette">{nodePalette.map((node) => <button key={node.label} type="button"><node.icon size={16} /><span><strong>{node.label}</strong><small>{node.group} - {node.detail}</small></span></button>)}</aside>
              <div className="workflow-canvas" aria-label="Workflow canvas preview">{canvasNodes.map((node) => <article className={`workflow-canvas-node ${node.tone}`} key={node.key} style={{ left: `${node.x}%`, top: `${node.y}%` }}><node.icon size={16} /><span><strong>{node.label}</strong><small>{node.type}</small></span></article>)}<div className="workflow-canvas-line one" /><div className="workflow-canvas-line two" /><div className="workflow-canvas-line three" /><div className="workflow-minimap"><span /></div></div>
            </div>
            <div className="workflow-control-row">{builderControls.map((control) => <button type="button" key={control.label}><control.icon size={15} />{control.label}</button>)}</div>
          </WorkflowPanel>
        </div>

        <aside className="workflow-side-stack">
          <WorkflowPanel title="Recent executions"><div className="workflow-execution-list">{executions.map((run) => <div key={run.id}><span><strong>{run.id}</strong><small>{run.workflow}</small></span><Badge variant={run.status === "Completed" ? "success" : run.status === "Failed" ? "danger" : run.status === "Paused" ? "warning" : "info"}>{run.status}</Badge><p>{run.node} - {run.duration} - retries {run.retries}</p></div>)}</div></WorkflowPanel>
          <WorkflowPanel title="Templates"><div className="workflow-template-grid">{templates.map((template) => <article key={template.name}><template.icon size={17} /><strong>{template.name}</strong><p>{template.category} - {template.difficulty}</p><Badge>{template.nodes} nodes</Badge></article>)}</div></WorkflowPanel>
          <WorkflowPanel title="Version history"><div className="workflow-version-list">{versionHistory.map((version) => <div key={version.version}><version.icon size={16} /><span><strong>{version.version} - {version.status}</strong><small>{version.change}</small></span><em>{version.time}</em></div>)}</div></WorkflowPanel>
        </aside>
      </section>

      <section className="workflow-bottom-grid">
        <WorkflowPanel title="Execution logs"><div className="workflow-log-list">{workflowLogs.map((event) => <div className="workflow-log" key={`${event.time}-${event.title}`}><span>{event.time}</span><event.icon size={16} /><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></WorkflowPanel>
        <EmptyState title="No real integrations executed" description="Workflow nodes are registered and execution is durable, but provider calls are intentionally simulated until integration adapters are connected." action={<Button variant="outline" size="sm"><Settings size={15} />Review adapters</Button>} />
        <div className="workflow-card"><Skeleton className="workflow-skeleton" /><Skeleton className="workflow-skeleton-line" /><Skeleton className="workflow-skeleton-line" /></div>
      </section>

      <section className="workflow-state-grid"><ErrorState title="AI reasoning is deferred" description="AI workflow nodes coordinate with the AI architecture, but Task 017 does not execute real LLM reasoning." onRetry={() => undefined} /><EmptyState title="No approval selected" description="Human-in-the-loop approvals are modeled for pause, assign, comment, approve, reject, and resume flows." action={<Button variant="outline" size="sm"><AlertTriangle size={15} />Open queue</Button>} /></section>
    </div>
  );
}

function WorkflowPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="workflow-card"><div className="workflow-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}

