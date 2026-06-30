"use client";

import { ArrowRight, CheckCircle2, Filter, PlugZap, Plus, RefreshCw, Search, Settings, ShieldCheck, SlidersHorizontal } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, SearchInput, Skeleton } from "@voicesense/ui";
import { activityFeed, availableIntegrations, categories, connectorMethods, installedConnections, integrationStats } from "../../../lib/integration-data";

export default function IntegrationsPage() {
  return (
    <div className="integrations-page">
      <header className="integrations-hero">
        <div><p className="ws-kicker">Enterprise connector marketplace</p><h1>Install, test, version, sync, and monitor enterprise connectors through one marketplace and SDK standard.</h1><p>Manage connector publishing, one-click installation, authentication, permissions, sync jobs, playground runs, dependency maps, and health analytics.</p></div>
        <div className="integrations-actions"><Button><Plus size={16} />Install connector</Button><Button variant="outline"><Settings size={16} />SDK settings</Button></div>
      </header>

      <section className="integrations-stat-grid" aria-label="Integration summary">{integrationStats.map((stat) => <article className={`integrations-card integrations-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="integrations-toolbar"><div className="integrations-filter-row">{categories.map((category) => <button className={category === "All" ? "is-active" : ""} type="button" key={category}>{category}</button>)}</div><div className="integrations-search"><SearchInput placeholder="Search integrations" /><Button variant="outline" size="sm"><Filter size={15} />Filter</Button></div></section>

      <section className="integrations-main-grid">
        <div className="integrations-left-stack">
          <IntegrationPanel title="Installed connections" action={<Button variant="outline" size="sm"><RefreshCw size={15} />Test all</Button>}>
            <div className="integrations-connection-list">{installedConnections.map((connection) => <div className="integrations-connection" key={connection.name}><div><strong>{connection.name}</strong><p>{connection.provider} - {connection.auth}</p></div><Badge variant={connection.status === "Healthy" ? "success" : connection.status === "Degraded" ? "warning" : "danger"}>{connection.status}</Badge><span>{connection.health}</span><small>{connection.lastChecked}</small></div>)}</div>
          </IntegrationPanel>

          <IntegrationPanel title="Marketplace foundation" action={<Button variant="outline" size="sm"><Search size={15} />Browse all</Button>}>
            <div className="integrations-market-grid">{availableIntegrations.map((item) => <article className="integrations-market-card" key={item.name}><div><span className="integrations-market-icon"><item.icon size={19} /></span><Badge>{item.category}</Badge></div><strong>{item.name}</strong><p>{item.auth}</p><div className="integrations-chip-row">{item.capabilities.map((capability) => <span key={capability}>{capability}</span>)}</div><Button variant="outline" size="sm">Install<ArrowRight size={14} /></Button></article>)}</div>
          </IntegrationPanel>
        </div>

        <aside className="integrations-side-stack">
          <IntegrationPanel title="Smart installation wizard"><div className="integrations-wizard"><div className="is-active"><span>1</span><strong>Select provider</strong></div><div><span>2</span><strong>Choose auth</strong></div><div><span>3</span><strong>Configure scopes</strong></div><div><span>4</span><strong>Test and enable</strong></div></div></IntegrationPanel>
          <IntegrationPanel title="Universal connector standard"><div className="integrations-method-list">{connectorMethods.map((method) => <div key={method}><CheckCircle2 size={15} /><span>{method}</span></div>)}</div></IntegrationPanel>
          <IntegrationPanel title="Security model"><div className="integrations-security"><ShieldCheck size={22} /><strong>Secret-manager ready</strong><p>Connections store credential fingerprints and secret references only. Raw secrets are never returned by APIs.</p></div></IntegrationPanel>
          <IntegrationPanel title="Activity feed"><div className="integrations-activity-list">{activityFeed.map((event) => <div className="integrations-activity" key={event.title}><span>{event.time}</span><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></IntegrationPanel>
        </aside>
      </section>

      <section className="integrations-state-grid"><EmptyState title="Production provider credentials deferred" description="Task 023 expands the marketplace and connector lifecycle foundation. Paid marketplace flows, revenue sharing, and production credentials remain out of scope." action={<Button variant="outline" size="sm"><PlugZap size={15} />Create connector</Button>} /><div className="integrations-card"><Skeleton className="integrations-skeleton" /><Skeleton className="integrations-skeleton-line" /><Skeleton className="integrations-skeleton-line" /></div><ErrorState title="Connector health unavailable" description="Health checks should fail clearly while the marketplace and installed connection views remain usable." onRetry={() => undefined} /></section>
    </div>
  );
}

function IntegrationPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="integrations-card"><div className="integrations-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}