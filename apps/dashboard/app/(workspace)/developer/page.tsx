"use client";

import { AlertCircle, Copy, Play, Plus, RefreshCcw, Search, Terminal } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, SearchInput, Skeleton } from "@voicesense/ui";
import { apiKeys, apiLogs, developerNav, docsSections, oauthApps, playgroundEndpoints, rateLimits, sdks, usageMetrics, webhooks } from "../../../lib/developer-data";

export default function DeveloperPage() {
  return (
    <div className="dev-page">
      <header className="dev-hero">
        <div>
          <p className="ws-kicker">Developer platform</p>
          <h1>Build, test, automate, and scale on VoiceSense with premium APIs, SDKs, CLI, webhooks, OAuth, sandbox, and analytics.</h1>
          <p>Explore endpoints, execute sandbox requests, generate code samples, manage credentials, inspect request timelines, and monitor API health from one developer-grade workspace.</p>
        </div>
        <div className="dev-hero-actions"><Button><Plus size={16} />Create API key</Button><Button variant="outline"><Terminal size={16} />Open API explorer</Button></div>
      </header>

      <nav className="dev-nav" aria-label="Developer navigation">{developerNav.map((item) => <a href={`#${item.label.toLowerCase().replaceAll(" ", "-")}`} key={item.label}><item.icon size={16} />{item.label}</a>)}</nav>

      <section id="overview" className="dev-grid four">{usageMetrics.map((metric) => <article className="dev-card dev-metric" key={metric.label}><metric.icon size={18} /><p>{metric.label}</p><strong>{metric.value}</strong><span>{metric.detail}</span></article>)}</section>

      <section className="dev-grid two">
        <DeveloperPanel id="api-keys" title="API keys" action={<Button size="sm"><Plus size={15} />New key</Button>}>
          <div className="dev-table-list">{apiKeys.map((key) => <div className="dev-row" key={key.name}><div><strong>{key.name}</strong><p>{key.prefix} Â· {key.environment}</p><div className="dev-tags">{key.scopes.map((scope) => <Badge key={scope}>{scope}</Badge>)}</div></div><div><span>{key.requests}</span><small>Last used {key.lastUsed}</small></div></div>)}</div>
          <SecretNotice />
        </DeveloperPanel>

        <DeveloperPanel id="webhooks" title="Webhooks" action={<Button size="sm" variant="outline">Test webhook</Button>}>
          <div className="dev-table-list">{webhooks.map((hook) => <div className="dev-row" key={hook.url}><div><strong>{hook.url}</strong><p>{hook.events.join(", ")}</p></div><div><Badge variant={hook.status === "Active" ? "success" : "warning"}>{hook.status}</Badge><small>{hook.deliveries} delivery</small></div></div>)}</div>
        </DeveloperPanel>
      </section>

      <section id="api-playground" className="dev-playground">
        <DeveloperPanel title="Interactive API explorer" action={<Button size="sm"><Play size={15} />Send request</Button>}>
          <div className="dev-playground-grid"><div className="dev-request-builder"><label>Endpoint</label><select defaultValue="/v1/users/me"><option>/v1/users/me</option><option>/v1/developer/api-keys</option><option>/v1/conversations</option></select><label>Headers</label><pre>{`Authorization: Bearer vsk_...
Content-Type: application/json`}</pre><label>JSON body</label><pre>{`{
  "name": "Production key",
  "scopes": ["read", "write"]
}`}</pre><div className="dev-copy-row"><Button variant="outline" size="sm"><Copy size={15} />Copy request</Button></div></div><div className="dev-response-viewer"><div><Badge variant="success">200 OK</Badge><span>124 ms</span></div><pre>{`{
  "ok": true,
  "data": {
    "id": "usr_...",
    "email": "ada@example.com"
  }
}`}</pre><Button variant="outline" size="sm"><Copy size={15} />Copy response</Button></div></div>
        </DeveloperPanel>
      </section>

      <section className="dev-grid two">
        <DeveloperPanel id="documentation" title="Documentation portal"><div className="dev-doc-grid">{docsSections.map((section) => <a href="#" key={section}>{section}</a>)}</div></DeveloperPanel>
        <DeveloperPanel id="sdks" title="SDK generator framework"><div className="dev-sdk-grid">{sdks.map((sdk) => <div className="dev-sdk" key={sdk.language}><sdk.icon size={18} /><div><strong>{sdk.language}</strong><p>{sdk.package}</p></div><Badge>{sdk.status}</Badge></div>)}</div></DeveloperPanel>
      </section>

      <section className="dev-grid two">
        <DeveloperPanel id="oauth-apps" title="OAuth apps"><div className="dev-table-list">{oauthApps.map((app) => <div className="dev-row" key={app.name}><div><strong>{app.name}</strong><p>{app.clientId} Â· {app.environment}</p></div><Badge>{app.status}</Badge></div>)}</div><EmptyState title="OAuth application framework ready" description="Application registration, redirect URIs, scopes, token refresh, and revocation are modeled for secure third-party apps." /></DeveloperPanel>
        <DeveloperPanel id="api-logs" title="API logs" action={<SearchInput placeholder="Search logs" />}><div className="dev-log-list">{apiLogs.map((log) => <div className="dev-log-row" key={log.requestId}><span>{log.time}</span><Badge variant={log.status < 300 ? "success" : "danger"}>{log.status}</Badge><strong>{log.method}</strong><p>{log.endpoint}</p><small>{log.latency} Â· {log.requestId}</small></div>)}</div></DeveloperPanel>
      </section>

      <section className="dev-grid two">
        <DeveloperPanel id="usage-analytics" title="Developer health dashboard"><div className="dev-bars">{[42, 58, 49, 72, 66, 88, 53].map((height, index) => <div key={index}><span style={{ height: `${height}%` }} /></div>)}</div></DeveloperPanel>
        <DeveloperPanel id="rate-limits" title="Rate limits"><div className="dev-table-list">{rateLimits.map((limit) => <div className="dev-row" key={limit.label}><div><strong>{limit.label}</strong><p>{limit.limit}</p></div><span>{limit.used} used</span></div>)}</div></DeveloperPanel>
      </section>

      <section className="dev-grid three" id="settings"><ErrorState title="Sandbox environment preview" description="Test organizations, fake phone numbers, mock conversations, sample events, and fixture resources are architecture-ready." onRetry={() => undefined} /><div className="dev-card"><Skeleton className="dev-skeleton" /><Skeleton className="dev-skeleton-line" /><Skeleton className="dev-skeleton-line" /></div><div className="dev-card dev-security"><AlertCircle size={22} /><strong>Security model</strong><p>Secrets are generated once, hashed before storage, scoped by permission, and audited on mutation.</p></div></section>
    </div>
  );
}

function DeveloperPanel({ id, title, action, children }: { id?: string; title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article id={id} className="dev-card"><div className="dev-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}

function SecretNotice() {
  return <div className="dev-secret-notice"><strong>Secret keys are shown once.</strong><p>VoiceSense stores only hashed credentials. Regeneration creates a new secret and invalidates the old one.</p></div>;
}