# AI Employee Configuration Guide

AI employee configuration is split across stable identity data and versioned operating data.

## Agent Identity

Stored on `agents`:

- Name
- Display name
- Avatar
- Role
- Department
- Category
- Description
- Lifecycle state
- Template reference

## Versioned Configuration

Stored on `agent_versions`:

- Instructions
- Personality config
- Voice config
- Knowledge config
- Memory config
- Channel config
- Collaboration config
- Model config
- Tool config
- Workflow config
- Validation state

## Builder Configuration

Stored on `agent_configurations`:

- Builder progress
- Readiness checks
- Playground state