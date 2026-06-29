import logging

from app.metrics.prometheus import EVENTS_PROCESSED
from app.queue.events import EventType, QueueEvent
from app.services.diff_risk import analyze_pull_request
from app.services.flakiness import record_test_outcomes
from app.services.triage import analyze_workflow_run
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def handle_event(event: QueueEvent) -> None:
    db = SessionLocal()
    try:
        if event.type in (EventType.PR_OPENED, EventType.PR_SYNC):
            analyze_pull_request(db, event.payload)
        elif event.type == EventType.WORKFLOW_RUN:
            analyze_workflow_run(db, event.payload)
            record_test_outcomes(db, event.payload)
        EVENTS_PROCESSED.labels(event_type=event.type.value).inc()
    except Exception:
        logger.exception("Failed to process event %s", event.type)
        db.rollback()
        raise
    finally:
        db.close()
