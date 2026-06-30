# Workspace Components

This folder contains the reusable application shell and dashboard foundation for VoiceSense.

- `WorkspaceShell.tsx`: permanent app chrome for authenticated workspace pages.
- `DashboardHome.tsx`: dashboard composition using reusable widgets and mock data.
- `DashboardWidgets.tsx`: reusable dashboard widgets such as statistic cards, activity feed, quick actions, empty states, loading previews, and error states.

Future authenticated pages should render inside the `(workspace)` route group so they inherit the shell automatically.