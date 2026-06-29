from datetime import datetime, timedelta, timezone

from app.db.session import CITriage, FlakyTestFlag, PullRequestRisk, SessionLocal

SEED_PULLS = [
    {
        "id": "PR-2291",
        "title": "Rework session refresh to use rotating tokens",
        "repo": "platform/auth-service",
        "author": "r.alvarez",
        "files_changed": 14,
        "risk_score": 84,
        "rationale": "Touches token validation and silently changes refresh expiry from 30m to 15m.",
    },
    {
        "id": "PR-2287",
        "title": "Add retry/backoff to payment webhook consumer",
        "repo": "platform/billing",
        "author": "j.okafor",
        "files_changed": 6,
        "risk_score": 67,
        "rationale": "Introduces at-least-once delivery risk; no idempotency key check added.",
    },
    {
        "id": "PR-2284",
        "title": "Migrate orders table to add partial index",
        "repo": "platform/orders",
        "author": "l.chen",
        "files_changed": 3,
        "risk_score": 58,
        "rationale": "Online migration on a hot table; lock duration not measured in staging.",
    },
    {
        "id": "PR-2279",
        "title": "Update changelog and bump dev dependencies",
        "repo": "platform/web",
        "author": "a.novak",
        "files_changed": 2,
        "risk_score": 9,
        "rationale": "Docs and devDependencies only, no runtime code touched.",
    },
]

SEED_FLAKY = [
    {
        "id": "FT-014",
        "name": "test_session_expiry_boundary",
        "suite": "auth-service / integration",
        "confidence": 81,
        "last_flaked": "3 runs ago",
    },
    {
        "id": "FT-009",
        "name": "test_webhook_delivery_ordering",
        "suite": "billing / integration",
        "confidence": 64,
        "last_flaked": "7 runs ago",
    },
    {
        "id": "FT-031",
        "name": "test_cart_total_rounding",
        "suite": "orders / unit",
        "confidence": 22,
        "last_flaked": "19 runs ago",
    },
]

SEED_TRIAGE = [
    {
        "id": "CI-5510",
        "run": "auth-service · build #5510",
        "commit": "4f2a91c",
        "classification": "regression",
        "summary": "Token refresh test fails consistently after PR-2291; not a flake.",
        "minutes_ago": 6,
    },
    {
        "id": "CI-5508",
        "run": "web · build #5508",
        "commit": "9c0e7aa",
        "classification": "infra",
        "summary": "Runner lost network mid-job pulling node_modules cache.",
        "minutes_ago": 41,
    },
    {
        "id": "CI-5503",
        "run": "billing · build #5503",
        "commit": "a13d402",
        "classification": "flaky",
        "summary": "Webhook ordering test failed once in 40 runs; matches known flake signature.",
        "minutes_ago": 95,
    },
    {
        "id": "CI-5498",
        "run": "orders · build #5498",
        "commit": "7b88e10",
        "classification": "environment",
        "summary": "Local Postgres version mismatch in self-hosted runner pool.",
        "minutes_ago": 162,
    },
]


def seed_database() -> None:
    now = datetime.now(timezone.utc)
    db = SessionLocal()
    try:
        if db.query(PullRequestRisk).count() > 0:
            print("Database already seeded — skipping.")
            return

        for row in SEED_PULLS:
            db.add(PullRequestRisk(**row))

        for row in SEED_FLAKY:
            db.add(FlakyTestFlag(**row))

        for raw in SEED_TRIAGE:
            row = dict(raw)
            minutes_ago = row.pop("minutes_ago")
            reported_at = now - timedelta(minutes=minutes_ago)
            db.add(CITriage(reported_at=reported_at, **row))

        db.commit()
        print("Seed data loaded.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
