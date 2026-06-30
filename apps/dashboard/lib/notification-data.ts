import { AlertTriangle, Bell, CheckCircle2, CreditCard, Info, KeyRound, ShieldAlert, Users, Workflow } from "lucide-react";

export const notificationStats = [
  { label: "Unread", value: "12", detail: "4 security related", icon: Bell, tone: "blue" },
  { label: "Events today", value: "18.2k", detail: "99.98% processed", icon: Workflow, tone: "green" },
  { label: "Failed deliveries", value: "7", detail: "Queued for retry", icon: AlertTriangle, tone: "amber" },
  { label: "Subscribers", value: "6", detail: "1 active engine", icon: CheckCircle2, tone: "purple" },
];

export const notifications = [
  { title: "API key created", body: "Ada created Production API key in Acme Co.", category: "Security", severity: "Warning", status: "Unread", time: "3 min ago", icon: KeyRound },
  { title: "File upload completed", body: "Support policy handbook.pdf is ready in Storage.", category: "System", severity: "Success", status: "Unread", time: "12 min ago", icon: CheckCircle2 },
  { title: "New teammate joined", body: "Maya joined Customer Success workspace.", category: "Team", severity: "Information", status: "Read", time: "44 min ago", icon: Users },
  { title: "Billing settings updated", body: "Plan contact was changed for Acme Co.", category: "Billing", severity: "Information", status: "Read", time: "2 hr ago", icon: CreditCard },
  { title: "Workflow retry scheduled", body: "Refund review workflow failed once and is queued for retry.", category: "System", severity: "Error", status: "Unread", time: "Yesterday", icon: AlertTriangle },
  { title: "Security event recorded", body: "A new sign-in was recorded from a trusted device.", category: "Security", severity: "Information", status: "Read", time: "Yesterday", icon: ShieldAlert },
];

export const eventLogs = [
  { event: "api_key.created", status: "Processed", subscriber: "notification-engine", latency: "18 ms", retries: 0 },
  { event: "file.uploaded", status: "Processed", subscriber: "notification-engine", latency: "23 ms", retries: 0 },
  { event: "workflow.executed", status: "Retrying", subscriber: "webhook-dispatcher", latency: "312 ms", retries: 1 },
  { event: "billing.updated", status: "Processed", subscriber: "notification-engine", latency: "17 ms", retries: 0 },
];

export const notificationFilters = ["All", "Unread", "Security", "Billing", "Team", "System"];

export const preferenceChannels = [
  { label: "In-app", description: "Show notifications in the VoiceSense workspace.", enabled: true, status: "Implemented" },
  { label: "Email", description: "Send important summaries and security alerts by email.", enabled: false, status: "Architecture ready" },
  { label: "SMS", description: "Placeholder for future urgent mobile notifications.", enabled: false, status: "Placeholder" },
  { label: "Push", description: "Placeholder for future browser and mobile push.", enabled: false, status: "Placeholder" },
  { label: "Webhooks", description: "Forward selected notifications to developer endpoints.", enabled: false, status: "Architecture ready" },
];

export const categoryPreferences = [
  { label: "Security", description: "Sign-ins, keys, permissions, and sensitive account changes.", value: "Immediate" },
  { label: "Billing", description: "Plan, usage, invoices, and payment-related events.", value: "Daily digest" },
  { label: "Team activity", description: "Invites, members, roles, and workspace activity.", value: "Instant" },
  { label: "System updates", description: "Storage, workflow, developer, and platform events.", value: "Hourly digest" },
];

export const drawerNotifications = notifications.slice(0, 4);
export const notificationIcons = { Info };