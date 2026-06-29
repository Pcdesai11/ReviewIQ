import logging
import time

from app.config import settings
from app.queue import dequeue
from app.workers.handlers import handle_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


def run() -> None:
    logger.info("ReviewIQ worker started (poll interval %.1fs)", settings.worker_poll_interval)
    while True:
        event = dequeue(timeout=int(settings.worker_poll_interval))
        if event:
            logger.info("Processing %s", event.type.value)
            handle_event(event)
        else:
            time.sleep(settings.worker_poll_interval)


if __name__ == "__main__":
    run()
