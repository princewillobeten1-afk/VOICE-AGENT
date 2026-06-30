# Conversation Engine Extension Guide

## Channel Adapters

Adapters should normalize inbound channel payloads into conversation turns. They should not own business state.

## Intent Providers

Future intent providers should return intent name, confidence, entities, and multi-intent candidates into `conversation_turns.intent` and `conversation_turns.entities`.

## Memory Hooks

Memory providers should read/write through explicit hook payloads. Task 014 stores references only.

## Workflow Hooks

Workflow engines should update `conversation_sessions.workflow_state`. Task 014 does not execute workflows.

## Human Handoff

Live agent systems should consume handoff events and conversation summaries, then update `handoff_status` when accepted or returned to AI.