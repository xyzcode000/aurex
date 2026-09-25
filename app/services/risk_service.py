from sqlalchemy.orm import Session

from app.schemas.risk import RiskResponse
from app.services.project_service import (
    get_project,
    calculate_risk_score,
    get_risk_level,
    get_risk_explanation,
)


def get_project_risk(
    db: Session,
    project_id: str
) -> RiskResponse | None:

    project = get_project(db, project_id)

    if not project:
        return None

    risk_score = calculate_risk_score(project)

    return RiskResponse(
        project_id=project.id,
        risk_score=float(risk_score),
        risk_level=get_risk_level(risk_score),
        risk_explanation=get_risk_explanation(project)
    )