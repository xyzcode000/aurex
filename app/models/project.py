from datetime import date, datetime, timezone
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.database import Base


if TYPE_CHECKING:
    from app.models.financial_record import FinancialRecord
    from app.models.progress_record import ProgressRecord
    from app.models.milestone import Milestone


class Project(Base):

    @property
    def risk_level(self) -> str:
        if self.risk_score <= 25:
            return "LOW"
        elif self.risk_score <= 50:
            return "MEDIUM"
        elif self.risk_score <= 75:
            return "HIGH"
        else:
            return "CRITICAL"

    @property
    def risk_explanation(self) -> list[str]:
        explanations = []

        if self.budget > 0:
            expenditure_ratio = (
                self.expenditure / self.budget
            ) * 100

            if expenditure_ratio > 90:
                explanations.append(
                    "Expenditure has crossed 90% of the allocated budget."
                )
            elif expenditure_ratio > 75:
                explanations.append(
                    "Expenditure has crossed 75% of the allocated budget."
                )

        if self.progress_percentage < 30:
            explanations.append(
                "Project progress is below 30%."
            )
        elif self.progress_percentage < 50:
            explanations.append(
                "Project progress is below 50%."
            )

        if not explanations:
            explanations.append(
                "Project financial expenditure and progress are currently within the defined risk thresholds."
            )

        return explanations

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    public_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        unique=True,
        index=True,
        default=uuid4,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    department: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    budget: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    approved_cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    revised_cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    expenditure: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    planned_progress: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    progress_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    planned_completion_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    actual_completion_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE"
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    financial_records: Mapped[list["FinancialRecord"]] = relationship(
        "FinancialRecord",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    progress_records: Mapped[list["ProgressRecord"]] = relationship(
        "ProgressRecord",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    milestones: Mapped[list["Milestone"]] = relationship(
        "Milestone",
        back_populates="project",
        cascade="all, delete-orphan"
    )