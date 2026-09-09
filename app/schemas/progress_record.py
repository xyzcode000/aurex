from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ProgressRecordCreate(BaseModel):
    record_date: date

    progress_percentage: float = Field(
        ...,
        ge=0,
        le=100
    )

    remarks: str | None = None


class ProgressRecordResponse(ProgressRecordCreate):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)