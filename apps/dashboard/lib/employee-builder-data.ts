import { Activity, BadgeCheck, BookOpen, Bot, BrainCircuit, CalendarClock, CheckCircle2, ClipboardList, Database, FileText, GitBranch, Globe2, History, Mail, MemoryStick, MessageSquareText, Mic2, Phone, PlugZap, Rocket, Settings, ShieldCheck, Sparkles, UserRound, Volume2, Workflow, Wrench } from "lucide-react";

export const builderWizardSteps = [
  { step: 1, label: "Identity", icon: UserRound, status: "Complete" },
  { step: 2, label: "Personality", icon: Sparkles, status: "Complete" },
  { step: 3, label: "Instructions", icon: FileText, status: "In progress" },
  { step: 4, label: "Voice", icon: Mic2, status: "Ready" },
  { step: 5, label: "Knowledge", icon: BookOpen, status: "Needs source" },
  { step: 6, label: "Tools", icon: Wrench, status: "Scoped" },
  { step: 7, label: "Memory", icon: MemoryStick, status: "Policy set" },
  { step: 8, label: "Channels", icon: MessageSquareText, status: "Draft" },
  { step: 9, label: "Review", icon: ShieldCheck, status: "Pending" },
  { step: 10, label: "Publish", icon: Rocket, status: "Locked" },
];

export const personalityControls = [
  { label: "Formality", value: "72" },
  { label: "Creativity", value: "38" },
  { label: "Confidence", value: "84" },
  { label: "Response length", value: "56" },
];

export const employeeTemplates = [
  { name: "Receptionist", role: "Front desk and routing", icon: Phone, channels: "Phone, chat" },
  { name: "Sales Representative", role: "Lead qualification", icon: BadgeCheck, channels: "Phone, SMS, email" },
  { name: "Customer Support", role: "Policy-aware resolution", icon: MessageSquareText, channels: "Chat, email, phone" },
  { name: "Appointment Scheduler", role: "Calendar coordination", icon: CalendarClock, channels: "Phone, SMS" },
  { name: "HR Assistant", role: "Internal policy support", icon: ClipboardList, channels: "Chat, email" },
  { name: "Technical Support", role: "Troubleshooting intake", icon: Database, channels: "Chat, email" },
];

export const builderKnowledgeSources = ["Billing policy", "Help center", "CRM account notes", "Refund FAQ"];
export const builderTools = ["CRM read", "Calendar schedule", "Email draft", "Refund preview", "Human approval"];
export const builderChannels = ["Phone", "Chat", "Email", "SMS", "WhatsApp", "Slack", "Teams"];

export const profileTabs = ["Overview", "Configuration", "Activity", "Conversations", "Analytics", "Knowledge", "Integrations", "Memory", "Version History", "Settings"];

export const versionHistory = [
  { version: "v4", status: "Published", summary: "Added strict refund escalation and shorter answers.", date: "Today" },
  { version: "v3", status: "Archived", summary: "Updated billing policy language.", date: "Jun 24" },
  { version: "v2", status: "Archived", summary: "Added CRM lookup permissions.", date: "Jun 18" },
  { version: "v1", status: "Draft", summary: "Initial customer success configuration.", date: "Jun 10" },
];

export const playgroundTurns = [
  { speaker: "Tester", body: "I need to cancel but I was also charged twice.", tone: "customer" },
  { speaker: "Maya", body: "I can help with both. I will first verify the duplicate charge, then explain cancellation options clearly.", tone: "employee" },
  { speaker: "Context preview", body: "Billing policy v3, Refund FAQ, CRM account note: renewal issue detected.", tone: "tool" },
  { speaker: "Tool log", body: "refund.preview placeholder accepted. Human approval required before action.", tone: "tool" },
];

export const playgroundMetrics = [
  { label: "Response time", value: "184 ms", icon: BrainCircuit },
  { label: "Token usage", value: "Placeholder", icon: Activity },
  { label: "Context items", value: "4", icon: BookOpen },
  { label: "Tool calls", value: "1 mock", icon: PlugZap },
];



export const profileActivity = [
  { title: "Published v4", detail: "Refund escalation guardrail updated.", time: "10:40", icon: Rocket },
  { title: "Simulation passed", detail: "12 of 14 test cases passed readiness review.", time: "09:20", icon: CheckCircle2 },
  { title: "Knowledge source changed", detail: "Billing policy v3 attached.", time: "Yesterday", icon: BookOpen },
  { title: "Integration scoped", detail: "CRM access limited to read-only fields.", time: "Yesterday", icon: PlugZap },
];

export const voiceSettings = [
  { label: "Provider", value: "Placeholder Voice" },
  { label: "Voice", value: "Warm professional" },
  { label: "Speed", value: "1.02x" },
  { label: "Stability", value: "82%" },
  { label: "Expressiveness", value: "64%" },
  { label: "Accent", value: "Neutral" },
];

export const channelIcons = { Phone, Mail, MessageSquareText, Globe2, Volume2, Workflow, Bot, Settings, GitBranch };