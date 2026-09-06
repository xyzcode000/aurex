from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordResponse
)

from app.services.financial_record_service import (
    create_financial_record
)

from app.services.project_service import (
    create_project,
    get_project,
    get_projects,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "/",
    response_model=ProjectResponse
)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return create_project(db, project)


@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def list_all_projects(
    db: Session = Depends(get_db)
):
    return get_projects(db)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_single_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    project = get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

@router.post(
    "/{project_id}/financial",
    response_model=FinancialRecordResponse
)
def add_financial_record(
    project_id: str,
    record_data: FinancialRecordCreate,
    db: Session = Depends(get_db)
):
    record = create_financial_record(
        db,
        project_id,
        record_data
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return record