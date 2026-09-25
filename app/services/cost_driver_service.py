from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.cost_driver import CostDriverResponse
from app.services.project_service import get_project


def get_cost_drivers(
    db: Session,
    project_id: str
) -> CostDriverResponse | None:

    project = get_project(db, project_id)

    if not project:
        return None

    expenditure_ratio = 0.0

    if project.budget > 0:
        expenditure_ratio = (
            project.expenditure / project.budget
        ) * 100

    remaining_budget = (
        project.budget - project.expenditure
    )

    cost_progress_gap = (
        expenditure_ratio - project.progress_percentage
    )

    if expenditure_ratio > 90:
        primary_cost_driver = "HIGH_EXPENDITURE"
    elif expenditure_ratio > 75:
        primary_cost_driver = "ELEVATED_EXPENDITURE"
    elif project.progress_percentage < 30:
        primary_cost_driver = "LOW_PROGRESS"
    elif cost_progress_gap > 20:
        primary_cost_driver = "COST_PROGRESS_MISMATCH"
    else:
        primary_cost_driver = "NO_MAJOR_COST_DRIVER"

    return CostDriverResponse(
        project_id=project.id,
        budget=float(project.budget),
        expenditure=float(project.expenditure),
        expenditure_ratio=round(expenditure_ratio, 2),
        remaining_budget=float(remaining_budget),
        progress_percentage=float(project.progress_percentage),
        cost_progress_gap=round(cost_progress_gap, 2),
        primary_cost_driver=primary_cost_driver
    )