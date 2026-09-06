from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: str | None = None

    department: str | None = None
    location: str | None = None

    budget: float = Field(..., gt=0)
    expenditure: float = Field(default=0, ge=0)

    progress_percentage: float = Field(
        default=0,
        ge=0,
        le=100
    )

    planned_completion_date: date | None = None


class ProjectResponse(ProjectCreate):
    id: int
    public_id: UUID
    status: str
    risk_score: float
    risk_level: str
    risk_explanation: list[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)