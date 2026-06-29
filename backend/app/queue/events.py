from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventType(str, Enum):
    PR_OPENED = "pr.opened"
    PR_SYNC = "pr.sync"
    WORKFLOW_RUN = "workflow_run"


class QueueEvent(BaseModel):
    type: EventType
    payload: dict[str, Any]
    received_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_json(cls, raw: str) -> "QueueEvent":
        return cls.model_validate_json(raw)
