# Workspace Shell Architecture

The VoiceSense workspace shell is the permanent layout foundation for authenticated product surfaces.

## Route Structure

Authenticated workspace pages should live inside the Next.js route group:

```text
apps/dashboard/app/(workspace)
```

The route group uses:

```text
apps/dashboard/app/(workspace)/layout.tsx
```

That layout renders `WorkspaceShell`, so future pages inherit the sidebar, top navigation, content area, and utility panel automatically.

Auth pages remain outside the workspace shell under:

```text
apps/dashboard/app/auth
```

The design system reference remains outside the workspace shell under:

```text
apps/dashboard/app/design-system
```

## Component Structure

```text
apps/dashboard/components/workspace/WorkspaceShell.tsx
apps/dashboard/components/workspace/DashboardHome.tsx
apps/dashboard/components/workspace/DashboardWidgets.tsx
apps/dashboard/lib/workspace-data.ts
```

## Shell Responsibilities

`WorkspaceShell` owns only application chrome:

- Left sidebar
- Organization switcher placeholder
- Workspace search shortcut
- Nested navigation
- Sidebar collapse/expand
- Mobile drawer behavior
- Top navigation
- Breadcrumbs
- Global search field
- Command trigger placeholder
- Notifications placeholder
- Theme toggle
- User menu placeholder
- Optional right utility panel

It should not own business logic or feature-specific state.

## Dashboard Responsibilities

`DashboardHome` composes reusable dashboard widgets with mock data only. It does not fetch APIs and does not implement AI functionality.

Reusable widgets include:

- Welcome card
- Statistic cards
- Usage overview
- Activity feed
- Quick actions
- System status
- Empty state gallery
- Loading preview
- Error preview

## Future Page Pattern

Create future pages inside `(workspace)`:

```text
apps/dashboard/app/(workspace)/employees/page.tsx
apps/dashboard/app/(workspace)/settings/page.tsx
apps/dashboard/app/(workspace)/developer/page.tsx
```

Each page should focus on its content. The workspace shell should remain stable.

## Accessibility

- The shell includes a skip link to the main content.
- Sidebar navigation uses semantic `nav` and active route state.
- Mobile navigation uses an overlay close button.
- Icon-only controls include `aria-label`.
- Focus indicators are inherited from design-system tokens.

## Performance

- Dashboard data is static mock data for fast initial render.
- Layout state is isolated to the client shell.
- Widgets are small reusable components to minimize unnecessary re-render scope.
- The right utility panel is optional and can be omitted on narrower layouts.