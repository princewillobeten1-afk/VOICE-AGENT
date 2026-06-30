import { BarChart3, CheckCircle2, Clock3, FileText, Inbox, Mail, MessageCircle, Paperclip, Phone, RadioTower, Route, Send, ShieldCheck, Smartphone, Users, Workflow } from "lucide-react";

export const omniStats = [
  { label: "Active sessions", value: "1,284", detail: "11 channels", icon: Inbox, tone: "green" },
  { label: "Messages today", value: "48.2k", detail: "+18% vs yesterday", icon: Send, tone: "blue" },
  { label: "Delivery rate", value: "99.1%", detail: "p95 740 ms", icon: CheckCircle2, tone: "amber" },
  { label: "Identity matches", value: "92%", detail: "multi-signal", icon: Users, tone: "purple" },
];

export const channelCards = [
  { name: "Voice", provider: "Telephony Platform", status: "Operational", latency: "320 ms", icon: Phone },
  { name: "WhatsApp", provider: "Meta Business", status: "Operational", latency: "510 ms", icon: MessageCircle },
  { name: "Email", provider: "SendGrid", status: "Operational", latency: "1.8 s", icon: Mail },
  { name: "Web Chat", provider: "VoiceSense Widget", status: "Operational", latency: "88 ms", icon: RadioTower },
  { name: "SMS", provider: "Twilio", status: "Degraded", latency: "1.2 s", icon: Smartphone },
  { name: "Slack", provider: "Slack App", status: "Operational", latency: "440 ms", icon: Inbox },
];

export const customerTimeline = [
  { time: "09:12", channel: "Voice", title: "Inbound call resolved billing issue", detail: "Maya confirmed invoice status and captured follow-up preference.", icon: Phone },
  { time: "09:18", channel: "WhatsApp", title: "Continuation sent", detail: "Summary and payment link delivered on preferred channel.", icon: MessageCircle },
  { time: "09:24", channel: "Workflow", title: "Refund review workflow created", detail: "Policy check and manager approval branch prepared.", icon: Workflow },
  { time: "10:04", channel: "Email", title: "Email transcript delivered", detail: "Customer received full conversation summary and next steps.", icon: Mail },
];

export const sessions = [
  { customer: "Jordan Lee", channel: "WhatsApp", identity: "+1 415 010 2194", status: "Active", continuation: "Voice -> WhatsApp" },
  { customer: "Priya Shah", channel: "Email", identity: "priya@northstar.io", status: "Waiting", continuation: "Web Chat -> Email" },
  { customer: "Marcus Bell", channel: "SMS", identity: "crm_88241", status: "Active", continuation: "Email -> SMS" },
];

export const deliveryMetrics = [
  { label: "Sent", value: "48.2k", icon: Send },
  { label: "Delivered", value: "47.8k", icon: CheckCircle2 },
  { label: "Read", value: "31.4k", icon: Inbox },
  { label: "Failed", value: "412", icon: ShieldCheck },
];

export const readiness = [
  { label: "Formatter", value: "Capability-aware", icon: Route },
  { label: "Attachments", value: "Storage refs", icon: Paperclip },
  { label: "Identity", value: "Multi-signal", icon: Users },
  { label: "Analytics", value: "Channel metrics", icon: BarChart3 },
  { label: "Replay", value: "Timeline-ready", icon: Clock3 },
  { label: "Docs", value: "Extensible", icon: FileText },
];
