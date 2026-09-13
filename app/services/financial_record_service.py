from sqlalchemy.orm import Session

from app.models.financial_record import FinancialRecord
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordResponse
)
from app.services.project_service import get_project


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

    # Save to database
    db.add(record)
    db.commit()
    db.refresh(record)

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