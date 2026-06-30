"use client";

import { ArrowRight, CheckCircle2, ClipboardCheck, Eye, FileText, Play, Rocket, Save, ShieldCheck, Sparkles } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, Skeleton } from "@voicesense/ui";
import { builderChannels, builderKnowledgeSources, builderTools, builderWizardSteps, employeeTemplates, personalityControls, voiceSettings } from "../../../../lib/employee-builder-data";

export default function BuilderPage() {
  return (
    <div className="builder-page">
      <header className="builder-hero"><div><p className="ws-kicker">AI employee builder</p><h1>Hire, train, test, and publish an AI employee through one guided workspace.</h1><p>The builder keeps identity, instructions, voice, knowledge, tools, memory, channels, review, and publishing connected to the Task 011 AI architecture.</p></div><div className="builder-actions"><Button><Save size={16} />Save draft</Button><Button variant="outline"><Play size={16} />Test</Button><Button variant="outline"><Rocket size={16} />Publish</Button></div></header>

      <section className="builder-layout">
        <aside className="builder-steps" aria-label="Builder steps">{builderWizardSteps.map((item) => <button className={item.step === 3 ? "is-active" : item.status === "Complete" ? "is-complete" : ""} type="button" key={item.label}><span>{item.step}</span><item.icon size={17} /><strong>{item.label}</strong><Badge variant={item.status === "Complete" ? "success" : item.status === "Needs source" ? "warning" : "info"}>{item.status}</Badge></button>)}</aside>

        <main className="builder-workbench">
          <section className="builder-card builder-identity"><div className="builder-avatar">MA</div><div><p className="ws-kicker">Identity</p><h2>Maya, Customer Success Agent</h2><p>Owned by CX Team. Responsible for billing questions, retention conversations, refund preparation, and policy-safe handoff.</p></div><Badge variant="warning">Draft v4</Badge></section>

          <section className="builder-grid two"><BuilderPanel title="Personality controls" action={<Sparkles size={18} />}><div className="builder-slider-list">{personalityControls.map((control) => <label key={control.label}><span>{control.label}</span><input type="range" min="0" max="100" defaultValue={control.value} /><strong>{control.value}%</strong></label>)}</div></BuilderPanel><BuilderPanel title="Voice configuration" action={<Badge>Placeholder providers</Badge>}><div className="builder-meta-grid">{voiceSettings.map((item) => <div key={item.label}><span>{item.label}</span><strong>{item.value}</strong></div>)}</div></BuilderPanel></section>

          <BuilderPanel title="Instruction editor" action={<Button variant="outline" size="sm"><Eye size={15} />Preview</Button>}><div className="builder-editor"><div><Badge>System prompt</Badge><Badge>Versioned</Badge><Badge>Variables</Badge></div><textarea defaultValue={`You are Maya, a calm Customer Success AI Employee for {{organization_name}}. Resolve billing questions clearly, use approved policy language, and request human approval before refunds or cancellation offers.`} /><div className="builder-validation"><CheckCircle2 size={16} /><span>Prompt variables are valid. Refund action requires approval. No hardcoded provider behavior detected.</span></div></div></BuilderPanel>

          <section className="builder-grid three"><BuilderPanel title="Knowledge"><div className="builder-chip-list">{builderKnowledgeSources.map((item) => <span key={item}>{item}</span>)}</div></BuilderPanel><BuilderPanel title="Tools"><div className="builder-chip-list">{builderTools.map((item) => <span key={item}>{item}</span>)}</div></BuilderPanel><BuilderPanel title="Channels"><div className="builder-chip-list">{builderChannels.map((item) => <span key={item}>{item}</span>)}</div></BuilderPanel></section>

          <section className="builder-grid two"><BuilderPanel title="Memory policy"><div className="builder-policy-list"><div><strong>Short-term</strong><p>Keep active conversation state until session ends.</p></div><div><strong>Long-term</strong><p>Disabled until retention policy is approved.</p></div><div><strong>Shared memory</strong><p>Prepared for future supervisor and specialist collaboration.</p></div></div></BuilderPanel><BuilderPanel title="Review summary"><div className="builder-review"><ClipboardCheck size={22} /><strong>7 of 10 steps ready</strong><p>Knowledge freshness and final publishing checks still need review before live deployment.</p><Button size="sm"><ArrowRight size={15} />Continue review</Button></div></BuilderPanel></section>
        </main>
      </section>

      <section className="builder-template-strip">{employeeTemplates.map((template) => <article className="builder-card builder-template" key={template.name}><template.icon size={18} /><strong>{template.name}</strong><p>{template.role}</p><span>{template.channels}</span></article>)}<EmptyState title="No custom template selected" description="Save this configuration as a reusable hiring template after review." action={<Button variant="outline" size="sm"><FileText size={15} />Save template</Button>} /><div className="builder-card"><Skeleton className="builder-skeleton" /><Skeleton className="builder-skeleton-line" /></div><ErrorState title="Validation warning" description="Validation states should guide users without blocking unrelated builder sections." onRetry={() => undefined} /></section>
    </div>
  );
}

function BuilderPanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="builder-card"><div className="builder-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}