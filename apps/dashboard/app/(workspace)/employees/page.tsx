"use client";

import { ArrowUpRight, Bot, FileSearch, MoreHorizontal, Play, Plus, ShieldCheck, SlidersHorizontal } from "lucide-react";
import { Badge, Button, EmptyState, IconButton, SearchInput } from "@voicesense/ui";
import { builderSteps, channelCoverage, employees, employeeStats, readinessChecks, runtimeEvents, testConversation } from "../../../lib/employee-data";

export default function EmployeesPage() {
  return (
    <div className="employees-page">
      <header className="employees-hero">
        <div>
          <p className="ws-kicker">AI employees</p>
          <h1>Create, configure, test, and supervise every AI employee before it reaches a customer.</h1>
          <p>Design the role, bind knowledge and tools, run simulations, review guardrails, and promote employees through draft, testing, and live states.</p>
        </div>
        <div className="employees-actions">
          <Button><Plus size={16} />Create employee</Button>
          <Button variant="outline"><Play size={16} />Run simulation</Button>
        </div>
      </header>

      <section className="employees-stat-grid" aria-label="AI employee summary">
        {employeeStats.map((stat) => (
          <article className={`employees-card employees-stat ${stat.tone}`} key={stat.label}>
            <stat.icon size={18} />
            <p>{stat.label}</p>
            <strong>{stat.value}</strong>
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

      <section className="employees-main-grid">
        <div className="employees-left-stack">
          <EmployeePanel title="Employee roster" action={<Button variant="outline" size="sm">View deployments</Button>}>
            <div className="employees-roster">
              {employees.map((employee) => (
                <article className="employees-row" key={employee.name}>
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
            <div className="employees-profile">
              <div className="employees-avatar large">MA</div>
              <strong>Maya</strong>
              <p>Customer Success Agent owned by CX Team.</p>
            </div>
            <dl className="employees-profile-meta">
              <div><dt>Guardrail</dt><dd>Strict refunds</dd></div>
              <div><dt>Knowledge</dt><dd>Billing policy, Help Center, CRM notes</dd></div>
              <div><dt>Handoff</dt><dd>Escalate after refund preview</dd></div>
            </dl>
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

function EmployeePanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="employees-card"><div className="employees-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}
