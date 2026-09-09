from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ScenarioRequest,
)

from app.services.project_service import (
    create_project,
    get_projects,
    get_project_by_id,
    update_project,
    delete_project,
)

from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.timeline_prediction import predict_completion_date
from app.services.risk_intelligence import analyze_risk
from app.services.scenario_intelligence import simulate_scenario
from app.services.predictive_intelligence import predict_final_cost
from app.services.early_warning import generate_early_warning
from app.services.investigation_engine import investigate_project
from app.services.unified_intelligence import generate_unified_intelligence


# =========================================================
# PROJECT ROUTER
# =========================================================

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)],
)


# =========================================================
# COMMON HELPERS
# =========================================================

def get_required_project(
    db: Session,
    project_id: int,
):
    """
    Fetch a project or raise a clean 404 error.
    """

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


def validate_timeline_data(project):
    """
    Timeline intelligence requires planned start
    and planned end dates.
    """

    missing_fields = []

    if project.planned_start_date is None:
        missing_fields.append("planned_start_date")

    if project.planned_end_date is None:
        missing_fields.append("planned_end_date")

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": (
                    "Timeline intelligence requires "
                    "the following project fields."
                ),
                "missing_fields": missing_fields,
            },
        )


# =========================================================
# CREATE PROJECT
# =========================================================

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


# =========================================================
# GET ALL PROJECTS
# =========================================================

@router.get(
    "",
    response_model=list[ProjectResponse],
)
def read_projects(
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of projects to skip",
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
        description="Maximum number of projects to return",
    ),
    db: Session = Depends(get_db),
):
    return get_projects(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# BUDGET INTELLIGENCE
# =========================================================

@router.get(
    "/{project_id}/intelligence/budget",
)
def budget_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    return analyze_budget(project)


# =========================================================
# TIMELINE INTELLIGENCE
# =========================================================

@router.get(
    "/{project_id}/intelligence/timeline",
)
def timeline_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    validate_timeline_data(project)

    return analyze_timeline(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=float(
            project.planned_progress or 0
        ),
        actual_progress=float(
            project.actual_progress or 0
        ),
    )


# =========================================================
# TIMELINE PREDICTION
# =========================================================

@router.get(
    "/{project_id}/intelligence/timeline-prediction",
)
def timeline_prediction(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    validate_timeline_data(project)

    return predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(
            project.actual_progress or 0
        ),
    )


# =========================================================
# RISK INTELLIGENCE
# =========================================================

@router.get(
    "/{project_id}/intelligence/risk",
)
def risk_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    return analyze_risk(project)


# =========================================================
# SCENARIO SIMULATION
# =========================================================

@router.post(
    "/{project_id}/intelligence/scenario",
)
def scenario_intelligence(
    scenario: ScenarioRequest,
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    validate_timeline_data(project)

    return simulate_scenario(
        project=project,
        budget_change_percent=scenario.budget_change_percent,
        delay_days=scenario.delay_days,
        progress_change_percent=scenario.progress_change_percent,
    )


# =========================================================
# COST PREDICTION
# =========================================================

@router.get(
    "/{project_id}/intelligence/prediction",
)
def predictive_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    return predict_final_cost(project)


# =========================================================
# EARLY WARNING
# =========================================================

@router.get(
    "/{project_id}/intelligence/early-warning",
)
def early_warning_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    validate_timeline_data(project)

    return generate_early_warning(project)


# =========================================================
# INVESTIGATION ENGINE
# =========================================================

@router.get(
    "/{project_id}/intelligence/investigation",
)
def investigation_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    validate_timeline_data(project)

    return investigate_project(project)


# =========================================================
# UNIFIED INTELLIGENCE
# =========================================================

@router.get(
    "/{project_id}/intelligence",
)
def unified_intelligence(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    validate_timeline_data(project)

    return generate_unified_intelligence(project)


# =========================================================
# GET SINGLE PROJECT
# =========================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def read_project(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    return get_required_project(
        db=db,
        project_id=project_id,
    )


# =========================================================
# UPDATE PROJECT
# =========================================================

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_existing_project(
    project_data: ProjectUpdate,
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    return update_project(
        db=db,
        project=project,
        project_data=project_data,
    )


# =========================================================
# DELETE PROJECT
# =========================================================

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_project(
    project_id: int = Path(
        ...,
        title="Project ID",
        description="Positive numeric project identifier",
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    project = get_required_project(
        db=db,
        project_id=project_id,
    )

    delete_project(
        db=db,
        project=project,
    )

    return None