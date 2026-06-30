# ADR-019: Omnichannel Communication Platform

## Status

Accepted

## Context

VoiceSense needs one AI employee experience across voice calls, WhatsApp, SMS, email, web chat, Slack, Microsoft Teams, Telegram, Facebook Messenger, Instagram Messaging, mobile SDK messaging, and future channels. Customers must be recognized across channels, and conversation context must survive channel switching.

## Decision

We will implement Omnichannel as a provider-independent communication layer with channel configuration, normalized sessions, unified customer identity, normalized messages, attachment references, provider-independent delivery events, customer timeline events, and channel analytics.

Channel adapters normalize provider payloads before messages reach AI employees. The Conversation Engine, Memory System, Knowledge Engine, Workflow Engine, Tool Runtime, and AI Employee layers consume normalized context rather than provider-specific payloads. Outbound responses pass through a formatter that adapts rich content to channel capabilities.

## Consequences

- AI employees can operate consistently across every supported channel.
- Customer timeline replay becomes a first-class product primitive.
- Provider switching is isolated to adapters and channel configuration.
- Future smart channel selection can use preference, urgency, cost, availability, and provider health.
- Production provider credentials, messaging billing, human live chat, and marketing campaign automation remain outside this task.

## Alternatives Considered

- Build separate inboxes per channel. Rejected because it fragments customer context and weakens AI employee continuity.
- Put channel-specific logic inside AI employees. Rejected because it creates coupling and makes future providers expensive to add.
- Store provider raw payloads only. Rejected because analytics, search, replay, and workflow continuation require normalized records.