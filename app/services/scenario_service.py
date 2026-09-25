from types import SimpleNamespace

from sqlalchemy.orm import Session

from app.schemas.scenario import (
    ScenarioRequest,
    ScenarioResponse
)
from app.services.project_service import (
    get_project,
    calculate_risk_score,
    get_risk_level
)


def simulate_project_scenario(
    db: Session,
    project_id: str,
    scenario_data: ScenarioRequest
) -> ScenarioResponse | None:

    # Find the project
    project = get_project(db, project_id)

    if not project:
        return None

    # Keep original values
    current_expenditure = project.expenditure
    current_progress = project.progress_percentage

    # Calculate simulated values
    simulated_expenditure = (
        current_expenditure
        + scenario_data.additional_expenditure
    )

    simulated_progress = min(
        current_progress
        + scenario_data.additional_progress,
        100
    )

    # Create a temporary object for risk calculation.
    # This does NOT modify the database project.
    simulated_project = SimpleNamespace(
        budget=project.budget,
        expenditure=simulated_expenditure,
        progress_percentage=simulated_progress
    )

    # Calculate simulated risk
    simulated_risk_score = calculate_risk_score(
        simulated_project
    )

    simulated_risk_level = get_risk_level(
        simulated_risk_score
    )

    # Calculate simulated expenditure ratio
    simulated_expenditure_ratio = 0.0

    if project.budget > 0:
        simulated_expenditure_ratio = (
            simulated_expenditure / project.budget
        ) * 100

    return ScenarioResponse(
        project_id=project.id,
        current_expenditure=float(
            current_expenditure
        ),
        simulated_expenditure=float(
            simulated_expenditure
        ),
        current_progress=float(
            current_progress
        ),
        simulated_progress=float(
            simulated_progress
        ),
        simulated_expenditure_ratio=round(
            simulated_expenditure_ratio,
            2
        ),
        simulated_risk_score=float(
            simulated_risk_score
        ),
        simulated_risk_level=simulated_risk_level
    )