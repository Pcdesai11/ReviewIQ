import logging
from collections import deque
from threading import Lock

from app.config import settings
from app.queue.events import QueueEvent

logger = logging.getLogger(__name__)

QUEUE_KEY = "reviewiq:events"

_memory_queue: deque[str] = deque()
_memory_lock = Lock()
_redis_client = None
_redis_checked = False


def _get_redis():
    global _redis_client, _redis_checked
    if _redis_checked:
        return _redis_client
    _redis_checked = True
    try:
        import redis

        client = redis.from_url(settings.redis_url, decode_responses=True)
        client.ping()
        _redis_client = client
        logger.info("Connected to Redis at %s", settings.redis_url)
    except Exception as exc:
        logger.warning("Redis unavailable (%s) — using in-memory queue", exc)
        _redis_client = None
    return _redis_client


def enqueue(event: QueueEvent) -> None:
    raw = event.to_json()
    client = _get_redis()
    if client:
        client.rpush(QUEUE_KEY, raw)
    else:
        with _memory_lock:
            _memory_queue.append(raw)


def dequeue(timeout: int = 5) -> QueueEvent | None:
    client = _get_redis()
    if client:
        result = client.blpop(QUEUE_KEY, timeout=timeout)
        if not result:
            return None
        return QueueEvent.from_json(result[1])

    with _memory_lock:
        if not _memory_queue:
            return None
        return QueueEvent.from_json(_memory_queue.popleft())


def queue_depth() -> int:
    client = _get_redis()
    if client:
        return int(client.llen(QUEUE_KEY))
    with _memory_lock:
        return len(_memory_queue)
