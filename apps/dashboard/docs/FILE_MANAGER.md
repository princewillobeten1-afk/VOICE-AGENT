# File Manager UI Foundation

The VoiceSense file manager lives at `/storage` inside the workspace shell. It is a reusable operational surface for assets, upload sessions, folders, metadata, empty states, loading states, and provider error states.

## Layout

- Hero: storage purpose and primary actions.
- Summary stats: total assets, used storage, protected files, and active uploads.
- Toolbar: breadcrumbs, search, filter, sort, and view controls.
- Main content: upload drop zone, folder grid, and file table.
- Detail rail: selected file metadata, upload progress, and recent activity.
- State gallery: empty, loading, and provider error examples.

## Design Rules

- The page uses the permanent workspace shell and shared UI package.
- Mock data lives in `apps/dashboard/lib/storage-data.ts`.
- No real API calls or business logic are wired in Task 008.
- File operations are represented as reusable control patterns for future integration.
- The layout remains usable across desktop, tablet, and mobile breakpoints.

## Future Integration Points

- Replace mock data with React Query calls to `/v1/storage`.
- Add drag-and-drop upload controller with resumable upload support.
- Add real table selection, bulk action confirmation, and context menu operations.
- Add provider status, quota usage, retention policy controls, and audit event deep links.