from pydantic import BaseModel, Field


class ScenarioRequest(BaseModel):
    additional_expenditure: float = Field(
        default=0.0,
        ge=0
    )
    additional_progress: float = Field(
        default=0.0,
        ge=0
    )


class ScenarioResponse(BaseModel):
    project_id: int
    current_expenditure: float
    simulated_expenditure: float
    current_progress: float
    simulated_progress: float
    simulated_expenditure_ratio: float
    simulated_risk_score: float
    simulated_risk_level: str