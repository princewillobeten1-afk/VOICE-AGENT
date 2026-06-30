import {
  Activity,
  AudioLines,
  Bot,
  BrainCircuit,
  CalendarClock,
  ChartSpline,
  CircleCheck,
  Clock3,
  Code2,
  DatabaseZap,
  GitBranch,
  Headphones,
  Inbox,
  KeyRound,
  MessageSquareText,
  PhoneCall,
  PlugZap,
  RadioTower,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";

export const navigation = [
  { label: "Command", icon: Activity, active: true },
  { label: "Employees", icon: Bot },
  { label: "Conversations", icon: MessageSquareText },
  { label: "Voice", icon: AudioLines },
  { label: "Knowledge", icon: Search },
  { label: "Workflows", icon: Workflow },
  { label: "Developers", icon: Code2 },
  { label: "Security", icon: ShieldCheck },
];

export const channels = [
  { label: "Phone", value: "1,284", icon: PhoneCall, tone: "green" },
  { label: "Chat", value: "842", icon: MessageSquareText, tone: "blue" },
  { label: "Email", value: "391", icon: Send, tone: "amber" },
  { label: "WhatsApp", value: "226", icon: Inbox, tone: "purple" },
];

export const employees = [
  {
    name: "Maya",
    role: "Customer Success Agent",
    status: "Live",
    latency: "612 ms",
    resolution: "82%",
    channels: ["Phone", "Chat", "Email"],
  },
  {
    name: "Atlas",
    role: "Sales Development Agent",
    status: "Testing",
    latency: "708 ms",
    resolution: "76%",
    channels: ["Phone", "Calendar", "CRM"],
  },
  {
    name: "Nova",
    role: "Support Triage Agent",
    status: "Draft",
    latency: "--",
    resolution: "--",
    channels: ["Chat", "Knowledge", "Workflow"],
  },
];

export const runtimeEvents = [
  { time: "09:42", label: "Inbound call routed to Maya", icon: PhoneCall },
  { time: "09:43", label: "Knowledge search returned 7 policy matches", icon: DatabaseZap },
  { time: "09:44", label: "Refund workflow requested approval", icon: GitBranch },
  { time: "09:46", label: "Customer follow-up email drafted", icon: Send },
];

export const qualityMetrics = [
  { label: "Avg voice latency", value: "642 ms", delta: "-18%", icon: RadioTower },
  { label: "Resolved without handoff", value: "79.4%", delta: "+6.1%", icon: CircleCheck },
  { label: "Tool success rate", value: "98.2%", delta: "+1.8%", icon: PlugZap },
  { label: "Guardrail blocks", value: "31", delta: "stable", icon: ShieldCheck },
];

export const buildSteps = [
  { label: "Identity", icon: Bot, complete: true },
  { label: "Instructions", icon: BrainCircuit, complete: true },
  { label: "Voice", icon: Headphones, complete: true },
  { label: "Tools", icon: PlugZap, complete: false },
  { label: "Schedule", icon: CalendarClock, complete: false },
  { label: "Evaluate", icon: ChartSpline, complete: false },
];

export const conversationTurns = [
  { speaker: "Customer", text: "I need to move my onboarding call and ask about the annual plan." },
  { speaker: "Maya", text: "I can help with both. I found your account and two available times tomorrow." },
  { speaker: "Tool", text: "Calendar availability checked. CRM account context loaded." },
];

export const topActions = [
  { label: "Create employee", icon: Sparkles },
  { label: "Test voice", icon: AudioLines },
  { label: "API keys", icon: KeyRound },
  { label: "View logs", icon: Clock3 },
];
