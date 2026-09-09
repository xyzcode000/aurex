from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class MilestoneCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    planned_date: date

    actual_date: date | None = None

    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "DELAYED"] = "PENDING"

    description: str | None = None


class MilestoneResponse(MilestoneCreate):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )