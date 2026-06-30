# Conversation State Management Guide

Conversation state lives at multiple levels.

## Conversation

Tracks channel, status, lifecycle stage, priority, topic, active intent, handoff status, summary, and external thread identifiers.

## Session

Tracks channel adapter state, current speaker, active turn, pending questions, tool state, workflow state, memory refs, and recovery state.

## Turn

Tracks speaker type, turn type, intent placeholder, entities, context delta, response plan, latency, interruption state, and message linkage.

State is designed to survive interruptions and session recovery.