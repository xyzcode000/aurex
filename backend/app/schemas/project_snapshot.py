from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProjectSnapshotCreate(BaseModel):
    """
    Request used to record a historical project observation.

    The API only accepts the observation date.
    The remaining project state is captured from the current project.
    """

    observation_date: date


class ProjectSnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    observation_date: date
    snapshot_type: str

    implementing_agency: str | None
    location: str | None
    status: str

    approved_budget: Decimal
    revised_budget: Decimal | None
    expenditure: Decimal

    planned_start_date: date | None
    planned_end_date: date | None
    actual_start_date: date | None
    actual_end_date: date | None

    planned_progress: Decimal
    actual_progress: Decimal

    created_at: datetime