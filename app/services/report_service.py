from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.report import ProjectReportResponse
from app.services.project_service import get_project


def get_project_report(
    db: Session,
    project_id: str
) -> ProjectReportResponse | None:

    project = get_project(db, project_id)

    if not project:
        return None

    remaining_budget = (
        project.budget - project.expenditure
    )

    return ProjectReportResponse(
        project_id=project.id,
        project_name=project.name,
        department=project.department,
        location=project.location,
        budget=float(project.budget),
        expenditure=float(project.expenditure),
        remaining_budget=float(remaining_budget),
        progress_percentage=float(project.progress_percentage),
        status=project.status,
        risk_score=float(project.risk_score),
        risk_level=project.risk_level,
        risk_explanation=project.risk_explanation,
        financial_records_count=len(project.financial_records),
        progress_records_count=len(project.progress_records),
        milestones_count=len(project.milestones)
    )