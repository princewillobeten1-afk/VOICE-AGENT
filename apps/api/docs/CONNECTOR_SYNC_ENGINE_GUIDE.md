# Connector Sync Engine Guide

The sync engine supports initial, incremental, scheduled, manual, and retryable sync jobs.

`connector_sync_jobs` tracks status, cursor, conflict count, records processed, retries, timestamps, error state, and sync metadata. Future workers can execute real connector syncs behind the same table contract.