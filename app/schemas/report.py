from pydantic import BaseModel


class ProjectReportResponse(BaseModel):
    project_id: int
    project_name: str
    department: str | None
    location: str | None

    budget: float
    expenditure: float
    remaining_budget: float

    progress_percentage: float
    status: str

    risk_score: float
    risk_level: str
    risk_explanation: list[str]

    financial_records_count: int
    progress_records_count: int
    milestones_count: int