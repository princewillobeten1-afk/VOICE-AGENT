# SDK Architecture

Official VoiceSense SDKs should be generated from the public OpenAPI contract where possible, then wrapped with ergonomic helpers.

## Required SDK Capabilities

- API key authentication.
- Request ID propagation.
- Typed error handling.
- Pagination helpers.
- Webhook signature verification.
- Retry policy with exponential backoff.
- Timeout configuration.
- Environment support.

## Package Names

- TypeScript: `@voicesense/sdk`
- Node.js: `voicesense`
- Python: `voicesense`
- Go: `github.com/voicesense/voicesense-go`
- Java: `com.voicesense`
- PHP: `voicesense/voicesense-php`

## Versioning

SDK major versions track API major versions. `/v1` APIs map to SDK `1.x`.