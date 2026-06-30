# ADR-018: Enterprise Telephony Infrastructure

## Status

Accepted

## Context

VoiceSense needs a telephony foundation that can support inbound and outbound calls, PSTN, SIP, browser/mobile call surfaces, number management, call routing, queues, recording metadata, and real-time monitoring. The platform must not become dependent on one vendor such as Twilio or Telnyx, and it must connect cleanly to the existing Voice Engine, Conversation Engine, Workflow Engine, AIOps, storage, and notification/event systems.

## Decision

We will implement Telephony as a provider-independent platform layer above the Real-Time Voice Engine.

Telephony owns provider configuration, phone number inventory, SIP endpoint metadata, routing rules, queue records, call lifecycle state, recording metadata, call events, and call metrics. Voice Engine owns low-latency audio streaming and speech runtime. Provider-specific behavior will be isolated behind future adapters configured by `telephony_provider_configs` and selected by priority, region, health, and failover metadata.

The initial implementation includes normalized database tables, REST APIs, domain-event publication for call lifecycle events, dashboard reference UI, and architecture/developer documentation. It intentionally excludes provider account provisioning, phone number purchasing, billing, and human workforce management.

## Consequences

- VoiceSense can support Twilio, Telnyx, Plivo, Vonage, SignalWire, Amazon Connect, Azure Communication Services, and custom SIP without changing product code paths.
- Calls become durable, auditable platform records that can connect to conversations, workflows, AI employees, voice sessions, recordings, and AIOps.
- Routing and queue policy can evolve into contact-center workflows while remaining AI-first.
- Provider integrations require future adapter contracts and webhook verification before production telephony traffic can be processed.

## Alternatives Considered

- Build directly on one telephony vendor. Rejected because it creates lock-in and weakens enterprise BYOC/custom SIP strategy.
- Put call control inside the Voice Engine. Rejected because call lifecycle, numbers, SIP, queues, routing, and recording policy have different scaling and compliance concerns than audio streaming.
- Delay telephony data modeling until provider integration. Rejected because routing, analytics, permissions, and dashboard foundations need stable contracts before provider-specific code arrives.