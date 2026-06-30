import { BadgeDollarSign, BarChart3, CalendarClock, CircleDollarSign, CreditCard, DatabaseZap, FileText, Gauge, KeyRound, LineChart, Phone, ReceiptText, ShieldCheck, Sparkles, Wallet, Workflow } from "lucide-react";

export const billingStats = [
  { label: "MRR", value: "$48.6k", detail: "+12.4% MoM", icon: CircleDollarSign, tone: "green" },
  { label: "Usage spend", value: "$7.8k", detail: "forecast $9.2k", icon: LineChart, tone: "blue" },
  { label: "Credits", value: "184k", detail: "42k expiring", icon: Wallet, tone: "amber" },
  { label: "Invoices", value: "99.1%", detail: "payment success", icon: ReceiptText, tone: "purple" },
];

export const usageMeters = [
  { name: "Voice minutes", value: "18.4k", limit: "30k", progress: 61, icon: Phone },
  { name: "AI conversations", value: "42.8k", limit: "75k", progress: 57, icon: Sparkles },
  { name: "API requests", value: "1.2M", limit: "1.5M", progress: 80, icon: DatabaseZap },
  { name: "Workflow runs", value: "86k", limit: "150k", progress: 58, icon: Workflow },
];

export const invoices = [
  { number: "INV-2026-006", status: "Paid", amount: "$12,840", issued: "Jun 1", due: "Jun 15" },
  { number: "INV-2026-007", status: "Open", amount: "$13,920", issued: "Jul 1", due: "Jul 15" },
  { number: "INV-ENT-102", status: "Draft", amount: "$84,000", issued: "Annual", due: "Manual" },
];

export const creditLedger = [
  { type: "Monthly allocation", amount: "+120,000", balance: "220,000", scope: "All services" },
  { type: "Voice usage", amount: "-18,420", balance: "201,580", scope: "Voice" },
  { type: "Promotion", amount: "+25,000", balance: "226,580", scope: "AI" },
];

export const costBreakdown = [
  { label: "AI Employees", value: "$3,420", icon: Sparkles },
  { label: "Voice/STT/TTS", value: "$2,880", icon: Phone },
  { label: "Workflows", value: "$920", icon: Workflow },
  { label: "Knowledge", value: "$640", icon: FileText },
  { label: "Integrations", value: "$410", icon: KeyRound },
  { label: "Storage", value: "$260", icon: DatabaseZap },
];

export const planFeatures = ["75 AI employees", "30k voice minutes", "1.5M API requests", "Premium support", "Custom quotas", "Enterprise SSO ready"];
export const providerReadiness = ["Stripe", "Paddle", "Lemon Squeezy", "PayPal", "Manual invoicing"];
export const billingReadiness = [
  { label: "Tax framework", value: "Modeled", icon: ShieldCheck },
  { label: "PDF invoices", value: "Storage-ready", icon: FileText },
  { label: "Budget controls", value: "Forecasting", icon: Gauge },
  { label: "Contracts", value: "Hybrid pricing", icon: BadgeDollarSign },
  { label: "Renewals", value: "Lifecycle", icon: CalendarClock },
  { label: "Analytics", value: "MRR / ARR", icon: BarChart3 },
];