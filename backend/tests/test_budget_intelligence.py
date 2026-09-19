from types import SimpleNamespace
from decimal import Decimal

from app.services.budget_intelligence import analyze_budget


def make_project(
    approved_budget=100000000,
    revised_budget=110000000,
    expenditure=40000000,
    planned_progress=50,
    actual_progress=40,
):
    return SimpleNamespace(
        approved_budget=Decimal(str(approved_budget)),
        revised_budget=(
            Decimal(str(revised_budget))
            if revised_budget is not None
            else None
        ),
        expenditure=Decimal(str(expenditure)),
        planned_progress=Decimal(str(planned_progress)),
        actual_progress=Decimal(str(actual_progress)),
    )


def test_budget_analysis_calculates_budget_difference():
    project = make_project(
        approved_budget=100000000,
        revised_budget=110000000,
    )

    result = analyze_budget(project)

    assert result["budget_difference"] == 10000000
    assert result["budget_change_percent"] == 10


def test_budget_analysis_calculates_progress_gap():
    project = make_project(
        planned_progress=60,
        actual_progress=40,
    )

    result = analyze_budget(project)

    assert result["spending_progress_gap"] == -20


def test_budget_analysis_projects_expenditure_from_progress():
    project = make_project(
        expenditure=40000000,
        actual_progress=40,
    )

    result = analyze_budget(project)

    assert result["projected_expenditure"] == 100000000


def test_budget_risk_is_high_when_projected_expenditure_exceeds_revised_budget():
    project = make_project(
        revised_budget=90000000,
        expenditure=40000000,
        actual_progress=40,
    )

    result = analyze_budget(project)

    assert result["projected_expenditure"] == 100000000
    assert result["budget_risk"] == "high"


def test_budget_risk_is_medium_when_projected_expenditure_is_above_90_percent():
    project = make_project(
        revised_budget=100000000,
        expenditure=37000000,
        actual_progress=40,
    )

    result = analyze_budget(project)

    assert result["projected_expenditure"] == 92500000
    assert result["budget_risk"] == "medium"


def test_budget_risk_is_low_when_projected_expenditure_is_below_90_percent():
    project = make_project(
        revised_budget=100000000,
        expenditure=30000000,
        actual_progress=40,
    )

    result = analyze_budget(project)

    assert result["projected_expenditure"] == 75000000
    assert result["budget_risk"] == "low"


def test_revised_budget_defaults_to_approved_budget():
    project = make_project(
        approved_budget=100000000,
        revised_budget=None,
    )

    result = analyze_budget(project)

    assert result["revised_budget"] == 100000000
    assert result["budget_difference"] == 0
    assert result["budget_change_percent"] == 0