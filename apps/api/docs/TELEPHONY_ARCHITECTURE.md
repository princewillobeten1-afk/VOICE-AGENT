# Enterprise Telephony Architecture

Task 021 establishes VoiceSense telephony as the provider-independent call backbone above the Real-Time Voice Engine.

## Goals

- Support inbound and outbound PSTN, SIP, browser, and mobile call orchestration.
- Keep providers replaceable through workspace-scoped provider configuration.
- Connect calls to AI employees, conversations, workflows, storage, analytics, notifications, and AIOps.
- Model queues, routing, call lifecycle, events, recordings, and metrics without implementing provider account provisioning or billing.

## Layers

1. Provider configuration stores capability, priority, region, health, secret references, and failover policy.
2. Number and SIP inventory maps reachable addresses to queues, agents, and routing rules.
3. Routing selects destination, queue, fallback, and Voice Engine handoff metadata.
4. Call orchestration stores durable call state and timeline events.
5. Voice Engine owns real-time audio transport, STT, TTS, VAD, interruption, and stream events.
6. Conversation, workflow, tool, memory, and analytics systems consume call context through IDs and domain events.

## Boundary With Voice Engine

Telephony owns call setup, phone numbers, SIP endpoints, provider selection, queues, routing, call status, recording policy metadata, and call analytics. Voice Engine owns low-latency audio session runtime and provider-specific speech transport.

## Provider Strategy

Providers are data-driven. Twilio, Telnyx, Plivo, Vonage, SignalWire, Amazon Connect, Azure Communication Services, and custom SIP are catalog options. Runtime adapters should implement a common interface for webhook verification, inbound normalization, outbound dialing, media stream attachment, recording controls, DTMF, transfers, and hangup.