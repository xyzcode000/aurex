from sqlalchemy.orm import Session

from app.models.progress_record import ProgressRecord
from app.schemas.progress_record import ProgressRecordCreate
from app.services.project_service import get_project, calculate_risk_score


def create_progress_record(
    db: Session,
    project_id: str,
    record_data: ProgressRecordCreate
) -> ProgressRecord | None:

    # Find the project using either internal ID or public UUID
    project = get_project(db, project_id)

    if not project:
        return None

    # Create progress record using the project's internal ID
    record = ProgressRecord(
        project_id=project.id,
        **record_data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    # Update project's current progress
    project.progress_percentage = record.progress_percentage

    # Recalculate project risk after progress changes
    project.risk_score = calculate_risk_score(project)

    db.commit()
    db.refresh(project)

    return record