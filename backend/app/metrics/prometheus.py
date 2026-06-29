from prometheus_client import Counter, Histogram

WEBHOOKS_RECEIVED = Counter(
    "reviewiq_webhooks_received_total",
    "GitHub webhooks received",
    ["event"],
)

EVENTS_ENQUEUED = Counter(
    "reviewiq_events_enqueued_total",
    "Events enqueued for processing",
    ["event_type"],
)

EVENTS_PROCESSED = Counter(
    "reviewiq_events_processed_total",
    "Events processed by workers",
    ["event_type"],
)

ANALYSES_COMPLETED = Counter(
    "reviewiq_analyses_completed_total",
    "Analysis jobs completed",
    ["analysis_type"],
)

LLM_CALLS = Counter(
    "reviewiq_llm_calls_total",
    "LLM API calls made",
    ["analysis_type"],
)

ANALYSIS_DURATION = Histogram(
    "reviewiq_analysis_duration_seconds",
    "Analysis duration in seconds",
    ["analysis_type"],
    buckets=(0.1, 0.5, 1, 2, 5, 10, 30, 60),
)
