from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.project import Project
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