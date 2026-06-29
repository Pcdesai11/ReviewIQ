from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TriageClass = Literal["regression", "flaky", "infra", "environment"]


class PullRequestRiskOut(BaseModel):
    id: str
    title: str
    repo: str
    author: str
    files_changed: int = Field(serialization_alias="filesChanged")
    risk_score: int = Field(serialization_alias="riskScore")
    rationale: str

    model_config = {"from_attributes": True, "populate_by_name": True, "serialize_by_alias": True}


class FlakyTestOut(BaseModel):
    id: str
    name: str
    suite: str
    confidence: int
    last_flaked: str = Field(serialization_alias="lastFlaked")

    model_config = {"from_attributes": True, "populate_by_name": True, "serialize_by_alias": True}


class FlakyTestListOut(BaseModel):
    tests: list[FlakyTestOut]


class CITriageOut(BaseModel):
    id: str
    run: str
    commit: str
    classification: TriageClass
    summary: str
    minutes_ago: int = Field(serialization_alias="minutesAgo")

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class CITriageListOut(BaseModel):
    items: list[CITriageOut]


class MetricsSummaryOut(BaseModel):
    average_risk: float = Field(serialization_alias="averageRisk")
    high_risk_open_prs: int = Field(serialization_alias="highRiskOpenPRs")
    flaky_tests_watched: int = Field(serialization_alias="flakyTestsWatched")
    triaged_today: int = Field(serialization_alias="triagedToday")

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class HealthOut(BaseModel):
    status: str
    timestamp: datetime


class TrendPoint(BaseModel):
    date: str
    average_risk: float = Field(serialization_alias="averageRisk")
    flaky_flags: int = Field(serialization_alias="flakyFlags")
    triage_count: int = Field(serialization_alias="triageCount")

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class MetricsTrendOut(BaseModel):
    points: list[TrendPoint]


class AuditLogOut(BaseModel):
    id: str
    analysis_type: str = Field(serialization_alias="analysisType")
    subject_id: str = Field(serialization_alias="subjectId")
    model_provider: str = Field(serialization_alias="modelProvider")
    model_name: str = Field(serialization_alias="modelName")
    output: str
    action_taken: str = Field(serialization_alias="actionTaken")
    created_at: datetime = Field(serialization_alias="createdAt")

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class AuditLogListOut(BaseModel):
    items: list[AuditLogOut]
