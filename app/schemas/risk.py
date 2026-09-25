from pydantic import BaseModel


class RiskResponse(BaseModel):
    project_id: int
    risk_score: float
    risk_level: str
    risk_explanation: list[str]