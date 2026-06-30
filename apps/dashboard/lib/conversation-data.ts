import { Activity, AlertTriangle, Bot, BrainCircuit, CheckCircle2, Clock3, Goal, Handshake, Inbox, MessageSquareText, PauseCircle, RadioTower, RefreshCw, Send, ShieldCheck, Sparkles, UserRound, Workflow } from "lucide-react";

export const conversationStats = [
  { label: "Live conversations", value: "312", detail: "46 active now", icon: MessageSquareText, tone: "green" },
  { label: "Avg response", value: "742 ms", detail: "Across all channels", icon: Clock3, tone: "blue" },
  { label: "Goal completion", value: "81%", detail: "+6% this week", icon: Goal, tone: "purple" },
  { label: "Handoffs", value: "3.8%", detail: "Policy-safe escalation", icon: Handshake, tone: "amber" },
];

export const channelAdapters = [
  { channel: "Voice", adapter: "voice_adapter", status: "Ready", icon: RadioTower, capabilities: ["interruptions", "partial turns", "session recovery"] },
  { channel: "Web chat", adapter: "chat_adapter", status: "Ready", icon: MessageSquareText, capabilities: ["typing", "history", "handoff"] },
  { channel: "Email", adapter: "email_adapter", status: "Foundation", icon: Inbox, capabilities: ["threading", "async replies"] },
  { channel: "SMS", adapter: "sms_adapter", status: "Foundation", icon: Send, capabilities: ["short turns", "opt-out hooks"] },
  { channel: "Slack / Teams", adapter: "collab_adapter", status: "Future", icon: Workflow, capabilities: ["mentions", "threads"] },
];

export const conversationTimeline = [
  { time: "10:42:04", event: "conversation.started", detail: "Maya opened a customer success conversation from web chat.", icon: Sparkles },
  { time: "10:42:09", event: "context.loaded", detail: "Profile, billing policy, active subscription, and previous tickets prioritized.", icon: BrainCircuit },
  { time: "10:42:18", event: "user.message", detail: "Customer asked about duplicate charge and cancellation.", icon: UserRound },
  { time: "10:42:19", event: "intent.detected", detail: "billing_dispute + cancellation_risk, confidence placeholder 0.86.", icon: Activity },
  { time: "10:42:20", event: "ai.response", detail: "AI response generated with refund approval guardrail.", icon: Bot },
  { time: "10:42:30", event: "handoff.ready", detail: "Live agent transfer summary prepared but not triggered.", icon: Handshake },
];

export const activeSessions = [
  { id: "cs_2104", channel: "Voice", speaker: "Customer", state: "Active", topic: "Billing dispute", expires: "44 min" },
  { id: "cs_2103", channel: "Web chat", speaker: "AI employee", state: "Planning", topic: "Lead qualification", expires: "22 hr" },
  { id: "cs_2101", channel: "Email", speaker: "None", state: "Paused", topic: "Follow-up", expires: "6 days" },
];

export const goals = [
  { name: "Resolve support issue", status: "Active", progress: 68, detail: "Need confirmation on duplicate charge." },
  { name: "Reduce cancellation risk", status: "Monitoring", progress: 44, detail: "Offer policy-safe options." },
  { name: "Collect information", status: "Complete", progress: 100, detail: "Account and transaction identified." },
];

export const contextSources = [
  { label: "Current conversation", value: "6 turns", icon: MessageSquareText },
  { label: "User profile", value: "Loaded", icon: UserRound },
  { label: "Knowledge", value: "Billing policy", icon: BrainCircuit },
  { label: "Workflow state", value: "Refund approval pending", icon: Workflow },
  { label: "Memory hooks", value: "Architecture only", icon: ShieldCheck },
  { label: "Integration data", value: "CRM snapshot", icon: Activity },
];

export const analyticsCards = [
  { label: "Turn count", value: "14", icon: MessageSquareText },
  { label: "Duration", value: "08:16", icon: Clock3 },
  { label: "Intent switches", value: "2", icon: RefreshCw },
  { label: "Sentiment", value: "Placeholder", icon: Activity },
];

export const historyRows = [
  { subject: "Duplicate charge", channel: "Web chat", status: "Open", employee: "Maya", updated: "2 min ago" },
  { subject: "Demo request", channel: "SMS", status: "Completed", employee: "Nova", updated: "18 min ago" },
  { subject: "Appointment change", channel: "Voice", status: "Paused", employee: "Atlas", updated: "1 hr ago" },
  { subject: "Invoice copy", channel: "Email", status: "Handoff", employee: "Maya", updated: "Yesterday" },
];

export const engineChecks = [
  { label: "Channel independent", state: "Yes", icon: CheckCircle2 },
  { label: "State recovery", state: "Ready", icon: ShieldCheck },
  { label: "Tool hooks", state: "Future", icon: Workflow },
  { label: "RAG hooks", state: "Future", icon: BrainCircuit },
  { label: "Human handoff", state: "Architecture", icon: AlertTriangle },
  { label: "Analytics", state: "Collecting", icon: Activity },
];