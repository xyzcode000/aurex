from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# -------------------------------------------------
# PROJECT BASE
# -------------------------------------------------

class ProjectBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    implementing_agency: str | None = Field(
        default=None,
        max_length=255,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    status: str = "planned"

    approved_budget: Decimal = Field(
        gt=0,
    )

    revised_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    expenditure: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )

    planned_start_date: date | None = None

    planned_end_date: date | None = None

    actual_start_date: date | None = None

    actual_end_date: date | None = None

    planned_progress: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        le=100,
    )

    actual_progress: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        le=100,
    )


# -------------------------------------------------
# CREATE PROJECT
# -------------------------------------------------

class ProjectCreate(ProjectBase):
    pass


# -------------------------------------------------
# UPDATE PROJECT
# -------------------------------------------------

class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    implementing_agency: str | None = Field(
        default=None,
        max_length=255,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    status: str | None = None

    approved_budget: Decimal | None = Field(
        default=None,
        gt=0,
    )

    revised_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    expenditure: Decimal | None = Field(
        default=None,
        ge=0,
    )

    planned_start_date: date | None = None

    planned_end_date: date | None = None

    actual_start_date: date | None = None

    actual_end_date: date | None = None

    planned_progress: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    actual_progress: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )


# -------------------------------------------------
# PROJECT RESPONSE
# -------------------------------------------------

class ProjectResponse(ProjectBase):
    id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# AUREX SCENARIO SIMULATION REQUEST
# -------------------------------------------------

class ScenarioRequest(BaseModel):
    """
    Input values for the Aurex Scenario Simulation Engine.
    """

    budget_change_percent: float = Field(
        default=0,
        ge=-100,
        le=100,
        description="Percentage change in approved budget",
    )

    delay_days: int = Field(
        default=0,
        ge=0,
        le=3650,
        description="Number of days to add as project delay",
    )

    progress_change_percent: float = Field(
        default=0,
        ge=-100,
        le=100,
        description="Percentage change in actual project progress",
    )