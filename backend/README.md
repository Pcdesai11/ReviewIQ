# ReviewIQ — Backend

FastAPI Results API for ReviewIQ. See [`# ReviewIQ.ini`](../#%20ReviewIQ.ini) in the repo root.

## Quick start

```bash
# From repo root — start Postgres + Redis (optional; SQLite works for local dev)
docker compose up -d

# Backend setup
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
copy .env.example .env          # Windows — uses SQLite by default
# cp .env.example .env

alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000/docs** for interactive API docs.

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /v1/metrics/summary` | Dashboard portfolio stats |
| `GET /v1/pulls` | All open PRs, sorted by risk |
| `GET /v1/pulls/{id}/risk` | Single PR risk score + rationale |
| `GET /v1/tests/flaky` | Flaky test watch list |
| `GET /v1/ci-runs/triage` | CI triage queue |
| `GET /v1/ci-runs/{id}/triage` | Single CI run triage |
| `POST /webhooks/github` | GitHub webhook ingest (stub) |
| `GET /health` | Health check |

## What's next

- [ ] Redis queue + workers (diff risk, flakiness, triage)
- [ ] LLM provider layer
- [ ] Wire frontend to Results API (replace `mockData.ts`)
- [ ] Prometheus metrics
