"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-28
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pull_request_risks",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("repo", sa.String(length=256), nullable=False),
        sa.Column("author", sa.String(length=128), nullable=False),
        sa.Column("files_changed", sa.Integer(), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "flaky_test_flags",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("suite", sa.String(length=256), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("last_flaked", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ci_triages",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("run", sa.String(length=256), nullable=False),
        sa.Column("commit", sa.String(length=64), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("reported_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("ci_triages")
    op.drop_table("flaky_test_flags")
    op.drop_table("pull_request_risks")
