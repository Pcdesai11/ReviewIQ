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
