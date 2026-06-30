# Local Development Infrastructure

VoiceSense uses PostgreSQL for durable relational data and Redis for caches, rate limiting, queues, and future realtime coordination.

## Requirements

- Docker Desktop
- Node.js 22+
- Python 3.12+

## Start Services

From the repository root:

```bash
docker compose up -d postgres redis
```

PostgreSQL:

- Host: `db.cxhqhpwyeavxsygxppyp.supabase.co`
- Port: `5432`
- Database: `voicesense`
- User: `postgres`
- Password: `postgres`

Redis:

- Host: `localhost`
- Port: `6379`

## Environment

Create `.env` from `.env.example` and set:

```bash
DATABASE_URL=postgresql://postgres:%40%24papa%2C123..@db.cxhqhpwyeavxsygxppyp.supabase.co:5432/postgres
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=1L/beJUiCIfAJPX0OV2Ny49O2AKywYoQ3KCh4vNXtRVRYE19HoAPbOlFY9DquV2vOncEHrw9+C1+ipQg+mIp4g==
```

## Install API Dependencies

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

## Run Migrations

From `apps/api` with the virtual environment active:

```bash
python scripts/run_migrations.py
```

## Start API

```bash
uvicorn app.main:app --reload --port 8000
```

Open API docs:

```text
http://localhost:8000/docs
```

## Identity Smoke Test

With the API running:

```bash
python scripts/smoke_identity.py
```

The smoke test checks health, sign-up, and sign-in against the local API.