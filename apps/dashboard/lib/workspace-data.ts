import {
  Activity,
  Archive,
  BarChart3,
  Bell,
  BookOpen,
  BrainCircuit,
  Bot,
  Building2,
  Cable,
  ChevronRight,
  CircleDollarSign,
  Code2,
  DatabaseZap,
  FileSearch,
  Gauge,
  GitBranch,
  Home,
  Inbox,
  KeyRound,
  Layers3,
  LifeBuoy,
  MessageSquareText,
  Phone,
  Plus,
  RadioTower,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
  Workflow,
  Wrench,
} from "lucide-react";

export const workspaceOrgs = [
  { name: "Acme Co", plan: "Scale", active: true },
  { name: "Northstar Labs", plan: "Sandbox", active: false },
  { name: "Studio Atlas", plan: "Agency", active: false },
];

export const workspaceGroups = [
  {
    label: "Operate",
    items: [
      { label: "Dashboard", href: "/", icon: Home, active: true },
      { label: "AI Employees", href: "/employees", icon: Bot, children: ["Builder", "Testing", "Deployments"] },
      { label: "AI Studio", href: "/studio", icon: Sparkles, children: ["Prompts", "Playground", "Evaluations"] },
      { label: "AI Teams", href: "/teams", icon: Building2, children: ["Org chart", "Delegation", "Policies"] },
      { label: "Conversations", href: "/conversations", icon: MessageSquareText, children: ["Inbox", "Live", "Reviews"] },
      { label: "Omnichannel", href: "/omnichannel", icon: Inbox, children: ["Channels", "Timeline", "Delivery"] },
      { label: "Telephony", href: "/telephony", icon: Phone, children: ["Numbers", "Queues", "Providers"] },
      { label: "Voice Engine", href: "/voice", icon: RadioTower, children: ["Sessions", "Providers", "Testing"] },
    ],
  },
  {
    label: "Knowledge and action",
    items: [
      { label: "Knowledge Base", href: "/knowledge", icon: BookOpen, children: ["Sources", "Indexes", "Memory"] },
      { label: "Retrieval", href: "/retrieval", icon: FileSearch, children: ["Indexes", "Playground", "Providers"] },
      { label: "Memory", href: "/memory", icon: BrainCircuit, children: ["Explorer", "Policies", "Analytics"] },
      { label: "Storage", href: "/storage", icon: Archive, children: ["Files", "Uploads", "Trash"] },
      { label: "Workflows", href: "/workflows", icon: Workflow },
      { label: "Tools", href: "/tools", icon: Wrench, children: ["Registry", "Playground", "MCP"] },
      { label: "Integrations", href: "/integrations", icon: Cable },
      { label: "Analytics", href: "/analytics", icon: BarChart3 },
    ],
  },
  {
    label: "Platform",
    items: [
      { label: "Developer", href: "/developer", icon: Code2, children: ["API keys", "Webhooks", "Docs"] },
      { label: "Billing", href: "/billing", icon: CircleDollarSign },
      { label: "Security", href: "/security", icon: ShieldCheck, children: ["Policies", "Audit", "Compliance"] },
      { label: "Settings", href: "/settings", icon: Settings },
    ],
  },
];

export const topUtilityItems = [
  { label: "Notifications", icon: Bell },
  { label: "Support", icon: LifeBuoy },
  { label: "Security", icon: ShieldCheck },
];

export const stats = [
  { label: "AI employees", value: "12", detail: "+3 this month", icon: Bot, tone: "green" },
  { label: "Active conversations", value: "248", detail: "31 live now", icon: MessageSquareText, tone: "blue" },
  { label: "Monthly minutes", value: "18.4k", detail: "62% of quota", icon: RadioTower, tone: "amber" },
  { label: "Tool success rate", value: "98.2%", detail: "+1.8% vs last week", icon: Gauge, tone: "purple" },
];

export const usageSeries = [
  { day: "Mon", minutes: 2200 },
  { day: "Tue", minutes: 3100 },
  { day: "Wed", minutes: 2700 },
  { day: "Thu", minutes: 3900 },
  { day: "Fri", minutes: 3400 },
  { day: "Sat", minutes: 2100 },
  { day: "Sun", minutes: 980 },
];

export const activity = [
  { time: "10:42", title: "Maya resolved a billing question", detail: "Customer Success Agent", icon: Sparkles },
  { time: "10:18", title: "Knowledge index refreshed", detail: "182 documents processed", icon: DatabaseZap },
  { time: "09:57", title: "Refund workflow requested review", detail: "Human approval required", icon: GitBranch },
  { time: "09:31", title: "New phone number connected", detail: "+1 (415) 010-2194", icon: Phone },
];

export const quickActions = [
  { label: "Create AI employee", detail: "Design a role, voice, tools, and guardrails.", icon: Plus },
  { label: "Test a conversation", detail: "Run a safe simulation before going live.", icon: MessageSquareText },
  { label: "Connect knowledge", detail: "Add docs, URLs, and company policies.", icon: FileSearch },
  { label: "Invite teammate", detail: "Add operators, developers, and managers.", icon: Building2 },
];

export const systemStatus = [
  { label: "Voice gateway", value: "Operational", icon: RadioTower },
  { label: "API", value: "Operational", icon: Code2 },
  { label: "Workflow queue", value: "Operational", icon: Workflow },
  { label: "Knowledge indexing", value: "Operational", icon: Layers3 },
];

export const emptyStates = [
  { title: "No AI employees yet", description: "Create a focused employee for a specific business role before expanding coverage.", action: "Create employee", icon: Bot },
  { title: "No conversations yet", description: "Run a test conversation or connect a channel to begin collecting transcripts.", action: "Start test", icon: Inbox },
  { title: "No knowledge base", description: "Add source material so employees can answer with company-specific context.", action: "Add source", icon: BookOpen },
  { title: "No integrations", description: "Connect tools when you are ready for employees to take approved actions.", action: "Browse integrations", icon: Cable },
];

export const breadcrumbs = ["Workspace", "Dashboard"];
export const commandSuggestions = ["Create employee", "Search conversations", "Invite member", "Open API keys"];
export const shellIcons = { Search, ChevronRight, KeyRound, Activity };






export const onboardingChecklist = [
  { label: "Create sample AI employee", detail: "Start with Maya, the customer support employee.", complete: true },
  { label: "Connect knowledge", detail: "Use demo policies, FAQs, and product docs.", complete: true },
  { label: "Run AI Studio simulation", detail: "Validate happy paths, edge cases, and escalation behavior.", complete: false },
  { label: "Review production gates", detail: "Check security, billing, analytics, and deployment readiness.", complete: false },
];

export const demoWorkspace = {
  organization: "Acme Co",
  employee: "Maya",
  workflow: "Refund approval",
  knowledgeBase: "Support policies",
  integration: "CRM sandbox",
  conversation: "Billing dispute simulation",
};