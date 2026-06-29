# ReviewIQ

AI-powered code review & CI triage. See [`# ReviewIQ.ini`](./#%20ReviewIQ.ini) for the full spec.

## Project layout

```
ReviewIQ/
├── backend/     # FastAPI Results API
├── frontend/    # React dashboard
└── docker-compose.yml
```

## Quick start

```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8001

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

- Dashboard: http://localhost:5173  
- API docs: http://127.0.0.1:8001/docs  

## Deploy backend on Render

The repo includes a [`render.yaml`](./render.yaml) blueprint that provisions:

| Service | Role |
|---|---|
| `reviewiq-api` | FastAPI web service |
| `reviewiq-worker` | Background worker (`python -m app.workers.runner`) |
| `reviewiq-db` | Managed PostgreSQL |
| `reviewiq-redis` | Redis-compatible queue (Key Value) |

### Steps

1. Push this repo to GitHub (if not already).
2. In [Render](https://dashboard.render.com/) → **Blueprints** → **New Blueprint Instance** → connect the repo.
3. Click **Deploy Blueprint** (creates all four resources).
4. After deploy, open **reviewiq-api** → **Environment** and set:
   - `LLM_API_KEY` — your OpenAI (or other provider) key
   - `GITHUB_TOKEN` — PAT with `repo` scope (read diffs, post comments)
   - `GITHUB_WEBHOOK_SECRET` — same secret you will use in GitHub webhook settings
   - `CORS_ORIGINS` — your Vercel frontend URL, e.g. `https://reviewiq.vercel.app`
5. Copy the **reviewiq-api** public URL (e.g. `https://reviewiq-api.onrender.com`).
6. In Vercel → project **Environment Variables** → set `VITE_API_URL` to that URL and redeploy.
7. In GitHub → repo **Settings → Webhooks** → add webhook:
   - **Payload URL:** `https://<reviewiq-api-url>/webhooks/github`
   - **Secret:** your `GITHUB_WEBHOOK_SECRET`
   - **Events:** Pull requests, Workflow runs

Verify: `GET https://<reviewiq-api-url>/health` should return `{"status":"ok",...}`.

> **Note:** Starter plans avoid free-tier sleep limits on workers. The worker must stay running for PR/CI analysis to process.
