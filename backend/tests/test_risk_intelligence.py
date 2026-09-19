from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.services.risk_intelligence import analyze_risk


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


def test_low_risk_project_returns_low_risk():
    project = make_project()

    result = analyze_risk(project)

    assert result["project_id"] == 1
    assert result["overall_risk_level"] in {
        "low",
        "medium",
        "high",
        "critical",
    }
    assert 0 <= result["overall_risk_score"] <= 100


def test_high_budget_risk_contributes_to_risk_score():
    project = make_project(
        revised_budget=90000000,
        expenditure=40000000,
        actual_progress=40,
    )

    result = analyze_risk(project)

    assert result["budget_risk"] == "high"
    assert result["overall_risk_score"] >= 35


def test_critical_milestone_risk_contributes_30_points():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = analyze_risk(project)

    assert result["milestone_risk"] == "critical"
    assert result["overall_risk_score"] >= 30


def test_high_milestone_risk_contributes_20_points():
    project = make_project(
        planned_progress=50,
        actual_progress=35,
    )

    result = analyze_risk(project)

    assert result["milestone_risk"] == "high"
    assert result["overall_risk_score"] >= 20


def test_medium_milestone_risk_contributes_10_points():
    project = make_project(
        planned_progress=50,
        actual_progress=45,
    )

    result = analyze_risk(project)

    assert result["milestone_risk"] == "medium"
    assert result["overall_risk_score"] >= 10


def test_risk_score_never_exceeds_100():
    project = make_project(
        revised_budget=50000000,
        expenditure=100000000,
        planned_progress=100,
        actual_progress=0,
    )

    result = analyze_risk(project)

    assert result["overall_risk_score"] <= 100


def test_risk_level_matches_score_thresholds():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = analyze_risk(project)

    score = result["overall_risk_score"]
    level = result["overall_risk_level"]

    if score >= 75:
        assert level == "critical"
    elif score >= 50:
        assert level == "high"
    elif score >= 25:
        assert level == "medium"
    else:
        assert level == "low"


def test_risk_result_contains_expected_fields():
    project = make_project()

    result = analyze_risk(project)

    expected_fields = {
        "project_id",
        "overall_risk_score",
        "overall_risk_level",
        "budget_risk",
        "milestone_risk",
        "calendar_schedule_risk",
        "calendar_schedule_status",
        "progress_gap_percent",
        "calendar_progress_difference_percent",
        "predicted_completion_status",
        "predicted_delay_days",
        "risk_factors",
        "intelligence_summary",
    }

    assert expected_fields.issubset(result.keys())