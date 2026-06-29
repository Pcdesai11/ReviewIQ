import re
from dataclasses import dataclass


@dataclass
class HeuristicResult:
    score: int
    rationale: str
    needs_llm: bool


RISK_PATTERNS: list[tuple[re.Pattern[str], int, str]] = [
    (re.compile(r"\b(auth|token|session|password|credential|oauth|jwt)\b", re.I), 25, "auth/credentials"),
    (re.compile(r"\b(migrat(e|ion)|schema|alter table)\b", re.I), 20, "database migration"),
    (re.compile(r"\b(concurrent|mutex|lock|race|thread|async)\b", re.I), 15, "concurrency"),
    (re.compile(r"\b(delete|drop|truncate|remove.*endpoint)\b", re.I), 15, "destructive change"),
    (re.compile(r"\b(payment|billing|invoice|charge)\b", re.I), 20, "payment/billing"),
    (re.compile(r"\b(encrypt|decrypt|secret|key rotation)\b", re.I), 18, "crypto/secrets"),
]

FLAKY_PATTERNS: list[tuple[re.Pattern[str], int]] = [
    (re.compile(r"\b(timeout|timed out|deadline)\b", re.I), 30),
    (re.compile(r"\b(flake|flaky|intermittent)\b", re.I), 40),
    (re.compile(r"\b(race|ordering|parallel)\b", re.I), 20),
    (re.compile(r"\b(network|connection reset|ECONNREFUSED)\b", re.I), 25),
    (re.compile(r"\b(sleep|wait|retry)\b", re.I), 15),
]

TRIAGE_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\b(runner|network|timeout|503|502|connection reset)\b", re.I), "infra", "Infrastructure or runner connectivity issue."),
    (re.compile(r"\b(flake|flaky|intermittent|passed on retry)\b", re.I), "flaky", "Intermittent failure matching known flake patterns."),
    (re.compile(r"\b(version mismatch|environment|env var|missing.*config)\b", re.I), "environment", "Environment configuration mismatch."),
]


def score_diff_heuristic(diff_text: str, files_changed: int) -> HeuristicResult:
    hits: list[str] = []
    score = min(files_changed * 2, 20)

    for pattern, weight, label in RISK_PATTERNS:
        if pattern.search(diff_text):
            score += weight
            hits.append(label)

    score = min(score, 95)
    if score >= 70 or (hits and score >= 45):
        rationale = f"Heuristic flags: {', '.join(hits)}." if hits else "Large diff with elevated change surface."
        return HeuristicResult(score=score, rationale=rationale, needs_llm=score >= 40)

    if not hits and files_changed <= 3:
        return HeuristicResult(
            score=max(5, score),
            rationale="Small diff; no high-risk patterns detected.",
            needs_llm=False,
        )

    return HeuristicResult(
        score=score,
        rationale=f"Moderate change surface{f' ({', '.join(hits)})' if hits else ''}.",
        needs_llm=True,
    )


def score_flaky_heuristic(test_name: str, failure_log: str, fail_count: int, total_runs: int) -> tuple[int, str]:
    text = f"{test_name} {failure_log}"
    score = 0
    for pattern, weight in FLAKY_PATTERNS:
        if pattern.search(text):
            score += weight

    if total_runs > 0:
        rate = fail_count / total_runs
        if 0 < rate < 0.15:
            score += int(rate * 200)
        elif rate >= 0.15:
            score += 10

    score = min(score, 95)
    if score >= 50:
        rationale = f"Failed {fail_count}/{total_runs} recent runs; intermittent failure signature."
    elif score >= 25:
        rationale = f"Possible flake — failed {fail_count}/{total_runs} runs with timing/network signals."
    else:
        rationale = f"Low flake signal ({fail_count}/{total_runs} failures)."
    return score, rationale


def classify_triage_heuristic(log_text: str) -> tuple[str, str, bool]:
    for pattern, classification, summary in TRIAGE_PATTERNS:
        if pattern.search(log_text):
            return classification, summary, True

    if re.search(r"\b(assert|expected|actual|TypeError|ReferenceError|failed)\b", log_text, re.I):
        return "regression", "Consistent test failure with assertion or code error — likely a real regression.", False

    return "regression", "Failure lacks infra/flake/environment signals; treating as regression.", True
