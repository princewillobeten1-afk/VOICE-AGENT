# Database Schema Foundation

VoiceSense uses PostgreSQL with UUID primary keys, normalized tenant relationships, explicit foreign keys, soft deletes where records represent user-managed resources, and indexes designed for high-volume organization-scoped access.

## Standards

Every major entity should use:

- `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `organization_id` for tenant isolation where applicable
- `workspace_id` for product workspace isolation where applicable
- `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `deleted_at TIMESTAMPTZ` for soft-deletable resources
- `created_by_user_id` and `updated_by_user_id` where user ownership matters

## Core Tables

Identity:

- `users`
- `organizations`
- `memberships`
- `teams`
- `team_members`
- `roles`
- `invitations`
- `sessions`
- `oauth_accounts`
- `verification_tokens`

Platform:

- `workspaces`
- `projects`
- `agents`
- `agent_versions`
- `voices`
- `prompts`
- `knowledge_bases`
- `data_sources`
- `documents`
- `embedding_placeholders`
- `conversations`
- `messages`
- `calls`
- `call_events`
- `workflows`
- `workflow_runs`
- `automation_events`
- `external_integrations`
- `connected_accounts`
- `api_keys`
- `webhook_endpoints`
- `files`
- `uploads`
- `usage_records`
- `analytics_events`
- `metric_snapshots`
- `billing_accounts`
- `subscription_placeholders`
- `notifications`
- `notification_preferences`
- `security_events`
- `domain_event_records`

## Scaling Notes

- Conversation, message, call event, analytics, and usage tables are expected to become high-volume tables.
- Query paths should include `organization_id`, `workspace_id`, and time/status indexes.
- Future partitioning candidates: `messages`, `call_events`, `usage_records`, `analytics_events`, `domain_event_records`.
- Embeddings intentionally use a placeholder table with `vector_ref` so vector storage can move to pgvector, Pinecone, Weaviate, or another provider later.

## Task 009 Notification and Event System

- domain_event_records: durable event store with versioning, correlation, causation, status, retry, and payload metadata.
- event_subscribers: event consumer registry.
- event_logs: per-subscriber processing outcomes and latency.
- 
otifications: in-app user notification records with category, severity, status, read/archive/delete lifecycle.
- 
otification_preferences: user channel, frequency, quiet-hours, category, and team notification preferences.
- 
otification_channels: future channel configuration for email, SMS, push, WhatsApp, Slack, Discord, and webhooks.
- 
otification_templates: reusable event-to-message templates with variables.
- delivery_attempts: delivery status, retry, latency, and provider tracking.


## Task 010 Universal Integration Framework

- integration_categories: marketplace category taxonomy.
- external_integrations: provider marketplace records with auth methods, capabilities, compatibility, versioning, and status.
- connector_definitions: connector interface metadata, handler references, retry/rate-limit policy, and health configuration.
- connected_accounts: organization/workspace installed connections.
- integration_credentials: secret references, fingerprints, rotation, expiry, and status metadata.
- integration_action_definitions: dynamic action contracts.
- integration_trigger_definitions: dynamic trigger contracts.
- connection_logs: lifecycle, action, trigger, and credential events.
- integration_health_checks: connection health history.


## Task 011 Future AI Data Model Considerations

Task 011 does not add tables. Future AI implementation tasks should consider models for ai_provider_configs, ai_sessions, ai_traces, prompt_versions, prompt_tests, context_snapshots, memory_entries, memory_retrievals, tool_registry_entries, tool_executions, ai_employee_collaborations, ai_response_evaluations, and provider_usage_records.


## Task 012 AI Employee Builder

- agents: AI employee identity, role, lifecycle, status, template reference, and publishing metadata.
- agent_versions: versioned instructions and configuration for personality, voice, knowledge, memory, channels, collaboration, model, tools, and workflows.
- agent_configurations: builder progress, readiness checks, and playground state.
- agent_templates: reusable employee templates.
- agent_drafts: resumable draft payloads.
- agent_publishing_history: publishing, duplication, archival, and lifecycle audit history.


## Task 013 Real-Time Voice Engine

- voice_provider_settings: Workspace-scoped provider configuration, capabilities, health, priority, and secret references for STT, TTS, VAD, and transports.
- voice_configurations: Agent or workspace voice settings including language, models, voice identity, streaming mode, VAD, interruption policy, latency budget, and fallback chain.
- voice_sessions: Long-running live session state for channel, transport, speaker, active response, context snapshot, pending tool calls, interruption count, timeout, and termination.
- voice_session_metrics: Per-stage latency, provider, and quality metrics.
- voice_audio_metadata: Metadata-only audio records by default, with optional file reference for future explicit recording policies.
- voice_stream_events: Ordered stream lifecycle events for audio chunks, VAD, STT, interruption, playback, session recovery, and termination.

## Task 014 Universal Conversation Engine

- conversations: Existing aggregate root extended with lifecycle stage, priority, topic, active intent, customer references, thread references, handoff status, and summary.
- conversation_sessions: Channel-independent session state, adapter metadata, current speaker, active intent, pending questions, tool/workflow state, memory refs, recovery state, and expiration.
- conversation_turns: Normalized user, AI, system, interruption, clarification, and follow-up turns with intent/entity placeholders and response plans.
- conversation_goals: Objective tracking with success criteria, progress, priority, and completion state.
- conversation_context_snapshots: Dynamic context assembly records with source priority, omissions, token budgets, and model limits.
- conversation_engine_events: Ordered lifecycle and processing events for auditing and event-system integration.
- conversation_analytics: Duration, turn count, response time, completion, escalation, goal, sentiment, and satisfaction placeholders.

## Task 015 Advanced Memory System

- memory_categories: Extensible category taxonomy with default privacy and retention hints.
- memory_policies: Workspace-scoped retention, expiration, cleanup, size, and privacy policies.
- memories: Layered AI employee memory records for short-term, working, long-term, episodic, semantic, organizational, shared, and session memory.
- memory_versions: Version history and change tracking for important memory updates.
- memory_links: Related, merged, duplicate, causal, and handoff relationships between memories.
- memory_access: Principal-based access grants for users, agents, teams, roles, and shared scopes.
- memory_events: Audit and observability events for create, retrieve, update, archive, forget, merge, and delete actions.
- memory_statistics: Memory growth, retrieval, storage, expiration, and cache metrics foundation.

## Task 016A Enterprise Knowledge Management Platform

- knowledge_bases: CMS repositories extended with owner, visibility, status, permissions, statistics, and publishing metadata.
- data_sources: Source registry extended with provider, health, sync configuration, credential reference, and sync timestamps.
- documents: Content assets extended with folder/category, source kind, validation, freshness, publishing, duplicate detection, metadata, and version pointers.
- knowledge_categories, knowledge_tags, knowledge_folders, knowledge_collections: Flexible organization system.
- website_sources: Website registration and crawl configuration without crawler execution.
- knowledge_faqs: FAQ content management records.
- document_versions: Version history and publishing records.
- knowledge_permissions: Principal-based access grants for knowledge bases and documents.
- knowledge_sync_jobs: Manual, scheduled, incremental, full, and conflict-aware sync job foundation.
- knowledge_activity_logs and knowledge_quality_checks: Governance, audit, validation, duplicate, freshness, and health tracking.
## Task 016B Enterprise RAG and Intelligent Retrieval Engine

- retrieval_provider_configs: Workspace-scoped embedding, vector store, and reranker provider configuration with priority, capabilities, health, and secret references.
- retrieval_settings: Chunking, provider references, hybrid weights, token budgets, metadata filters, cache policy, and permission mode.
- retrieval_indexes: Index registry for knowledge bases with provider metadata, document counts, chunk counts, and freshness.
- retrieval_chunks: Chunk metadata, source document links, token counts, embedding state, vector references, checksums, and status.
- embedding_jobs: Indexing and reindexing job records with provider, model, progress, timestamps, and error state.
- retrieval_requests: Search and context assembly traces with query, filters, weights, latency, token budget, and permission summary.
- search_logs: Stage-level retrieval logs for candidate search, reranking, context assembly, and diagnostics.
- retrieval_metrics: Workspace and knowledge-base retrieval metrics for future quality, latency, usage, and cost analytics.

## Task 017 Enterprise Visual Workflow Automation Engine

- workflows: Existing workflow aggregate extended with category, trigger, execution mode, canvas state, settings, version pointer, publication, and run counters.
- workflow_versions: Draft, published, rollback-ready snapshots of workflow definitions and canvas state.
- workflow_nodes: Visual graph node records with type, position, config, schemas, retry policy, timeout, and status.
- workflow_connections: Visual graph edges with handles, labels, and conditional expressions.
- workflow_runs: Durable execution records extended with trigger metadata, current node, pause/resume state, variables, retry count, duration, and execution state.
- workflow_execution_logs: Node-level execution traces, input/output snapshots, latency, retry, and diagnostic metadata.
- workflow_variables: Workflow/global/temp/environment/secret variable records with redacted secret handling.
- workflow_templates: Reusable template definitions and canvas state.
- workflow_schedules: Schedule metadata for future queue workers.
- workflow_approval_requests: Human-in-the-loop approval, assignment, comments, decisions, and resume state.

## Task 018 Universal Tool Calling and MCP Framework

- tool_categories: Workspace-scoped tool category taxonomy.
- tool_definitions: Registry records for internal, external, integration, workflow, developer, custom, and future MCP-backed tools.
- tool_versions: Versioned schemas and runtime configuration.
- tool_permissions: Principal-based allow/deny rules for discovery, execution, and management.
- tool_credentials: Secret references and connected-account links for tool authentication.
- tool_executions: Durable runtime execution records with validation, permission, latency, retry, cost, output, and error state.
- tool_execution_logs: Stage-level logs for request, guardrails, execution, result, and failure events.
- tool_health_metrics: Usage, success, failure, latency, retry, cost, and health metrics.
- mcp_server_definitions: Placeholder registry for future MCP server transport, session, tool, resource, and prompt discovery.

## Task 019 Multi-Agent Collaboration Engine

- ai_roles: Configurable AI employee roles, responsibilities, permissions, and metadata.
- ai_teams: AI departments, nested teams, supervisors, responsibilities, routing policy, and collaboration rules.
- ai_team_members: AI employee team assignment, membership type, role, availability, workload, and responsibilities.
- collaboration_policies: Delegation depth, allowed delegation paths, approvals, escalations, and department restrictions.
- collaboration_sessions: Shared objective, conversation/workflow links, supervisor, priority, shared state, and success criteria.
- delegation_events: Source and target agents, routing confidence, task payload, delegation depth, status, and due dates.
- shared_contexts: Shared conversation, objective, variables, customer data, and workflow state records.
- shared_memory_refs: Permission-aware references to Memory System facts, notes, decisions, and task history.
- collaboration_messages: Internal communication bus for direct messages, broadcasts, task requests, and status updates.
- collaboration_logs: Traceable collaboration timeline events.
- collaboration_metrics: Delegation, success, utilization, resolution, workload, and escalation metrics.

## Task 020 AI Operations Center Observability and Analytics Platform

- ops_dashboards: Saved personal and organization dashboard layouts, widgets, and filters.
- ops_metrics: High-volume operational metrics across platform components.
- ops_alerts and ops_alert_events: Configurable alert rules and triggered incidents.
- ops_health_reports: Component health scores, checks, incidents, and historical status.
- ops_cost_records: LLM, STT, TTS, embedding, vector, tool, workflow, and infrastructure cost telemetry.
- ops_evaluation_results: AI quality evaluation results for goal completion, instruction following, hallucination checks, knowledge accuracy, and human review.

## Task 021 Enterprise Telephony Infrastructure

- telephony_provider_configs: Workspace-scoped telephony provider settings, capabilities, health, priority, secret references, and failover policy.
- phone_numbers: E.164 number inventory with provider, route, agent, queue, compliance, and metadata references.
- sip_endpoints: SIP trunk, domain, peer, auth, allowed IP, header, and routing metadata.
- call_queues: AI-first queue records with assignment, overflow, wait, status, and analytics metadata.
- call_routing_rules: Priority-based routing conditions, destinations, business hours, and failover configuration.
- telephony_calls: Durable call aggregate linked to providers, numbers, queues, voice sessions, conversations, workflows, and AI employees.
- telephony_call_events: Ordered call lifecycle timeline events.
- call_recordings: Metadata, storage object reference, retention, and access policy records for future recording runtime.
- call_metrics: Call, provider, queue, latency, duration, quality, and cost metric foundation.

## Task 022 Omnichannel Communication Platform

- channel_configurations: Provider-agnostic channel settings, capabilities, formatter policy, credentials references, and health state.
- customer_identities: Multi-signal identity records for phone, email, CRM, external, provider, and workspace identifiers.
- channel_sessions: Channel-specific threads linked to unified conversations, customers, agents, context, and workflow state.
- omnichannel_messages: Normalized inbound and outbound messages across all supported channels.
- message_attachments: Storage-backed attachment metadata, scan state, and access policy records.
- delivery_events: Provider-independent delivery, read, retry, failure, and expiration events.
- customer_timeline_events: Chronological cross-channel customer journey replay events.
- channel_analytics: Channel performance, delivery, engagement, response time, and continuation metrics.


## Task 023 Enterprise Integration Platform

- connector_versions: Draft, published, deprecated, rollback, SDK contract, changelog, and migration metadata.
- connector_installations: Workspace installation lifecycle, permission review, configuration wizard state, and health summary.
- connector_sync_jobs: Initial, incremental, scheduled, manual, retry, conflict, cursor, and status tracking.
- connector_marketplace_metadata: Listing status, developer metadata, ratings framework, downloads, installs, docs, screenshots, and dependency maps.
- connector_playground_runs: Simulated action, trigger, event, sync, and auth tests for administrators and developers.
- connector_analytics_records: Connector usage, failure, sync volume, install, active organization, and auth failure metrics.


## Task 024 Enterprise Developer Platform

- api_versions: Stable, beta, deprecation, sunset, migration, OpenAPI, and release metadata.
- oauth_access_tokens: OAuth token and refresh-token hashes with scopes, expiry, status, and revocation.
- rate_limit_policies: Organization, API key, endpoint, burst, quota, and environment rate-limit policy records.
- sandbox_resources: Test organizations, AI employees, mock conversations, fake phone numbers, mock events, and sample fixtures.
- api_explorer_runs: Executed explorer requests with headers, body, response, latency, timeline, and generated code samples.
- cli_releases: CLI version, install command, command surface, changelog, and metadata.
- sdk_releases: SDK language, package, version, OpenAPI compatibility, install command, docs, and generation metadata.


## Task 025 Enterprise Billing Platform

- subscription_plans: Configurable plan catalog with features, limits, credits, support level, and pricing metadata.
- subscriptions: Organization subscription lifecycle, periods, trials, provider refs, and contract refs.
- billing_usage_records: Metered billing usage across voice, AI, API, workflow, tools, storage, integrations, messages, and phone numbers.
- credit_transactions: Append-only credit ledger with balance-after tracking and expiration.
- billing_quotas: Hard/soft limits, warning thresholds, grace policies, and current usage.
- invoices and invoice_line_items: Invoice metadata, totals, PDF refs, line items, credits, discounts, tax placeholder, and payment state.
- discounts: Coupon, promotion, enterprise pricing, and trial-extension rule framework.
- billing_profiles: Billing contacts, address, tax metadata, and invoice preferences.
- enterprise_contracts: Seat, usage, flat-rate, hybrid, and custom contract metadata.
- payment_provider_configs and payment_methods: Provider-agnostic payment framework and tokenized payment method refs.
- budget_controls and billing_analytics_records: Budget caps, forecasts, MRR, ARR, credit consumption, and revenue metrics.

## Task 026 Enterprise Security, Administration, Compliance, and Governance Platform

- admin_departments: Organization administration hierarchy and department metadata.
- user_groups and user_group_members: Enterprise user grouping for future delegated administration and policy targeting.
- custom_roles: Organization-specific RBAC bundles with permission and constraint metadata.
- governance_policies: Organization and workspace policy records with monitor/enforce modes.
- abac_policies: Attribute-based access rules by resource, action, conditions, priority, and effect.
- sso_connections: Provider-agnostic OIDC/SAML connection metadata and secret references.
- mfa_factors and trusted_devices: MFA enrollment and device trust foundations.
- secret_records and secret_versions: Versioned secret-reference registry for rotation and compliance checks.
- compliance_frameworks and compliance_evidence: Readiness, controls, evidence, and file-linked artifacts.
- data_governance_policies: Retention, residency, classification, legal hold, and rules metadata.
- encryption_key_records: KMS/HSM/provider key references and rotation policy metadata.
- security_risk_events: Risk signals, levels, scores, status, and mitigation state.
- security_health_scores: Periodic organization security posture scoring.
- governance_graph_snapshots: Cross-platform relationship snapshots for future governance analytics.
## Task 027 VoiceSense AI Studio

- ai_studio_prompts: Workspace prompt artifacts linked to optional AI employees.
- ai_studio_prompt_versions: Draft, published, archived, rollback-ready prompt versions with variables, guardrails, token estimates, validation state, and release notes.
- ai_studio_prompt_templates: Organization prompt template libraries by category.
- ai_studio_playground_runs: Recorded text/voice playground attempts and execution traces.
- ai_studio_simulation_scenarios: Reusable personas, scripts, assertions, edge cases, and escalation scenarios.
- ai_studio_evaluation_metrics and ai_studio_evaluation_runs: Extensible scoring framework, regression summaries, latency, and cost telemetry.
- ai_studio_test_suites, ai_studio_test_cases, and ai_studio_test_runs: Batchable tests, assertions, schedules, and deployment gates.
- ai_studio_benchmarks and ai_studio_experiments: Baseline comparison and A/B experiment foundations.
- ai_studio_deployments: Environment-based prompt deployment, approval, rollout, and rollback metadata.
- ai_studio_comments and ai_studio_activity_logs: Collaboration, reviews, approvals, mentions, and activity timelines.
- ai_studio_analytics_records, ai_studio_interaction_timelines, and ai_studio_replay_sessions: Prompt performance, AI timeline, and replay inspection foundations.