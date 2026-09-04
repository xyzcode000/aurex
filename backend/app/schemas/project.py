from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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


class ProjectCreate(ProjectBase):
    pass


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


class ProjectResponse(ProjectBase):
    id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )