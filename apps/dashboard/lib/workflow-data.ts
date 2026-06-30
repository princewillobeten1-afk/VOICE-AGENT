import { Activity, AlertTriangle, Bot, CalendarClock, CheckCircle2, Clock3, Code2, Database, GitBranch, GitMerge, History, KeyRound, Layers3, Mail, MessageSquareText, MousePointer2, Play, RefreshCw, Route, Search, Settings, ShieldCheck, SlidersHorizontal, Sparkles, Split, Square, Timer, Workflow, Zap } from "lucide-react";

export const workflowStats = [
  { label: "Published workflows", value: "38", detail: "+6 this month", icon: Workflow, tone: "green" },
  { label: "Running now", value: "124", detail: "18 waiting", icon: Activity, tone: "blue" },
  { label: "Success rate", value: "97.6%", detail: "last 7 days", icon: CheckCircle2, tone: "purple" },
  { label: "Avg duration", value: "2.8s", detail: "p95 9.4s", icon: Timer, tone: "amber" },
];

export const workflows = [
  { name: "Lead Qualification", category: "Sales", status: "Published", trigger: "Webhook", executions: "18.2k", success: 98, updated: "12 min ago" },
  { name: "Support Escalation", category: "Customer Support", status: "Published", trigger: "Conversation Event", executions: "9.4k", success: 96, updated: "34 min ago" },
  { name: "Invoice Processing", category: "Finance", status: "Draft", trigger: "Schedule", executions: "1.1k", success: 91, updated: "Yesterday" },
  { name: "Onboarding Follow-up", category: "HR", status: "Paused", trigger: "API", executions: "2.8k", success: 94, updated: "3 days ago" },
];

export const nodePalette = [
  { label: "Start", group: "Core", icon: Play, detail: "Manual, API, event, webhook" },
  { label: "Condition", group: "Control", icon: GitBranch, detail: "If / else routing" },
  { label: "Split", group: "Control", icon: Split, detail: "Parallel branches" },
  { label: "Human Approval", group: "Human", icon: ShieldCheck, detail: "Pause for review" },
  { label: "AI Employee", group: "AI", icon: Bot, detail: "Delegate to employee" },
  { label: "Knowledge Search", group: "AI", icon: Search, detail: "Retrieve context" },
  { label: "HTTP Request", group: "Integration", icon: Code2, detail: "Call custom API" },
  { label: "Email", group: "Integration", icon: Mail, detail: "Send or process mail" },
];

export const canvasNodes = [
  { key: "start", label: "Webhook received", type: "Start", x: 8, y: 18, icon: Play, tone: "green" },
  { key: "qualify", label: "AI qualification", type: "AI Employee", x: 31, y: 18, icon: Bot, tone: "blue" },
  { key: "condition", label: "Score above 80?", type: "Condition", x: 55, y: 18, icon: GitBranch, tone: "amber" },
  { key: "crm", label: "Update CRM", type: "CRM", x: 78, y: 8, icon: Database, tone: "purple" },
  { key: "approval", label: "Human review", type: "Approval", x: 78, y: 34, icon: ShieldCheck, tone: "red" },
];

export const executions = [
  { id: "run_82A", workflow: "Lead Qualification", status: "Running", node: "AI qualification", duration: "1.2s", retries: 0 },
  { id: "run_81F", workflow: "Support Escalation", status: "Paused", node: "Human approval", duration: "4m 21s", retries: 1 },
  { id: "run_80C", workflow: "Invoice Processing", status: "Completed", node: "End", duration: "8.4s", retries: 0 },
  { id: "run_7FF", workflow: "Onboarding Follow-up", status: "Failed", node: "HTTP Request", duration: "2.1s", retries: 3 },
];

export const templates = [
  { name: "Lead Qualification", category: "Sales", difficulty: "Intermediate", nodes: 14, icon: Sparkles },
  { name: "Appointment Booking", category: "Scheduling", difficulty: "Beginner", nodes: 9, icon: CalendarClock },
  { name: "Customer Support", category: "Support", difficulty: "Intermediate", nodes: 18, icon: MessageSquareText },
  { name: "Employee Onboarding", category: "HR", difficulty: "Advanced", nodes: 22, icon: Layers3 },
];

export const versionHistory = [
  { version: "v12", status: "Published", change: "Added approval branch", time: "Today", icon: CheckCircle2 },
  { version: "v11", status: "Rollback-ready", change: "Updated CRM transform", time: "Yesterday", icon: History },
  { version: "v10", status: "Draft", change: "Tested AI score threshold", time: "3 days ago", icon: SlidersHorizontal },
];

export const workflowLogs = [
  { time: "10:42", title: "Node executed", detail: "AI qualification completed in 820 ms.", icon: Zap },
  { time: "10:41", title: "Workflow paused", detail: "Human approval requested for Enterprise lead.", icon: ShieldCheck },
  { time: "10:39", title: "Retry scheduled", detail: "HTTP Request retry 2 of 3 after timeout.", icon: RefreshCw },
  { time: "10:34", title: "Error branch entered", detail: "CRM update failed validation.", icon: AlertTriangle },
];

export const builderControls = [
  { label: "Select", icon: MousePointer2 },
  { label: "Zoom", icon: Search },
  { label: "Auto layout", icon: Route },
  { label: "Merge", icon: GitMerge },
  { label: "End", icon: Square },
  { label: "Settings", icon: Settings },
];

export const workflowIcons = { Workflow, KeyRound, Clock3 };
