# Live Data Integration Layer

VoiceSense now uses a live integration path for the first dashboard surface: AI Employees.

## Runtime Flow

1. A user signs in or signs up through the dashboard auth pages.
2. The dashboard stores the access token, refresh token, organization id, and session marker.
3. The dashboard calls `POST /v1/workspaces/bootstrap-demo` when no active workspace exists.
4. The API creates a demo workspace, demo project, and seeded AI employees using the same domain models as production data.
5. The AI Employees page calls `GET /v1/ai-employees?workspace_id=...`.
6. The page opens `GET /v1/live/workspace-stream` to receive workspace summary events.

## Current Scope

Live-backed today:

- Sign in
- Sign up
- Demo workspace bootstrap
- AI employee roster
- AI employee summary counts
- Loading, empty, and error states for the AI Employees page
- Basic realtime workspace summary stream

Still placeholder-backed until their APIs are wired:

- Conversation counts
- Resolution rate
- Latency metrics
- Runtime events
- Channel coverage
- Evaluation suites

## Local Development

Run the API and dashboard together:

```powershell
docker compose up -d postgres redis
cd apps/api
.\.venv\Scripts\activate
python scripts\run_migrations.py
python -m uvicorn app.main:app --reload --port 8000
```

In another terminal:

```powershell
npm run dev
```

Open:

- Dashboard: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`

## Production Notes

The local SSE endpoint accepts `access_token` as a query parameter because native `EventSource` cannot send authorization headers. Before production, replace this with secure cookie-backed stream authentication or a short-lived stream token.
