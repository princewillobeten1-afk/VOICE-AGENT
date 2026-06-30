import { AlertCircle, ArrowRight, RefreshCcw } from "lucide-react";
import { Button, Skeleton } from "@voicesense/ui";
import { activity, demoWorkspace, emptyStates, onboardingChecklist, quickActions, stats, systemStatus, usageSeries } from "../../lib/workspace-data";

export function SectionHeader({ eyebrow, title, action }: { eyebrow?: string; title: string; action?: React.ReactNode }) {
  return <div className="ws-section-header"><div>{eyebrow ? <p>{eyebrow}</p> : null}<h2>{title}</h2></div>{action}</div>;
}

export function WidgetContainer({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <article className={`ws-widget ${className}`}>{children}</article>;
}

export function DashboardGrid({ children }: { children: React.ReactNode }) {
  return <section className="ws-dashboard-grid">{children}</section>;
}

export function StatisticCards() {
  return <section className="ws-stat-grid" aria-label="Workspace statistics">{stats.map((stat) => <WidgetContainer className={`ws-stat-card ${stat.tone}`} key={stat.label}><div className="ws-stat-icon"><stat.icon size={19} /></div><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></WidgetContainer>)}</section>;
}

export function WelcomeCard() {
  return <WidgetContainer className="ws-welcome-card"><div><p className="ws-kicker">Good morning</p><h1>Welcome back to VoiceSense.</h1><p>Your demo workspace is staged with {demoWorkspace.employee}, {demoWorkspace.workflow}, {demoWorkspace.knowledgeBase}, and {demoWorkspace.conversation} so teams can experience value in minutes.</p></div><div className="ws-welcome-actions"><Button>Create employee</Button><Button variant="outline">Open playground</Button></div></WidgetContainer>;
}

export function OnboardingChecklist() {
  return <WidgetContainer><SectionHeader eyebrow="Onboarding" title="Release-ready setup" /><div className="ws-onboarding-list">{onboardingChecklist.map((item) => <div className="ws-onboarding-row" data-complete={item.complete} key={item.label}><span>{item.complete ? "Done" : "Next"}</span><div><strong>{item.label}</strong><p>{item.detail}</p></div></div>)}</div></WidgetContainer>;
}

export function UsageOverview() {
  const max = Math.max(...usageSeries.map((item) => item.minutes));
  return <WidgetContainer className="ws-usage"><SectionHeader eyebrow="Usage" title="Weekly minutes" action={<Button variant="ghost" size="sm">View details</Button>} /><div className="ws-bars" aria-label="Weekly usage minutes">{usageSeries.map((item) => <div className="ws-bar-item" key={item.day}><div><span style={{ height: `${Math.max(14, (item.minutes / max) * 100)}%` }} /></div><p>{item.day}</p></div>)}</div></WidgetContainer>;
}

export function ActivityFeed() {
  return <WidgetContainer><SectionHeader eyebrow="Recent activity" title="Workspace events" /><div className="ws-activity-list">{activity.map((event) => <div className="ws-activity-row" key={event.title}><span className="ws-activity-time">{event.time}</span><div className="ws-activity-icon"><event.icon size={16} /></div><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></WidgetContainer>;
}

export function QuickActions() {
  return <WidgetContainer><SectionHeader eyebrow="Quick actions" title="Common setup paths" /><div className="ws-action-grid">{quickActions.map((action) => <button className="ws-action-card" type="button" key={action.label}><action.icon size={18} /><span><strong>{action.label}</strong><small>{action.detail}</small></span><ArrowRight size={16} /></button>)}</div></WidgetContainer>;
}

export function SystemStatus() {
  return <WidgetContainer><SectionHeader eyebrow="System" title="Status" /><div className="ws-status-list">{systemStatus.map((item) => <div className="ws-status-row" key={item.label}><item.icon size={17} /><span>{item.label}</span><strong>{item.value}</strong></div>)}</div></WidgetContainer>;
}

export function EmptyStateGallery() {
  return <WidgetContainer className="ws-empty-gallery"><SectionHeader eyebrow="Empty states" title="First-run guidance" /><div className="ws-empty-grid">{emptyStates.map((state) => <div className="ws-empty-card" key={state.title}><state.icon size={22} /><strong>{state.title}</strong><p>{state.description}</p><Button variant="outline" size="sm">{state.action}</Button></div>)}</div></WidgetContainer>;
}

export function LoadingPreview() {
  return <WidgetContainer><SectionHeader eyebrow="Loading" title="Stable skeletons" /><div className="ws-loading-grid"><Skeleton className="ws-loading-card" /><Skeleton className="ws-loading-card" /><Skeleton className="ws-loading-line" /><Skeleton className="ws-loading-line" /></div></WidgetContainer>;
}

export function ErrorPreview() {
  return <WidgetContainer className="ws-error-card"><AlertCircle size={24} /><div><strong>Could not load dashboard metrics</strong><p>Check your connection or retry. The layout keeps its dimensions while recovering.</p></div><Button variant="outline" size="sm"><RefreshCcw size={15} />Retry</Button></WidgetContainer>;
}