from sqlalchemy.orm import Session

from app.models.milestone import Milestone
from app.schemas.milestone import MilestoneCreate
from app.services.project_service import get_project


def create_milestone(
    db: Session,
    project_id: str,
    milestone_data: MilestoneCreate
) -> Milestone | None:

    # Find project using internal ID or public UUID
    project = get_project(db, project_id)

    if not project:
        return None

    # Create milestone using project's internal ID
    milestone = Milestone(
        project_id=project.id,
        **milestone_data.model_dump()
    )

    db.add(milestone)
    db.commit()
    db.refresh(milestone)

    return milestone

def get_milestones(
    db: Session,
    project_id: str
) -> list[Milestone] | None:

    project = get_project(db, project_id)

    if not project:
        return None

    return (
    db.query(Milestone)
    .filter(Milestone.project_id == project.id)
    .order_by(Milestone.planned_date.asc())
    .all()
)