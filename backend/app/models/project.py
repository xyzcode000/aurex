from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
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


class Project(Base):
    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint(
            "approved_budget >= 0",
            name="ck_projects_approved_budget_nonnegative",
        ),
        CheckConstraint(
            "revised_budget IS NULL OR revised_budget >= 0",
            name="ck_projects_revised_budget_nonnegative",
        ),
        CheckConstraint(
            "expenditure >= 0",
            name="ck_projects_expenditure_nonnegative",
        ),
        CheckConstraint(
            "planned_progress >= 0 AND planned_progress <= 100",
            name="ck_projects_planned_progress_range",
        ),
        CheckConstraint(
            "actual_progress >= 0 AND actual_progress <= 100",
            name="ck_projects_actual_progress_range",
        ),
        CheckConstraint(
            "planned_start_date IS NULL "
            "OR planned_end_date IS NULL "
            "OR planned_end_date >= planned_start_date",
            name="ck_projects_planned_dates_valid",
        ),
        CheckConstraint(
            "actual_start_date IS NULL "
            "OR actual_end_date IS NULL "
            "OR actual_end_date >= actual_start_date",
            name="ck_projects_actual_dates_valid",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
        default=0,
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
        default=0,
    )

    actual_progress: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )