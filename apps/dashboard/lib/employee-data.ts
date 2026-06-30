import {
  Activity,
  BadgeCheck,
  BookOpen,
  Bot,
  BrainCircuit,
  CalendarClock,
  CheckCircle2,
  CircleAlert,
  GitBranch,
  MessageSquareText,
  Mic2,
  Phone,
  ShieldCheck,
  Sparkles,
  Timer,
  Wrench,
  Zap,
} from "lucide-react";

export const employeeStats = [
  { label: "Live employees", value: "8", detail: "4 in testing", icon: Bot, tone: "green" },
  { label: "Conversations today", value: "1,284", detail: "31 active now", icon: MessageSquareText, tone: "blue" },
  { label: "Avg response latency", value: "1.2s", detail: "Voice + chat", icon: Timer, tone: "amber" },
  { label: "Resolved without handoff", value: "86%", detail: "+7% this week", icon: BadgeCheck, tone: "purple" },
];

export const employees = [
  {
    name: "Maya",
    role: "Customer Success Agent",
    status: "Live",
    model: "GPT-4.1",
    channel: "Voice, chat, email",
    owner: "CX Team",
    conversations: "642",
    resolution: "91%",
    latency: "1.1s",
    guardrail: "Strict refunds",
    tags: ["Billing", "Retention", "Escalation"],
  },
  {
    name: "Noah",
    role: "Inbound Sales Qualifier",
    status: "Testing",
    model: "GPT-4.1 mini",
    channel: "Phone, SMS",
    owner: "Revenue",
    conversations: "188",
    resolution: "78%",
    latency: "940ms",
    guardrail: "Human approval",
    tags: ["Lead scoring", "Calendar", "CRM"],
  },
  {
    name: "Iris",
    role: "Internal IT Helper",
    status: "Draft",
    model: "Claude Sonnet",
    channel: "Slack, web",
    owner: "Operations",
    conversations: "0",
    resolution: "-",
    latency: "-",
    guardrail: "Read-only tools",
    tags: ["Policies", "Tickets", "Knowledge"],
  },
];

export const builderSteps = [
  { label: "Role and success criteria", status: "Complete", icon: CheckCircle2 },
  { label: "Instructions and tone", status: "Complete", icon: BrainCircuit },
  { label: "Knowledge sources", status: "Needs review", icon: BookOpen },
  { label: "Tools and approvals", status: "In progress", icon: Wrench },
  { label: "Channels and voice", status: "Not started", icon: Mic2 },
];

export const readinessChecks = [
  { label: "Prompt policy", value: "Passed", icon: ShieldCheck, tone: "success" },
  { label: "Knowledge freshness", value: "Review", icon: CircleAlert, tone: "warning" },
  { label: "Tool permissions", value: "Scoped", icon: Wrench, tone: "success" },
  { label: "Fallback routing", value: "Ready", icon: GitBranch, tone: "success" },
];

export const testConversation = [
  { speaker: "Customer", body: "I was charged twice for my subscription. Can you fix it before my renewal?", tone: "customer" },
  { speaker: "Maya", body: "I can help with that. I found two charges on the same invoice and can prepare a refund request for the duplicate.", tone: "employee" },
  { speaker: "Tool call", body: "billing.refund.preview returned eligible_duplicate_charge with manager approval required.", tone: "tool" },
  { speaker: "Maya", body: "The refund is ready for approval. I also added a note to prevent the renewal from retrying the duplicate amount.", tone: "employee" },
];

export const runtimeEvents = [
  { time: "10:42", title: "Refund workflow requested approval", detail: "Maya paused before taking a sensitive action.", icon: GitBranch },
  { time: "10:39", title: "Knowledge answer cited policy", detail: "Used Billing policy v3 and Renewal FAQ.", icon: BookOpen },
  { time: "10:33", title: "Voice latency warning recovered", detail: "TTS provider fallback restored response time.", icon: Activity },
  { time: "10:28", title: "Sales call booked", detail: "Noah scheduled a qualified demo for Thursday.", icon: CalendarClock },
];

export const channelCoverage = [
  { label: "Voice", value: "6 employees", icon: Phone, tone: "green" },
  { label: "Chat", value: "8 employees", icon: MessageSquareText, tone: "blue" },
  { label: "Automation", value: "14 tools", icon: Zap, tone: "amber" },
  { label: "AI review", value: "23 flagged", icon: Sparkles, tone: "purple" },
];
