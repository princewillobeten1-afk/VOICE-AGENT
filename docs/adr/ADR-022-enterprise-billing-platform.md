# ADR-022: Enterprise Billing, Usage Metering, and Subscription Platform

## Status

Accepted

## Context

VoiceSense needs monetization infrastructure that can support startups, agencies, and enterprise customers with subscriptions, usage metering, credits, quotas, invoices, discounts, enterprise contracts, payment providers, budget controls, and analytics. This must be independent from any single payment gateway.

## Decision

We will implement Billing as a provider-agnostic platform layer. VoiceSense will own plans, subscriptions, usage records, credit transactions, quotas, invoices, invoice line items, discounts, billing profiles, enterprise contracts, payment provider configs, payment methods, budget controls, and billing analytics.

Live payment processing, tax compliance integrations, financial accounting integrations, and marketplace revenue sharing are deferred. Provider adapters can later connect Stripe, Paddle, Lemon Squeezy, PayPal, and manual invoicing without changing billing domain logic.

## Consequences

- Plans, limits, credits, and quotas are configurable without code changes.
- Usage can be metered across voice, AI, workflow, tools, knowledge, APIs, storage, integrations, webhooks, messages, and phone numbers.
- Enterprise contracts and hybrid pricing models can be represented early.
- Billing can produce dashboards and forecasts before payment provider integration is live.