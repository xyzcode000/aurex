from pydantic import BaseModel


class BenchmarkResponse(BaseModel):
    total_projects: int
    average_budget: float
    average_expenditure: float
    average_progress: float