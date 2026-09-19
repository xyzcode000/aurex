from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectCreate


def valid_project_data():
    return {
        "name": "Test Highway Project",
        "description": "Test infrastructure project",
        "implementing_agency": "Test Agency",
        "location": "Chhattisgarh",
        "status": "ongoing",
        "approved_budget": Decimal("100000000"),
        "revised_budget": Decimal("110000000"),
        "expenditure": Decimal("40000000"),
        "planned_start_date": date(2026, 1, 1),
        "planned_end_date": date(2027, 1, 1),
        "actual_start_date": date(2026, 1, 15),
        "actual_end_date": None,
        "planned_progress": Decimal("50"),
        "actual_progress": Decimal("40"),
    }


def test_valid_project_is_accepted():
    project = ProjectCreate(**valid_project_data())

    assert project.name == "Test Highway Project"
    assert project.approved_budget == Decimal("100000000")
    assert project.actual_progress == Decimal("40")


def test_planned_end_date_before_start_date_is_rejected():
    data = valid_project_data()

    data["planned_end_date"] = date(2025, 12, 31)

    with pytest.raises(ValidationError):
        ProjectCreate(**data)


def test_actual_end_date_before_actual_start_date_is_rejected():
    data = valid_project_data()

    data["actual_end_date"] = date(2026, 1, 10)

    with pytest.raises(ValidationError):
        ProjectCreate(**data)


def test_negative_budget_is_rejected():
    data = valid_project_data()

    data["approved_budget"] = Decimal("-1")

    with pytest.raises(ValidationError):
        ProjectCreate(**data)


def test_progress_above_100_is_rejected():
    data = valid_project_data()

    data["actual_progress"] = Decimal("101")

    with pytest.raises(ValidationError):
        ProjectCreate(**data)