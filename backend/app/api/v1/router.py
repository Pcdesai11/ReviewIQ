from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import CITriage, FlakyTestFlag, PullRequestRisk, get_db
from app.schemas.results import (
    CITriageListOut,
    CITriageOut,
    FlakyTestListOut,
    FlakyTestOut,
    MetricsSummaryOut,
    PullRequestRiskOut,
)

router = APIRouter(prefix="/v1", tags=["results"])


def _minutes_ago(reported_at: datetime) -> int:
    now = datetime.now(timezone.utc)
    if reported_at.tzinfo is None:
        reported_at = reported_at.replace(tzinfo=timezone.utc)
    return max(0, int((now - reported_at).total_seconds() // 60))


@router.get("/pulls", response_model=list[PullRequestRiskOut])
def list_pulls(db: Session = Depends(get_db)):
    rows = db.query(PullRequestRisk).order_by(PullRequestRisk.risk_score.desc()).all()
    return rows


@router.get("/pulls/{pull_id}/risk", response_model=PullRequestRiskOut)
def get_pull_risk(pull_id: str, db: Session = Depends(get_db)):
    row = db.get(PullRequestRisk, pull_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Pull request {pull_id} not found")
    return row


@router.get("/tests/flaky", response_model=FlakyTestListOut)
def list_flaky_tests(db: Session = Depends(get_db)):
    rows = db.query(FlakyTestFlag).order_by(FlakyTestFlag.confidence.desc()).all()
    return FlakyTestListOut(tests=[FlakyTestOut.model_validate(r) for r in rows])


@router.get("/ci-runs/triage", response_model=CITriageListOut)
def list_ci_triage(db: Session = Depends(get_db)):
    rows = db.query(CITriage).order_by(CITriage.reported_at.desc()).all()
    items = [
        CITriageOut(
            id=r.id,
            run=r.run,
            commit=r.commit,
            classification=r.classification,
            summary=r.summary,
            minutes_ago=_minutes_ago(r.reported_at),
        )
        for r in rows
    ]
    return CITriageListOut(items=items)


@router.get("/ci-runs/{run_id}/triage", response_model=CITriageOut)
def get_ci_triage(run_id: str, db: Session = Depends(get_db)):
    row = db.get(CITriage, run_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"CI run {run_id} not found")
    return CITriageOut(
        id=row.id,
        run=row.run,
        commit=row.commit,
        classification=row.classification,
        summary=row.summary,
        minutes_ago=_minutes_ago(row.reported_at),
    )


@router.get("/metrics/summary", response_model=MetricsSummaryOut)
def get_metrics_summary(db: Session = Depends(get_db)):
    avg_risk = db.query(func.avg(PullRequestRisk.risk_score)).scalar() or 0
    high_risk = db.query(PullRequestRisk).filter(PullRequestRisk.risk_score >= 70).count()
    flaky_count = db.query(FlakyTestFlag).count()

    start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    triaged_today = db.query(CITriage).filter(CITriage.reported_at >= start_of_day).count()

    return MetricsSummaryOut(
        average_risk=round(float(avg_risk), 1),
        high_risk_open_prs=high_risk,
        flaky_tests_watched=flaky_count,
        triaged_today=triaged_today,
    )
