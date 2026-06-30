# Retrieval Embedding Framework

VoiceSense keeps embeddings provider-agnostic. Embedding providers implement a common interface and return vector references instead of forcing the database to store vectors directly.

## Supported Future Providers

- OpenAI
- Cohere
- Google
- Voyage
- Jina
- Local embedding services

## Provider Configs

`retrieval_provider_configs` stores workspace-scoped provider metadata, capabilities, priority, model, dimensions, config, health state, and a `secret_ref`. Raw secrets must stay in a secrets manager.

## Interface Contract

An embedding provider accepts text plus provider config and returns token count, dimensions, provider name, model name, and vector reference. Production adapters may also return raw vectors to vector-store adapters, but raw vectors should not leak into API responses.

## Fallbacks

Provider priority allows fallback chains. If a primary embedding provider is unhealthy, workers can choose the next enabled provider with compatible dimensions.
