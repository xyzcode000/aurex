from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.services.early_warning import generate_early_warning


def make_project(
    project_id=1,
    approved_budget=100000000,
    revised_budget=100000000,
    expenditure=10000000,
    planned_start_date=date(2026, 1, 1),
    planned_end_date=date(2027, 12, 31),
    actual_start_date=date(2026, 1, 1),
    actual_end_date=None,
    planned_progress=20,
    actual_progress=20,
):
    return SimpleNamespace(
        id=project_id,
        approved_budget=Decimal(str(approved_budget)),
        revised_budget=Decimal(str(revised_budget)),
        expenditure=Decimal(str(expenditure)),
        planned_start_date=planned_start_date,
        planned_end_date=planned_end_date,
        actual_start_date=actual_start_date,
        actual_end_date=actual_end_date,
        planned_progress=Decimal(str(planned_progress)),
        actual_progress=Decimal(str(actual_progress)),
    )


def test_early_warning_returns_expected_top_level_fields():
    project = make_project()

    result = generate_early_warning(project)

    expected_fields = {
        "project_id",
        "overall_status",
        "priority",
        "risk_score",
        "warnings",
        "recommendations",
        "executive_summary",
        "intelligence",
    }

    assert expected_fields.issubset(result.keys())


def test_early_warning_returns_project_id():
    project = make_project(project_id=42)

    result = generate_early_warning(project)

    assert result["project_id"] == 42


def test_early_warning_detects_high_financial_risk():
    project = make_project(
        revised_budget=90000000,
        expenditure=40000000,
        actual_progress=40,
        planned_progress=40,
    )

    result = generate_early_warning(project)

    assert result["intelligence"]["budget"]["budget_risk"] == "high"
    assert len(result["warnings"]) > 0


def test_early_warning_detects_progress_gap():
    project = make_project(
        planned_progress=70,
        actual_progress=40,
    )

    result = generate_early_warning(project)

    assert result["intelligence"]["timeline"]["progress_gap_percent"] == 30
    assert len(result["warnings"]) > 0


def test_early_warning_detects_confirmed_delay():
    project = make_project(
        planned_start_date=date(2025, 1, 1),
        planned_end_date=date(2026, 1, 1),
        actual_start_date=date(2025, 1, 1),
        actual_end_date=date(2026, 4, 15),
        planned_progress=100,
        actual_progress=100,
    )

    result = generate_early_warning(project)

    assert len(result["warnings"]) > 0


def test_early_warning_contains_recommendations_for_risk():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = generate_early_warning(project)

    assert len(result["recommendations"]) > 0


def test_early_warning_priority_is_valid():
    project = make_project()

    result = generate_early_warning(project)

    assert result["priority"] in {
        "routine_monitoring",
        "monitor_closely",
        "urgent_attention",
        "immediate_action",
    }


def test_early_warning_status_is_valid():
    project = make_project()

    result = generate_early_warning(project)

    assert result["overall_status"] in {
        "low",
        "medium",
        "high",
        "critical",
    }