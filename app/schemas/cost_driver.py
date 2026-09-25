from pydantic import BaseModel


class CostDriverResponse(BaseModel):
    project_id: int
    budget: float
    expenditure: float
    expenditure_ratio: float
    remaining_budget: float
    progress_percentage: float
    cost_progress_gap: float
    primary_cost_driver: str