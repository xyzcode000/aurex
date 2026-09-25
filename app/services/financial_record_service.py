from sqlalchemy.orm import Session

from app.models.financial_record import FinancialRecord
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordResponse
)
from app.services.project_service import (
    get_project,
    calculate_risk_score
)


def create_financial_record(
    db: Session,
    project_id: str,
    record_data: FinancialRecordCreate
) -> FinancialRecord | None:

    # Find the project using either internal ID or public UUID
    project = get_project(db, project_id)

    if not project:
        return None

    # Create financial record
    record = FinancialRecord(
        project_id=project.id,
        **record_data.model_dump()
    )

    # Save financial record
    db.add(record)
    db.commit()
    db.refresh(record)

    # Update project's total expenditure
    project.expenditure += float(record.expenditure)  

    # Recalculate project risk score
    project.risk_score = calculate_risk_score(project)

    # Save updated project
    db.commit()
    db.refresh(project)

    return record


def get_financial_records(
    db: Session,
    project_id: str
) -> list[FinancialRecord] | None:

    # Find the project using either internal ID or public UUID
    project = get_project(db, project_id)

    if not project:
        return None

    # Get all financial records for this project
    records = (
        db.query(FinancialRecord)
        .filter(FinancialRecord.project_id == project.id)
        .order_by(FinancialRecord.record_date.desc())
        .all()
    )

    return records