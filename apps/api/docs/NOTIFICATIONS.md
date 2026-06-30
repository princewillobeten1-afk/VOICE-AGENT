# Notification System

VoiceSense notifications are generated from domain events. Product modules should emit events and avoid directly creating notifications unless there is a clear user-facing notification-only workflow.

## Notification Channels

Implemented now:

- In-app notifications

Architecture-ready or placeholders:

- Email
- SMS
- Push
- WhatsApp
- Slack
- Discord
- Webhooks

## Lifecycle

1. Event is published.
2. Notification subscriber receives the event.
3. Template is resolved from `notification_templates` or default event templates.
4. In-app notification is written to `notifications`.
5. Delivery result is written to `delivery_attempts`.
6. User can mark as read, archive, or delete.

## Preferences

`notification_preferences` stores user-level policy for:

- Email enabled
- In-app enabled
- Future channel toggles
- Frequency
- Quiet hours
- Category preferences
- Team notifications

## Templates

Templates support variable replacement using `{{variable_name}}`. Standard variables include:

- `user_name`
- `organization_name`
- `agent_name`
- `timestamp`
- `action_details`

## Security

Notification APIs enforce organization membership and tenant isolation. Users can only read and mutate their own notifications in the active organization.