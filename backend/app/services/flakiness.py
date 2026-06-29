import logging
import re
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import FlakyTestFlag, TestRunRecord
from app.integrations.github import github_client
from app.llm.heuristics import score_flaky_heuristic
from app.metrics.prometheus import ANALYSES_COMPLETED
from app.services.audit import write_audit

logger = logging.getLogger(__name__)

TEST_NAME_PATTERN = re.compile(r"(?:FAILED|FAIL)\s+(\S+)|(\btest_\w+|\bTest\w+\.\w+)")


def _extract_failed_tests(log_text: str) -> list[str]:
    names: set[str] = set()
    for match in TEST_NAME_PATTERN.finditer(log_text):
        name = match.group(1) or match.group(2)
        if name:
            names.add(name.strip("()[]"))
    return list(names)[:20]


def record_test_outcomes(db: Session, payload: dict) -> list[FlakyTestFlag]:
    run = payload.get("workflow_run") or payload
    repo_full = payload.get("repository", {}).get("full_name", "")
    run_id = str(run.get("id", uuid.uuid4().hex[:8]))
    conclusion = run.get("conclusion", "unknown")
    owner, repo = repo_full.split("/", 1) if "/" in repo_full else ("", repo_full)

    log_text = ""
    if owner and run.get("id") and github_client.available:
        log_text = github_client.download_workflow_logs(owner, repo, int(run["id"]))

    failed_tests = _extract_failed_tests(log_text)
    if not failed_tests and conclusion == "failure":
        failed_tests = [f"unknown_failure_{run_id[-6:]}"]

    now = datetime.now(timezone.utc)
    updated: list[FlakyTestFlag] = []

    for test_name in failed_tests:
        db.add(
            TestRunRecord(
                id=str(uuid.uuid4()),
                repo=repo_full or "unknown",
                test_name=test_name,
                suite=(run.get("name") or "ci")[:256],
                run_id=run_id,
                outcome="failed",
                created_at=now,
            )
        )

    if conclusion == "success":
        db.add(
            TestRunRecord(
                id=str(uuid.uuid4()),
                repo=repo_full or "unknown",
                test_name="__workflow_success__",
                suite=(run.get("name") or "ci")[:256],
                run_id=run_id,
                outcome="passed",
                created_at=now,
            )
        )

    db.commit()

    cutoff = now - timedelta(days=30)
    for test_name in failed_tests:
        total = (
            db.query(func.count(TestRunRecord.id))
            .filter(
                TestRunRecord.repo == repo_full,
                TestRunRecord.test_name == test_name,
                TestRunRecord.created_at >= cutoff,
            )
            .scalar()
            or 0
        )
        fails = (
            db.query(func.count(TestRunRecord.id))
            .filter(
                TestRunRecord.repo == repo_full,
                TestRunRecord.test_name == test_name,
                TestRunRecord.outcome == "failed",
                TestRunRecord.created_at >= cutoff,
            )
            .scalar()
            or 0
        )
        if total < 2:
            continue

        confidence, rationale = score_flaky_heuristic(test_name, log_text, fails, total)
        if confidence < 25:
            continue

        flag_id = f"FT-{test_name[:20].replace(' ', '_')}-{hash(repo_full) % 10000:04d}"
        suite = f"{repo_full.split('/')[-1] if repo_full else 'unknown'} / ci"
        last_flaked = f"{fails} failures in {total} runs"

        existing = db.get(FlakyTestFlag, flag_id)
        if existing:
            existing.confidence = confidence
            existing.last_flaked = last_flaked
            existing.name = test_name
            row = existing
        else:
            row = FlakyTestFlag(
                id=flag_id,
                name=test_name,
                suite=suite,
                confidence=confidence,
                last_flaked=last_flaked,
                created_at=now,
            )
            db.add(row)

        db.commit()
        db.refresh(row)
        updated.append(row)

        write_audit(
            db,
            analysis_type="flakiness",
            subject_id=flag_id,
            model_provider="heuristic",
            model_name="stats+rules",
            prompt=f"test={test_name} fails={fails} total={total}\n{log_text[:4000]}",
            output=f'{{"confidence": {confidence}, "rationale": "{rationale}"}}',
            action_taken="flagged" if confidence >= 50 else "watching",
        )
        ANALYSES_COMPLETED.labels(analysis_type="flakiness").inc()

    return updated
