from fastapi import HTTPException

from app.models.project import Project
from app.schemas.risk_engine import RiskEngineRequest


def build_risk_engine_request(
    project: Project
) -> RiskEngineRequest:
    """
    Convert the backend Project model into the
    input contract expected by the Risk Engine.
    """

    if project.approved_cost is None:
        raise HTTPException(
            status_code=400,
            detail="approved_cost is required for risk engine analysis"
        )

    if project.revised_cost is None:
        raise HTTPException(
            status_code=400,
            detail="revised_cost is required for risk engine analysis"
        )

    if project.planned_progress is None:
        raise HTTPException(
            status_code=400,
            detail="planned_progress is required for risk engine analysis"
        )

    return RiskEngineRequest(
        project_id=str(project.id),
        project_name=project.name,
        approved_cost=float(project.approved_cost),
        revised_cost=float(project.revised_cost),
        actual_expenditure=float(project.expenditure),
        planned_progress=float(project.planned_progress),
        actual_progress=float(project.progress_percentage),
    )