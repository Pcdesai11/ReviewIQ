import hashlib
import hmac
import json
import logging
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request

from app.config import settings
from app.queue import EventType, QueueEvent, enqueue

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def _enqueue(event_type: EventType, payload: dict[str, Any]) -> None:
    enqueue(QueueEvent(type=event_type, payload=payload))


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
    event_name = x_github_event or "unknown"
    action = payload.get("action")
    queued: list[str] = []

    if event_name == "pull_request" and action in ("opened", "synchronize", "reopened"):
        event_type = EventType.PR_OPENED if action == "opened" else EventType.PR_SYNC
        _enqueue(event_type, payload)
        queued.append(event_type.value)

    elif event_name == "workflow_run" and action == "completed":
        _enqueue(EventType.WORKFLOW_RUN, payload)
        queued.append(EventType.WORKFLOW_RUN.value)

    return {
        "accepted": True,
        "event": event_name,
        "action": action,
        "queued": queued,
        "message": "Events enqueued for worker processing" if queued else "Event acknowledged (no action)",
    }
