# AI Provider Abstraction Guide

VoiceSense must never depend on one model provider. The provider abstraction isolates business logic from LLM, embedding, speech-to-text, text-to-speech, and local model vendors.

## Supported Future Providers

- OpenAI
- Anthropic
- Google Gemini
- Grok
- DeepSeek
- Mistral
- Local models
- Future enterprise-hosted models

## Provider-Neutral Contracts

Provider adapters should expose normalized contracts for:

- Chat or reasoning requests
- Streaming responses
- Tool-call capable responses
- Embeddings
- Speech-to-text
- Text-to-speech
- Model capability discovery
- Usage and cost reporting
- Health and failover checks

## Provider Manager Responsibilities

- Resolve provider based on AI employee configuration.
- Enforce organization policy and allowed providers.
- Select fallback providers when latency or failures exceed policy.
- Normalize request and response formats.
- Track token usage, audio duration, latency, and estimated cost.
- Hide provider-specific SDK details from orchestration code.

## Model Capability Matrix

Future provider records should expose:

- Context window
- Streaming support
- Tool calling support
- JSON/schema output support
- Vision/audio support
- Latency tier
- Cost tier
- Data retention policy
- Region availability
- Enterprise compliance metadata

## Failover Policy

Provider failover should be explicit and auditable:

1. Check model availability and organization policy.
2. Attempt primary provider.
3. Retry according to provider-safe policy.
4. Fall back to compatible model if configured.
5. Emit `ai.provider.failed` and `ai.provider.fallback_used`.
6. Preserve trace details for debugging and cost analysis.

## Business Logic Rule

No business module should import provider SDKs. All model calls must go through the Provider Manager.