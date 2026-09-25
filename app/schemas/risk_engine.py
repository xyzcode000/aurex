from typing import Literal

from pydantic import BaseModel, Field


class RiskEngineRequest(BaseModel):
    project_id: str
    project_name: str

    approved_cost: float
    revised_cost: float
    actual_expenditure: float

    planned_progress: float
    actual_progress: float


class RiskEngineRisk(BaseModel):
    score: float = Field(..., ge=0, le=100)
    level: Literal["LOW", "MEDIUM", "HIGH"]


class RiskEngineAnomaly(BaseModel):
    status: Literal["NORMAL", "ANOMALY"]


class RiskEngineIndicators(BaseModel):
    progress_gap: float
    cost_overrun_pct: float
    spending_pct: float
    spending_vs_progress: float


class RiskEngineResponse(BaseModel):
    project_id: str
    project_name: str

    risk: RiskEngineRisk
    anomaly: RiskEngineAnomaly
    indicators: RiskEngineIndicators

    risk_reasons: list[str]