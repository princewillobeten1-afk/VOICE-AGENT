import { Activity, Bot, CalendarDays, CheckCircle2, Cloud, CreditCard, Database, KeyRound, Mail, MessageSquare, PlugZap, RefreshCw, ShieldCheck, Workflow } from "lucide-react";

export const integrationStats = [
  { label: "Installed", value: "18", detail: "12 healthy", icon: PlugZap, tone: "green" },
  { label: "Marketplace", value: "186", detail: "18 categories", icon: Cloud, tone: "blue" },
  { label: "Sync volume", value: "1.8M", detail: "99.4% success", icon: Workflow, tone: "purple" },
  { label: "Credential rotations", value: "6", detail: "2 expiring soon", icon: KeyRound, tone: "amber" },
];

export const categories = ["All", "Communication", "CRM", "Calendars", "Storage", "Automation", "Messaging", "Payments", "AI", "Databases", "Projects", "Support", "Development", "Productivity"];

export const availableIntegrations = [
  { name: "Gmail", category: "Communication", auth: "OAuth 2.0", status: "Available", featured: true, icon: Mail, capabilities: ["Send email", "New email"] },
  { name: "Slack", category: "Communication", auth: "OAuth 2.0", status: "Available", featured: true, icon: MessageSquare, capabilities: ["Send message", "New message"] },
  { name: "HubSpot", category: "CRM", auth: "OAuth / API key", status: "Available", featured: true, icon: Activity, capabilities: ["Create contact", "Contact updated"] },
  { name: "Google Calendar", category: "Calendars", auth: "OAuth PKCE", status: "Available", featured: true, icon: CalendarDays, capabilities: ["Schedule meeting", "Event created"] },
  { name: "Stripe", category: "Payments", auth: "API key", status: "Available", featured: false, icon: CreditCard, capabilities: ["Create customer", "Payment received"] },
  { name: "OpenAI", category: "AI", auth: "API key", status: "Available", featured: false, icon: Bot, capabilities: ["Provider config", "Usage event"] },
  { name: "PostgreSQL", category: "Databases", auth: "Basic / Custom", status: "Available", featured: false, icon: Database, capabilities: ["Query", "Row created"] },
  { name: "Salesforce", category: "CRM", auth: "OAuth / JWT", status: "Available", featured: false, icon: Activity, capabilities: ["Create lead", "Account updated"] },
  { name: "Zendesk", category: "Support", auth: "OAuth / API key", status: "Available", featured: false, icon: ShieldCheck, capabilities: ["Create ticket", "Ticket updated"] },
];

export const installedConnections = [
  { name: "Gmail - Support", provider: "Gmail", status: "Healthy", health: "99.9%", auth: "OAuth 2.0", lastChecked: "2 min ago" },
  { name: "Stripe - Production", provider: "Stripe", status: "Healthy", health: "99.8%", auth: "API key", lastChecked: "8 min ago" },
  { name: "Slack - Ops", provider: "Slack", status: "Degraded", health: "91.2%", auth: "OAuth 2.0", lastChecked: "14 min ago" },
  { name: "HubSpot - Sales", provider: "HubSpot", status: "Needs rotation", health: "87.4%", auth: "Private app", lastChecked: "1 hr ago" },
];

export const activityFeed = [
  { title: "Connection tested", detail: "Gmail - Support returned healthy", time: "10:52" },
  { title: "Credential rotation scheduled", detail: "HubSpot - Sales expires in 7 days", time: "10:10" },
  { title: "Action executed", detail: "Stripe create_customer accepted by connector", time: "09:44" },
  { title: "Trigger registered", detail: "Slack new_message placeholder subscribed", time: "09:12" },
];

export const connectorMethods = ["install()", "authenticate()", "validatePermissions()", "sync()", "executeAction()", "executeTrigger()", "publishVersion()", "testConnection()"];