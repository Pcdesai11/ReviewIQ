from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.config import settings

_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


class PullRequestRisk(Base):
    __tablename__ = "pull_request_risks"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    repo: Mapped[str] = mapped_column(String(256), nullable=False)
    author: Mapped[str] = mapped_column(String(128), nullable=False)
    files_changed: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


class FlakyTestFlag(Base):
    __tablename__ = "flaky_test_flags"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    suite: Mapped[str] = mapped_column(String(256), nullable=False)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)
    last_flaked: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


class CITriage(Base):
    __tablename__ = "ci_triages"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    run: Mapped[str] = mapped_column(String(256), nullable=False)
    commit: Mapped[str] = mapped_column(String(64), nullable=False)
    classification: Mapped[str] = mapped_column(String(32), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    reported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
