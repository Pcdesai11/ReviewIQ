import hashlib
import hmac
import json
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request

from app.config import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
):
    body = await request.body()

    if settings.github_webhook_secret:
        if not x_hub_signature_256:
            raise HTTPException(status_code=401, detail="Missing signature")
        expected = "sha256=" + hmac.new(
            settings.github_webhook_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

    payload: dict[str, Any] = json.loads(body) if body else {}

    # Ingest only — analysis workers will consume from the queue later.
    return {
        "accepted": True,
        "event": x_github_event,
        "action": payload.get("action"),
        "message": "Webhook received; queued for processing (worker not yet implemented)",
    }
