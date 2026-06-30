"use client";

import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import { ArrowUpRight, Bot, FileSearch, MoreHorizontal, Play, Plus, ShieldCheck, SlidersHorizontal, Timer, MessageSquareText, BadgeCheck } from "lucide-react";
import { Badge, Button, EmptyState, IconButton, SearchInput } from "@voicesense/ui";
import { builderSteps, channelCoverage, readinessChecks, runtimeEvents, testConversation } from "../../../lib/employee-data";
import { API_BASE_URL, bootstrapDemoWorkspace, getAccessToken, getActiveWorkspaceId, listAgents, type AgentOut } from "../../../lib/api-client";

type LiveSummary = {
  sequence: number;
  total_agents: number;
  live_agents: number;
  testing_agents: number;
};

type EmployeeView = {
  id: string;
  name: string;
  role: string;
  status: "Live" | "Testing" | "Draft";
  model: string;
  channel: string;
  owner: string;
  conversations: string;
  resolution: string;
  latency: string;
  guardrail: string;
  tags: string[];
};

const fallbackMetrics = [
  { conversations: "642", resolution: "91%", latency: "1.1s", model: "GPT-4.1", channel: "Voice, chat, email", guardrail: "Strict refunds" },
  { conversations: "188", resolution: "78%", latency: "940ms", model: "GPT-4.1 mini", channel: "Phone, SMS", guardrail: "Human approval" },
  { conversations: "0", resolution: "-", latency: "-", model: "Claude Sonnet", channel: "Slack, web", guardrail: "Read-only tools" },
];

export default function EmployeesPage() {
  const [agents, setAgents] = useState<AgentOut[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [summary, setSummary] = useState<LiveSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [streamState, setStreamState] = useState<"idle" | "connected" | "error">("idle");

  const loadEmployees = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const token = getAccessToken();
      if (!token) {
        setAgents([]);
        setError("Sign in to load AI employees from the VoiceSense API.");
        return;
      }
      let workspaceId = getActiveWorkspaceId();
      if (!workspaceId) {
        const demo = await bootstrapDemoWorkspace();
        workspaceId = demo.workspace.id;
      }
      const nextAgents = await listAgents(workspaceId);
      setAgents(nextAgents);
      setSelectedId((current) => current ?? nextAgents[0]?.id ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load AI employees.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadEmployees();
  }, [loadEmployees]);

  useEffect(() => {
    const token = getAccessToken();
    const workspaceId = getActiveWorkspaceId();
    if (!token || !workspaceId) return;

    const streamUrl = `${API_BASE_URL}/live/workspace-stream?access_token=${encodeURIComponent(token)}&workspace_id=${encodeURIComponent(workspaceId)}`;
    const source = new EventSource(streamUrl);
    source.onopen = () => setStreamState("connected");
    source.onerror = () => setStreamState("error");
    source.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data) as LiveSummary & { type?: string };
        if (payload.type === "workspace.summary") setSummary(payload);
      } catch {
        setStreamState("error");
      }
    };
    return () => source.close();
  }, [agents.length]);

  const employees = useMemo(() => agents.map(toEmployeeView), [agents]);
  const selectedEmployee = employees.find((employee) => employee.id === selectedId) ?? employees[0];
  const stats = useMemo(() => buildStats(employees, summary), [employees, summary]);

  return (
    <div className="employees-page">
      <header className="employees-hero">
        <div>
          <p className="ws-kicker">AI employees</p>
          <h1>Create, configure, test, and supervise every AI employee before it reaches a customer.</h1>
          <p>Design the role, bind knowledge and tools, run simulations, review guardrails, and promote employees through draft, testing, and live states.</p>
          <div className={`employees-live-pill ${streamState}`} aria-live="polite">
            <span />{streamState === "connected" ? "Live API connected" : streamState === "error" ? "Realtime stream reconnecting" : "Waiting for realtime stream"}
          </div>
        </div>
        <div className="employees-actions">
          <Button><Plus size={16} />Create employee</Button>
          <Button variant="outline"><Play size={16} />Run simulation</Button>
        </div>
      </header>

      <section className="employees-stat-grid" aria-label="AI employee summary">
        {stats.map((stat) => (
          <article className={`employees-card employees-stat ${stat.tone}`} key={stat.label}>
            <stat.icon size={18} />
            <p>{stat.label}</p>
            <strong>{loading ? "..." : stat.value}</strong>
            <span>{stat.detail}</span>
          </article>
        ))}
      </section>

      <section className="employees-toolbar" aria-label="Employee controls">
        <SearchInput placeholder="Search employees, roles, models, tools" />
        <div>
          <Button variant="outline" size="sm"><SlidersHorizontal size={15} />Filter</Button>
          <Button variant="outline" size="sm"><ShieldCheck size={15} />Readiness checks</Button>
        </div>
      </section>

      {error ? <EmployeePanel title="Live data status" action={<Button variant="outline" size="sm" onClick={() => void loadEmployees()}>Retry</Button>}><p className="employees-error">{error}</p></EmployeePanel> : null}

      <section className="employees-main-grid">
        <div className="employees-left-stack">
          <EmployeePanel title="Employee roster" action={<Button variant="outline" size="sm">View deployments</Button>}>
            <div className="employees-roster">
              {loading ? <EmployeeRosterSkeleton /> : null}
              {!loading && employees.length === 0 ? (
                <EmptyState title="No AI employees yet" description="Create or bootstrap employees before testing calls, chat, and workflow automations." action={<Button size="sm" onClick={() => void loadEmployees()}><Plus size={15} />Load demo employees</Button>} />
              ) : null}
              {!loading && employees.map((employee) => (
                <article className={`employees-row employees-row-button ${selectedEmployee?.id === employee.id ? "selected" : ""}`} key={employee.id} onClick={() => setSelectedId(employee.id)} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") setSelectedId(employee.id); }} role="button" tabIndex={0}>
                  <div className="employees-avatar">{employee.name.slice(0, 2).toUpperCase()}</div>
                  <div className="employees-row-main">
                    <div>
                      <strong>{employee.name}</strong>
                      <Badge variant={employee.status === "Live" ? "success" : employee.status === "Testing" ? "warning" : "info"}>{employee.status}</Badge>
                    </div>
                    <p>{employee.role} - {employee.channel}</p>
                    <div className="employees-tags">{employee.tags.map((tag) => <Badge key={tag}>{tag}</Badge>)}</div>
                  </div>
                  <dl className="employees-row-metrics">
                    <div><dt>Model</dt><dd>{employee.model}</dd></div>
                    <div><dt>Resolved</dt><dd>{employee.resolution}</dd></div>
                    <div><dt>Latency</dt><dd>{employee.latency}</dd></div>
                  </dl>
                  <IconButton variant="ghost" aria-label={`More actions for ${employee.name}`}><MoreHorizontal size={17} /></IconButton>
                </article>
              ))}
            </div>
          </EmployeePanel>

          <EmployeePanel title="Builder checklist" action={<Button size="sm"><ArrowUpRight size={15} />Open builder</Button>}>
            <div className="employees-step-list">
              {builderSteps.map((step) => (
                <div className={`employees-step ${step.status === "Complete" ? "complete" : ""}`} key={step.label}>
                  <step.icon size={17} />
                  <strong>{step.label}</strong>
                  <Badge variant={step.status === "Complete" ? "success" : step.status === "Needs review" ? "warning" : "info"}>{step.status}</Badge>
                </div>
              ))}
            </div>
          </EmployeePanel>
        </div>

        <aside className="employees-side-stack">
          <EmployeePanel title="Selected employee">
            {selectedEmployee ? (
              <>
                <div className="employees-profile">
                  <div className="employees-avatar large">{selectedEmployee.name.slice(0, 2).toUpperCase()}</div>
                  <strong>{selectedEmployee.name}</strong>
                  <p>{selectedEmployee.role} owned by {selectedEmployee.owner}.</p>
                </div>
                <dl className="employees-profile-meta">
                  <div><dt>Guardrail</dt><dd>{selectedEmployee.guardrail}</dd></div>
                  <div><dt>Knowledge</dt><dd>Billing policy, Help Center, CRM notes</dd></div>
                  <div><dt>Handoff</dt><dd>Escalate after policy-sensitive actions</dd></div>
                </dl>
              </>
            ) : <EmptyState title="No employee selected" description="Load live employees to inspect readiness, guardrails, and deployment posture." />}
          </EmployeePanel>

          <EmployeePanel title="Readiness">
            <div className="employees-readiness">
              {readinessChecks.map((check) => (
                <div className="employees-check" key={check.label}>
                  <check.icon size={16} />
                  <span>{check.label}</span>
                  <Badge variant={check.tone === "success" ? "success" : "warning"}>{check.value}</Badge>
                </div>
              ))}
            </div>
          </EmployeePanel>
        </aside>
      </section>

      <section className="employees-main-grid">
        <EmployeePanel title="Conversation simulation" action={<Button size="sm"><Play size={15} />Replay</Button>}>
          <div className="employees-turn-list">
            {testConversation.map((turn) => <div className={`employees-turn ${turn.tone}`} key={`${turn.speaker}-${turn.body}`}><span>{turn.speaker}</span><p>{turn.body}</p></div>)}
          </div>
        </EmployeePanel>

        <EmployeePanel title="Runtime events">
          <div className="employees-event-list">
            {runtimeEvents.map((event) => (
              <div className="employees-event" key={event.title}>
                <span>{event.time}</span>
                <event.icon size={17} />
                <div><strong>{event.title}</strong><p>{event.detail}</p></div>
              </div>
            ))}
          </div>
        </EmployeePanel>
      </section>

      <section className="employees-channel-grid" aria-label="Channel coverage">
        {channelCoverage.map((channel) => (
          <article className={`employees-card employees-channel ${channel.tone}`} key={channel.label}>
            <channel.icon size={20} />
            <strong>{channel.label}</strong>
            <p>{channel.value}</p>
          </article>
        ))}
        <EmptyState title="No evaluation suite yet" description="Add scored test cases before promoting high-risk employees to live channels." action={<Button variant="outline" size="sm"><FileSearch size={15} />Create suite</Button>} />
      </section>
    </div>
  );
}

function toEmployeeView(agent: AgentOut, index: number): EmployeeView {
  const metrics = fallbackMetrics[index % fallbackMetrics.length];
  return {
    id: agent.id,
    name: agent.display_name ?? agent.name,
    role: agent.role ?? "AI Employee",
    status: agent.status === "published" ? "Live" : agent.status === "testing" ? "Testing" : "Draft",
    model: metrics.model,
    channel: metrics.channel,
    owner: agent.department ? `${agent.department} Team` : "Workspace Team",
    conversations: metrics.conversations,
    resolution: metrics.resolution,
    latency: metrics.latency,
    guardrail: metrics.guardrail,
    tags: [agent.category ?? "General", agent.lifecycle_stage, agent.status].map(capitalize),
  };
}

function buildStats(employees: EmployeeView[], summary: LiveSummary | null) {
  const live = summary?.live_agents ?? employees.filter((employee) => employee.status === "Live").length;
  const testing = summary?.testing_agents ?? employees.filter((employee) => employee.status === "Testing").length;
  const total = summary?.total_agents ?? employees.length;
  return [
    { label: "Live employees", value: String(live), detail: `${testing} in testing`, icon: Bot, tone: "green" },
    { label: "Conversations today", value: total ? "1,284" : "0", detail: total ? "31 active now" : "No live traffic yet", icon: MessageSquareText, tone: "blue" },
    { label: "Avg response latency", value: total ? "1.2s" : "-", detail: "Voice + chat", icon: Timer, tone: "amber" },
    { label: "Resolved without handoff", value: total ? "86%" : "-", detail: total ? "+7% this week" : "Awaiting conversations", icon: BadgeCheck, tone: "purple" },
  ];
}

function capitalize(value: string) {
  return value.slice(0, 1).toUpperCase() + value.slice(1).replaceAll("_", " ");
}

function EmployeeRosterSkeleton() {
  return Array.from({ length: 3 }).map((_, index) => (
    <div className="employees-row employees-skeleton-row" key={index} aria-hidden="true">
      <div className="employees-avatar employees-skeleton" />
      <div className="employees-row-main">
        <div className="employees-skeleton line short" />
        <div className="employees-skeleton line" />
        <div className="employees-skeleton line tags" />
      </div>
      <div className="employees-skeleton metrics" />
    </div>
  ));
}

function EmployeePanel({ title, action, children }: { title: string; action?: ReactNode; children: ReactNode }) {
  return <article className="employees-card"><div className="employees-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}
