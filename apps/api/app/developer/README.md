# Developer Platform Backend

This module owns developer-facing platform primitives: API keys, PATs, OAuth app foundations, webhooks, API logs, usage summaries, SDK metadata, and developer settings.

Sensitive credentials are generated once, hashed before storage, and never returned again after creation.