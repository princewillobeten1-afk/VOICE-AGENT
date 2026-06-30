# Workflow Variable Guide

Variables are stored in `workflow_variables` and can also be carried per run in `workflow_runs.variables`.

## Scopes

- Workflow variables
- Global variables
- Temporary variables
- Environment variables
- Secret variables

Secret variables should store only `secret_ref`. Raw secret values must never be returned in API responses.

## Expressions

The foundation supports safe interpolation with `{{ input.field }}`, `{{ variables.name }}`, and similar dotted paths. Future expression support can add math, date operations, JSON access, conditionals, and function calls through a sandboxed evaluator.
