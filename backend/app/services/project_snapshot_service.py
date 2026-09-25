from datetime import date

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_snapshot import ProjectSnapshot


ALLOWED_SNAPSHOT_TYPES = {
    "baseline",
    "observation",
}


def create_project_snapshot(
    db: Session,
    project: Project,
    observation_date: date,
    snapshot_type: str = "observation",
) -> ProjectSnapshot:
    if snapshot_type not in ALLOWED_SNAPSHOT_TYPES:
        raise ValueError(
            "snapshot_type must be either 'baseline' or 'observation'."
        )

    snapshot = ProjectSnapshot(
        project_id=project.id,
        observation_date=observation_date,
        snapshot_type=snapshot_type,
        implementing_agency=project.implementing_agency,
        location=project.location,
        status=project.status,
        approved_budget=project.approved_budget,
        revised_budget=project.revised_budget,
        expenditure=project.expenditure,
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=project.planned_progress,
        actual_progress=project.actual_progress,
    )

    try:
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return snapshot

    except IntegrityError:
        db.rollback()

        raise ValueError(
            "A snapshot for this project and observation date already exists."
        )

    except SQLAlchemyError:
        db.rollback()
        raise