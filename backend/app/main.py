from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.api.webhooks.github import router as github_webhook_router
from app.config import settings
from app.schemas.results import HealthOut

app = FastAPI(
    title=settings.app_name,
    description="Results API for the ReviewIQ dashboard — PR risk, flaky tests, CI triage.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
app.include_router(github_webhook_router)


@app.get("/health", response_model=HealthOut, tags=["health"])
def health():
    return HealthOut(status="ok", timestamp=datetime.now(timezone.utc))
