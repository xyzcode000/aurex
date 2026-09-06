from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class FinancialRecordCreate(BaseModel):
    record_date: date
    expenditure: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )
    funding_received: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )
    description: str | None = None


class FinancialRecordResponse(FinancialRecordCreate):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)