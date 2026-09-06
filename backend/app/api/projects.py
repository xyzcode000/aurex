from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ScenarioRequest,
)

from app.services.project_service import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects,
    update_project,
)

from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk
from app.services.scenario_intelligence import simulate_scenario
from app.services.predictive_intelligence import predict_final_cost
from app.services.timeline_prediction import predict_completion_date
from app.services.early_warning import generate_early_warning
from app.services.investigation_engine import investigate_project
from app.services.unified_intelligence import generate_unified_intelligence


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
# AUREX TIMELINE INTELLIGENCE
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/timeline",
)
def get_timeline_intelligence(
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

    return analyze_timeline(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=float(project.planned_progress),
        actual_progress=float(project.actual_progress),
    )


# -------------------------------------------------
# AUREX TIMELINE PREDICTION INTELLIGENCE
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/timeline-prediction",
)
def get_timeline_prediction(
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

    return predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(project.actual_progress),
    )


# -------------------------------------------------
# AUREX RISK INTELLIGENCE
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/risk",
)
def get_risk_intelligence(
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

    return analyze_risk(project)


# -------------------------------------------------
# AUREX SCENARIO SIMULATION ENGINE
# -------------------------------------------------

@router.post(
    "/{project_id}/intelligence/scenario",
)
def run_scenario_simulation(
    project_id: int,
    scenario_data: ScenarioRequest,
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

    return simulate_scenario(
        project=project,
        budget_change_percent=scenario_data.budget_change_percent,
        delay_days=scenario_data.delay_days,
        progress_change_percent=scenario_data.progress_change_percent,
    )


# -------------------------------------------------
# AUREX PREDICTIVE COST INTELLIGENCE
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/prediction",
)
def get_cost_prediction(
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

    return predict_final_cost(project)


# -------------------------------------------------
# AUREX EARLY WARNING ENGINE
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/early-warning",
)
def get_early_warning(
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

    return generate_early_warning(project)


# -------------------------------------------------
# AUREX INVESTIGATION & ROOT-CAUSE ENGINE
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence/investigation",
)
def get_project_investigation(
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

    return investigate_project(project)


# -------------------------------------------------
# AUREX UNIFIED INTELLIGENCE ENGINE
# -------------------------------------------------
#
# This is the MASTER AUREX intelligence endpoint.
#
# It combines:
# Budget
# Timeline
# Risk
# Cost Prediction
# Timeline Prediction
# Early Warning
# Investigation
#
# -------------------------------------------------

@router.get(
    "/{project_id}/intelligence",
)
def get_unified_intelligence(
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

    return generate_unified_intelligence(project)


# -------------------------------------------------
# GET SINGLE PROJECT
# IMPORTANT:
# Keep this after all intelligence routes
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