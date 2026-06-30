# Knowledge Sync Architecture

Sync jobs prepare future connectors and crawlers.

Supported strategies:

- Manual sync
- Scheduled sync
- Incremental sync
- Full sync
- Conflict detection

Task 016A queues sync records only. Connector execution, crawling, and import workers are future tasks.