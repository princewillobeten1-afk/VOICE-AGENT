# Notification API

Base paths: `/v1/notifications` and `/v1/events`

## Notifications

- `GET /notifications` lists notifications with pagination, status, category, and search filters.
- `GET /notifications/unread-count` returns unread count for the current user.
- `PATCH /notifications/{notification_id}/read` marks one notification as read.
- `POST /notifications/read-all` marks all current user notifications as read.
- `POST /notifications/{notification_id}/archive` archives a notification.
- `DELETE /notifications/{notification_id}` soft deletes a notification.
- `GET /notifications/preferences` returns current user preferences.
- `PUT /notifications/preferences` updates current user preferences.
- `GET /notifications/settings` returns available channels, categories, frequencies, and realtime transports.

## Events

- `POST /events` publishes a domain event and runs current subscribers.
- `GET /events` lists organization events for audit-capable users.
- `GET /events/{event_id}/logs` lists subscriber processing logs for an event.

## Access Control

- Notification reads and mutations require organization read permission.
- Event publishing requires organization write permission.
- Event log listing requires audit read permission.