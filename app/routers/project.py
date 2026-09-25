
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.analytics import BenchmarkResponse
from app.schemas.cost_driver import CostDriverResponse
from app.schemas.report import ProjectReportResponse
from app.schemas.scenario import (
    ScenarioRequest,
    ScenarioResponse
)
from app.schemas.risk import RiskResponse

from app.services.risk_service import get_project_risk
from app.services.scenario_service import (
    simulate_project_scenario
)
from app.services.report_service import get_project_report
from app.services.cost_driver_service import get_cost_drivers
from app.services.analytics_service import get_project_benchmark
from app.schemas.progress_record import ProgressRecordCreate, ProgressRecordResponse
from app.services.progress_record_service import (
    create_progress_record,
    get_progress_records
)

from app.schemas.milestone import MilestoneCreate, MilestoneResponse
from app.services.milestone_service import (
    create_milestone,
    get_milestones
)
from app.db.database import get_db

from app.core.dependencies import (
    get_current_user,
    require_project_manager_or_admin,
    require_admin,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordResponse
)

from app.services.financial_record_service import (
    create_financial_record,
    get_financial_records

)

from app.services.project_service import (
    create_project,
    get_project,
    get_projects,
    update_project,
    delete_project,

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
    db: Session = Depends(get_db),
    current_user=Depends(require_project_manager_or_admin),
):
    return create_project(db, project)


@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def list_all_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_projects(db)

@router.get(
    "/analytics/benchmark",
    response_model=BenchmarkResponse
)
def project_benchmark(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),

):
    return get_project_benchmark(db)

@router.get(
    "/investigation/{project_id}/cost-drivers",
    response_model=CostDriverResponse
)
def project_cost_drivers(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = get_cost_drivers(
        db,
        project_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return result

@router.get(
    "/reports/{project_id}",
    response_model=ProjectReportResponse
)
def project_report(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = get_project_report(
        db,
        project_id
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return report

@router.post(
    "/scenarios/{project_id}",
    response_model=ScenarioResponse
)
def project_scenario(
    project_id: str,
    scenario_data: ScenarioRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = simulate_project_scenario(
        db,
        project_id,
        scenario_data
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return result

@router.get(
    "/risk/{project_id}",
    response_model=RiskResponse
)
def project_risk(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    risk = get_project_risk(
        db,
        project_id
    )

    if not risk:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return risk
@router.delete(
    "/{project_id}",
    status_code=204
)
def delete_existing_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    project = delete_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return None

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_single_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),

):
    project = get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_existing_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_project_manager_or_admin),
):
    project = update_project(
        db,
        project_id,
        project_data
    )

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
    db: Session = Depends(get_db),
    current_user=Depends(require_project_manager_or_admin),
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

@router.get(
    "/{project_id}/financial",
    response_model=list[FinancialRecordResponse]
)
def list_financial_records(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    records = get_financial_records(
        db,
        project_id
    )

    if records is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return records

@router.post(
    "/{project_id}/progress",
    response_model=ProgressRecordResponse
)
def add_progress_record(
    project_id: str,
    record_data: ProgressRecordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_project_manager_or_admin),
):
    record = create_progress_record(
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

@router.get(
    "/{project_id}/progress",
    response_model=list[ProgressRecordResponse]
)
def list_progress_records(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    records = get_progress_records(
        db,
        project_id
    )

    if records is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return records

@router.post(
    "/{project_id}/milestones",
    response_model=MilestoneResponse
)
def add_milestone(
    project_id: str,
    milestone_data: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_project_manager_or_admin),
):
    milestone = create_milestone(
        db,
        project_id,
        milestone_data
    )

    if not milestone:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return milestone

@router.get(
    "/{project_id}/milestones",
    response_model=list[MilestoneResponse]
)
def list_milestones(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    milestones = get_milestones(
        db,
        project_id
    )

    if milestones is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return milestones

