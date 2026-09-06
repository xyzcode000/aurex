from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


def calculate_risk_score(project: Project) -> float:
    score = 0.0

    # Financial risk
    if project.budget > 0:
        expenditure_ratio = (
            project.expenditure / project.budget
        ) * 100

        if expenditure_ratio > 90:
            score += 35
        elif expenditure_ratio > 75:
            score += 20

    # Progress risk
    if project.progress_percentage < 30:
        score += 25
    elif project.progress_percentage < 50:
        score += 15

    return min(score, 100)

def get_risk_explanation(project: Project) -> list[str]:
    explanations = []

    if project.budget > 0:
        expenditure_ratio = (
            project.expenditure / project.budget
        ) * 100

        if expenditure_ratio > 90:
            explanations.append(
                "Expenditure has crossed 90% of the allocated budget."
            )
        elif expenditure_ratio > 75:
            explanations.append(
                "Expenditure has crossed 75% of the allocated budget."
            )

    if project.progress_percentage < 30:
        explanations.append(
            "Project progress is below 30%."
        )
    elif project.progress_percentage < 50:
        explanations.append(
            "Project progress is below 50%."
        )

    if not explanations:
        explanations.append(
            "Project financial expenditure and progress are currently within the defined risk thresholds."
        )

    return explanations

def get_risk_level(score: float) -> str:
    if score <= 25:
        return "LOW"
    elif score <= 50:
        return "MEDIUM"
    elif score <= 75:
        return "HIGH"
    else:
        return "CRITICAL"


def create_project(
    db: Session,
    project_data: ProjectCreate
) -> Project:

    project = Project(**project_data.model_dump())

    db.add(project)
    db.commit()
    db.refresh(project)

    project.risk_score = calculate_risk_score(project)

    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session) -> list[Project]:
    return db.query(Project).all()


def get_project(
    db: Session,
    project_id: str
) -> Project | None:

    from uuid import UUID

def get_project(
    db: Session,
    project_id: str
) -> Project | None:

    # Try integer ID first
    try:
        internal_id = int(project_id)

        project = (
            db.query(Project)
            .filter(Project.id == internal_id)
            .first()
        )

        if project:
            return project

    except ValueError:
        pass

    # Try UUID
    try:
        public_id = UUID(project_id)

        return (
            db.query(Project)
            .filter(Project.public_id == public_id)
            .first()
        )

    except ValueError:
        return None