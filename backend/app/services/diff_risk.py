import json
import logging
import re
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import PullRequestRisk
from app.integrations.github import github_client
from app.llm import get_llm
from app.llm.heuristics import score_diff_heuristic
from app.metrics.prometheus import ANALYSES_COMPLETED, LLM_CALLS
from app.services.audit import write_audit

logger = logging.getLogger(__name__)


def _parse_llm_risk(content: str, fallback_score: int, fallback_rationale: str) -> tuple[int, str]:
    try:
        data = json.loads(content)
        return int(data.get("risk_score", fallback_score)), str(data.get("rationale", fallback_rationale))
    except (json.JSONDecodeError, TypeError, ValueError):
        match = re.search(r"(\d{1,3})", content)
        score = int(match.group(1)) if match else fallback_score
        return min(score, 100), content.strip()[:500] or fallback_rationale


def analyze_pull_request(db: Session, payload: dict) -> PullRequestRisk | None:
    pr = payload.get("pull_request") or payload
    repo_full = payload.get("repository", {}).get("full_name", "")
    if not repo_full and "repo" in payload:
        repo_full = payload["repo"].get("full_name", "")

    number = pr.get("number")
    if not number or not repo_full:
        logger.warning("PR payload missing number or repo")
        return None

    owner, repo = repo_full.split("/", 1)
    pr_id = f"{repo_full}#{number}"

    diff_text = ""
    if github_client.available:
        try:
            diff_text = github_client.get_pull_diff(owner, repo, number)
        except Exception as exc:
            logger.warning("Could not fetch diff: %s", exc)

    if not diff_text:
        diff_text = pr.get("body") or pr.get("title") or ""

    files_changed = pr.get("changed_files") or len(pr.get("files") or []) or max(1, diff_text.count("diff --git"))

    heuristic = score_diff_heuristic(diff_text[:50000], files_changed)
    risk_score = heuristic.score
    rationale = heuristic.rationale
    model_provider = "heuristic"
    model_name = "rules"
    prompt = f"PR {pr_id}\nFiles: {files_changed}\n\n{diff_text[:8000]}"
    llm_output = json.dumps({"risk_score": risk_score, "rationale": rationale})

    llm = get_llm()
    if heuristic.needs_llm and llm.available:
        system = (
            "You are a senior engineer reviewing a pull request diff. "
            'Respond with JSON only: {"risk_score": 0-100, "rationale": "one sentence"}. '
            "Focus on auth, migrations, concurrency, silent behavior changes."
        )
        user_prompt = f"PR: {pr.get('title', '')}\nRepo: {repo_full}\nFiles changed: {files_changed}\n\nDiff:\n{diff_text[:12000]}"
        try:
            response = llm.complete(user_prompt, system=system)
            LLM_CALLS.labels(analysis_type="diff_risk").inc()
            risk_score, rationale = _parse_llm_risk(response.content, risk_score, rationale)
            model_provider = response.provider
            model_name = response.model
            prompt = response.prompt
            llm_output = response.content
        except Exception as exc:
            logger.error("LLM diff risk failed: %s", exc)

    title = pr.get("title", "Untitled PR")
    author = (pr.get("user") or {}).get("login", "unknown")

    existing = db.get(PullRequestRisk, pr_id)
    if existing:
        existing.title = title
        existing.repo = repo_full
        existing.author = author
        existing.files_changed = files_changed
        existing.risk_score = risk_score
        existing.rationale = rationale
        row = existing
    else:
        row = PullRequestRisk(
            id=pr_id,
            title=title,
            repo=repo_full,
            author=author,
            files_changed=files_changed,
            risk_score=risk_score,
            rationale=rationale,
            created_at=datetime.now(timezone.utc),
        )
        db.add(row)

    db.commit()
    db.refresh(row)

    action = "scored"
    if risk_score >= settings.risk_threshold:
        comment = (
            f"**ReviewIQ — Risk score {risk_score}/100**\n\n"
            f"{rationale}\n\n"
            f"_Threshold: {settings.risk_threshold}. Please review carefully._"
        )
        if github_client.create_issue_comment(owner, repo, number, comment):
            action = f"scored + commented (score >= {settings.risk_threshold})"

    write_audit(
        db,
        analysis_type="diff_risk",
        subject_id=pr_id,
        model_provider=model_provider,
        model_name=model_name,
        prompt=prompt[:10000],
        output=llm_output[:5000],
        action_taken=action,
    )
    ANALYSES_COMPLETED.labels(analysis_type="diff_risk").inc()
    return row
