from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utc_now() -> datetime:
    """
    Return the current UTC time as a naive datetime.

    The database currently uses DateTime(timezone=False), so we keep
    the stored representation compatible with the existing schema
    while avoiding deprecated datetime.utcnow().
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ProjectSnapshot(Base):
    """
    Historical point-in-time state of a project.

    A snapshot represents the project data known/recorded at a
    particular observation date. The current `projects` table remains
    the operational source of truth for the latest state.
    """

    __tablename__ = "project_snapshots"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "observation_date",
            name="uq_project_snapshot_project_date",
        ),
        Index(
            "ix_project_snapshots_project_date",
            "project_id",
            "observation_date",
        ),
        CheckConstraint(
            "approved_budget >= 0",
            name="ck_project_snapshots_approved_budget_nonnegative",
        ),
        CheckConstraint(
            "revised_budget IS NULL OR revised_budget >= 0",
            name="ck_project_snapshots_revised_budget_nonnegative",
        ),
        CheckConstraint(
            "expenditure >= 0",
            name="ck_project_snapshots_expenditure_nonnegative",
        ),
        CheckConstraint(
            "planned_progress >= 0 AND planned_progress <= 100",
            name="ck_project_snapshots_planned_progress_range",
        ),
        CheckConstraint(
            "actual_progress >= 0 AND actual_progress <= 100",
            name="ck_project_snapshots_actual_progress_range",
        ),
        CheckConstraint(
            "planned_start_date IS NULL "
            "OR planned_end_date IS NULL "
            "OR planned_end_date >= planned_start_date",
            name="ck_project_snapshots_planned_dates_valid",
        ),
        CheckConstraint(
            "actual_start_date IS NULL "
            "OR actual_end_date IS NULL "
            "OR actual_end_date >= actual_start_date",
            name="ck_project_snapshots_actual_dates_valid",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    observation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    implementing_agency: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="planned",
    )

    approved_budget: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    revised_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    expenditure: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0"),
    )

    planned_start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    planned_end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    actual_start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    actual_end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    planned_progress: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0"),
    )

    actual_progress: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now,
    )