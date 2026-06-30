# Telephony Queue Guide

Call queues provide the future contact-center foundation without building a human agent desktop in Task 021.

## Queue Records

`call_queues` stores name, slug, priority, assignment policy, overflow policy, estimated wait, status, and analytics state.

## Assignment Policy

Assignment can later route to AI employees by skill, workload, language, department, SLA, or supervisor policy.

## Overflow Policy

Overflow can route to another AI employee, voicemail, workflow, external number, or a future human team.

## Metrics

Queue wait time, abandon rate, overflow count, transfer count, and AI resolution rate should flow into AIOps through `call_metrics` and operational metrics.