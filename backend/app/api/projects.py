from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.budget_intelligence import analyze_budget
from app.services.project_service import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects,
    update_project,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# -------------------------------------------------
# CREATE PROJECT
# -------------------------------------------------

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    return create_project(
        db=db,
        project_data=project_data,
    )


# -------------------------------------------------
# GET ALL PROJECTS
# -------------------------------------------------

@router.get(
    "",
    response_model=list[ProjectResponse],
)
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_projects(
        db=db,
        skip=skip,
        limit=limit,
    )


# -------------------------------------------------
# AUREX BUDGET INTELLIGENCE
# IMPORTANT: Specific route comes before /{project_id}
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/budget",
)
def get_budget_intelligence(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return analyze_budget(project)


# -------------------------------------------------
# GET SINGLE PROJECT
# -------------------------------------------------

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


# -------------------------------------------------
# UPDATE PROJECT
# -------------------------------------------------

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return update_project(
        db=db,
        project=project,
        project_data=project_data,
    )


# -------------------------------------------------
# DELETE PROJECT
# -------------------------------------------------

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    delete_project(
        db=db,
        project=project,
    )
    