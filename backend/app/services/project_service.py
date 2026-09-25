from datetime import date

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_snapshot import ProjectSnapshot
from app.schemas.project import ProjectCreate, ProjectUpdate


# =========================================================
# CREATE PROJECT
# =========================================================

def create_project(
    db: Session,
    project_data: ProjectCreate,
) -> Project:

    try:
        project = Project(
            **project_data.model_dump()
        )

        db.add(project)

        # Flush assigns the project ID without committing yet.
        db.flush()

        # -------------------------------------------------
        # AUTOMATIC BASELINE SNAPSHOT
        # -------------------------------------------------

        baseline_snapshot = ProjectSnapshot(
            project_id=project.id,
            observation_date=date.today(),
            snapshot_type="baseline",
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

        db.add(baseline_snapshot)

        # -------------------------------------------------
        # ATOMIC COMMIT
        # -------------------------------------------------

        db.commit()

        db.refresh(project)

        return project

    except SQLAlchemyError:
        db.rollback()
        raise


# =========================================================
# GET ALL PROJECTS
# =========================================================

def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Project]:

    return (
        db.query(Project)
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================================================
# GET PROJECT BY ID
# =========================================================

def get_project_by_id(
    db: Session,
    project_id: int,
) -> Project | None:

    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )


# =========================================================
# UPDATE PROJECT
# =========================================================

def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
) -> Project:

    try:
        update_data = project_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(project, field, value)

        db.commit()
        db.refresh(project)

        return project

    except SQLAlchemyError:
        db.rollback()
        raise


# =========================================================
# DELETE PROJECT
# =========================================================

def delete_project(
    db: Session,
    project: Project,
) -> None:

    try:
        db.delete(project)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise