from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.project import Project
from app.schemas.analytics import BenchmarkResponse


def get_project_benchmark(
    db: Session
) -> BenchmarkResponse:

    result = (
        db.query(
            func.count(Project.id),
            func.avg(Project.budget),
            func.avg(Project.expenditure),
            func.avg(Project.progress_percentage)
        )
        .first()
    )

    total_projects = result[0] or 0
    average_budget = result[1] or 0
    average_expenditure = result[2] or 0
    average_progress = result[3] or 0

    return BenchmarkResponse(
        total_projects=total_projects,
        average_budget=float(average_budget),
        average_expenditure=float(average_expenditure),
        average_progress=float(average_progress)
    )