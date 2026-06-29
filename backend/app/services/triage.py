import json
import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.session import CITriage
from app.integrations.github import github_client
from app.llm import get_llm
from app.llm.heuristics import classify_triage_heuristic
from app.metrics.prometheus import ANALYSES_COMPLETED, LLM_CALLS
from app.services.audit import write_audit

logger = logging.getLogger(__name__)


def _parse_llm_triage(content: str, fallback_class: str, fallback_summary: str) -> tuple[str, str]:
    try:
        data = json.loads(content)
        return str(data.get("classification", fallback_class)), str(data.get("summary", fallback_summary))
    except (json.JSONDecodeError, TypeError, ValueError):
        return fallback_class, content.strip()[:500] or fallback_summary


def analyze_workflow_run(db: Session, payload: dict) -> CITriage | None:
    run = payload.get("workflow_run") or payload
    conclusion = run.get("conclusion")
    if conclusion not in ("failure", "cancelled", "timed_out"):
        return None

    repo_full = payload.get("repository", {}).get("full_name", "")
    run_id = run.get("id")
    run_number = run.get("run_number", run_id)
    workflow_name = (run.get("name") or run.get("path") or "workflow").split("/")[-1]
    commit = (run.get("head_sha") or "")[:7]
    ci_id = f"CI-{run_id or uuid.uuid4().hex[:8]}"

    if db.get(CITriage, ci_id):
        return None

    owner, repo = repo_full.split("/", 1) if "/" in repo_full else ("", repo_full)
    log_text = ""
    if owner and run_id and github_client.available:
        log_text = github_client.download_workflow_logs(owner, repo, int(run_id))

    log_text = log_text or f"{workflow_name} {conclusion} {run.get('display_title', '')}"

    classification, summary, needs_llm = classify_triage_heuristic(log_text)
    model_provider = "heuristic"
    model_name = "rules"
    prompt = log_text[:8000]
    llm_output = json.dumps({"classification": classification, "summary": summary})

    llm = get_llm()
    if needs_llm and llm.available:
        system = (
            "Classify this CI failure. Respond with JSON only: "
            '{"classification": "infra|flaky|regression|environment", "summary": "one paragraph"}.'
        )
        try:
            response = llm.complete(f"Workflow: {workflow_name}\nConclusion: {conclusion}\n\nLogs:\n{log_text[:10000]}", system=system)
            LLM_CALLS.labels(analysis_type="triage").inc()
            classification, summary = _parse_llm_triage(response.content, classification, summary)
            model_provider = response.provider
            model_name = response.model
            prompt = response.prompt
            llm_output = response.content
        except Exception as exc:
            logger.error("LLM triage failed: %s", exc)

    if classification not in ("regression", "flaky", "infra", "environment"):
        classification = "regression"

    row = CITriage(
        id=ci_id,
        run=f"{repo.split('/')[-1] if '/' in repo_full else repo} · {workflow_name} #{run_number}",
        commit=commit or "unknown",
        classification=classification,
        summary=summary,
        reported_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    write_audit(
        db,
        analysis_type="triage",
        subject_id=ci_id,
        model_provider=model_provider,
        model_name=model_name,
        prompt=prompt[:10000],
        output=llm_output[:5000],
        action_taken=f"classified as {classification}",
    )
    ANALYSES_COMPLETED.labels(analysis_type="triage").inc()
    return row
