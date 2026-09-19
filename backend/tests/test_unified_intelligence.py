from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.services.unified_intelligence import generate_unified_intelligence


def make_project(
    project_id=1,
    approved_budget=100000000,
    revised_budget=100000000,
    expenditure=40000000,
    planned_start_date=date(2026, 1, 1),
    planned_end_date=date(2027, 12, 31),
    actual_start_date=date(2026, 1, 1),
    actual_end_date=None,
    planned_progress=60,
    actual_progress=40,
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


# =========================================================
# TOP-LEVEL RESPONSE CONTRACT
# =========================================================


def test_unified_returns_expected_top_level_fields():
    project = make_project()

    result = generate_unified_intelligence(project)

    expected_fields = {
        "project_id",
        "project_health",
        "executive_summary",
        "executive_insights",
        "intelligence_status",
        "risk",
        "financial_intelligence",
        "timeline_intelligence",
        "early_warning",
        "investigation",
        "recommended_actions",
    }

    assert expected_fields.issubset(result.keys())


def test_unified_preserves_project_id():
    project = make_project(project_id=99)

    result = generate_unified_intelligence(project)

    assert result["project_id"] == 99


def test_unified_returns_valid_project_health():
    project = make_project()

    result = generate_unified_intelligence(project)

    assert result["project_health"] in {
        "low",
        "medium",
        "high",
        "critical",
    }


def test_unified_returns_executive_summary():
    project = make_project()

    result = generate_unified_intelligence(project)

    assert isinstance(result["executive_summary"], str)
    assert len(result["executive_summary"]) > 0


def test_unified_returns_executive_insights():
    project = make_project()

    result = generate_unified_intelligence(project)

    assert isinstance(result["executive_insights"], list)


# =========================================================
# RISK CONTRACT
# =========================================================


def test_unified_contains_risk_intelligence():
    project = make_project()

    result = generate_unified_intelligence(project)

    risk = result["risk"]

    assert isinstance(risk, dict)
    assert "score" in risk
    assert "level" in risk


def test_unified_risk_has_valid_score_and_level():
    project = make_project()

    result = generate_unified_intelligence(project)

    risk = result["risk"]

    assert 0 <= risk["score"] <= 100

    assert risk["level"] in {
        "low",
        "medium",
        "high",
        "critical",
    }


# =========================================================
# FINANCIAL INTELLIGENCE CONTRACT
# =========================================================


def test_unified_contains_financial_intelligence():
    project = make_project()

    result = generate_unified_intelligence(project)

    financial = result["financial_intelligence"]

    assert isinstance(financial, dict)
    assert "budget" in financial
    assert "cost_prediction" in financial


def test_unified_financial_prediction_is_consistent():
    project = make_project(
        revised_budget=90000000,
        expenditure=50000000,
        actual_progress=40,
    )

    result = generate_unified_intelligence(project)

    financial = result["financial_intelligence"]
    cost_prediction = financial["cost_prediction"]

    assert cost_prediction["projected_final_cost"] == 125000000
    assert cost_prediction["prediction_status"] == "critical"


# =========================================================
# TIMELINE INTELLIGENCE CONTRACT
# =========================================================


def test_unified_contains_timeline_intelligence():
    project = make_project()

    result = generate_unified_intelligence(project)

    timeline = result["timeline_intelligence"]

    assert isinstance(timeline, dict)
    assert "timeline" in timeline
    assert "timeline_prediction" in timeline


def test_unified_progress_gap_is_consistent():
    project = make_project(
        planned_progress=70,
        actual_progress=40,
    )

    result = generate_unified_intelligence(project)

    timeline = result["timeline_intelligence"]
    timeline_data = timeline["timeline"]

    assert timeline_data["progress_gap_percent"] == 30
    assert result["risk"]["score"] >= 0


# =========================================================
# EARLY WARNING CONTRACT
# =========================================================


def test_unified_contains_early_warning():
    project = make_project()

    result = generate_unified_intelligence(project)

    warning = result["early_warning"]

    assert isinstance(warning, dict)
    assert "priority" in warning
    assert "warnings" in warning
    assert "recommendations" in warning


# =========================================================
# INVESTIGATION CONTRACT
# =========================================================


def test_unified_contains_investigation():
    project = make_project()

    result = generate_unified_intelligence(project)

    investigation = result["investigation"]

    assert isinstance(investigation, dict)
    assert "investigation_status" in investigation
    assert "findings" in investigation
    assert "investigation_actions" in investigation


# =========================================================
# RECOMMENDED ACTIONS
# =========================================================


def test_unified_contains_recommended_actions():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = generate_unified_intelligence(project)

    assert isinstance(result["recommended_actions"], list)
    assert len(result["recommended_actions"]) > 0


def test_unified_high_risk_project_generates_actions():
    project = make_project(
        revised_budget=90000000,
        expenditure=60000000,
        planned_progress=80,
        actual_progress=30,
    )

    result = generate_unified_intelligence(project)

    assert result["risk"]["score"] >= 50
    assert len(result["recommended_actions"]) > 0
    assert len(result["early_warning"]["warnings"]) > 0
    assert len(result["investigation"]["findings"]) > 0


# =========================================================
# INTELLIGENCE STATUS CONTRACT
# =========================================================


def test_unified_intelligence_status_contains_all_engines():
    project = make_project()

    result = generate_unified_intelligence(project)

    status = result["intelligence_status"]

    assert "aggregate_risk" in status
    assert "financial_prediction" in status
    assert "timeline_prediction" in status
    assert "early_warning" in status
    assert "investigation" in status


def test_unified_intelligence_status_matches_main_results():
    project = make_project()

    result = generate_unified_intelligence(project)

    status = result["intelligence_status"]

    assert (
        status["aggregate_risk"]["score"]
        == result["risk"]["score"]
    )

    assert (
        status["aggregate_risk"]["level"]
        == result["risk"]["level"]
    )


# =========================================================
# CROSS-ENGINE CONTRACT TESTS
#
# These protect the relationships between the unified
# summary and the underlying intelligence results.
# =========================================================


def test_unified_financial_status_matches_cost_prediction():
    project = make_project(
        revised_budget=90000000,
        expenditure=50000000,
        actual_progress=40,
    )

    result = generate_unified_intelligence(project)

    unified_status = result["intelligence_status"][
        "financial_prediction"
    ]["status"]

    prediction_status = result[
        "financial_intelligence"
    ]["cost_prediction"]["prediction_status"]

    assert unified_status == prediction_status


def test_unified_timeline_status_matches_timeline_prediction():
    project = make_project()

    result = generate_unified_intelligence(project)

    unified_status = result["intelligence_status"][
        "timeline_prediction"
    ]["status"]

    prediction_status = result[
        "timeline_intelligence"
    ]["timeline_prediction"]["prediction_status"]

    assert unified_status == prediction_status


def test_unified_timeline_delay_matches_timeline_prediction():
    project = make_project()

    result = generate_unified_intelligence(project)

    unified_delay = result["intelligence_status"][
        "timeline_prediction"
    ]["predicted_delay_days"]

    prediction_delay = result[
        "timeline_intelligence"
    ]["timeline_prediction"]["predicted_delay_days"]

    assert unified_delay == prediction_delay


def test_unified_early_warning_status_matches_warning():
    project = make_project()

    result = generate_unified_intelligence(project)

    unified_status = result["intelligence_status"][
        "early_warning"
    ]["status"]

    warning_status = result[
        "early_warning"
    ]["overall_status"]

    assert unified_status == warning_status


def test_unified_early_warning_priority_matches_warning():
    project = make_project()

    result = generate_unified_intelligence(project)

    unified_priority = result["intelligence_status"][
        "early_warning"
    ]["priority"]

    warning_priority = result[
        "early_warning"
    ]["priority"]

    assert unified_priority == warning_priority


def test_unified_investigation_status_matches_investigation():
    project = make_project()

    result = generate_unified_intelligence(project)

    unified_status = result["intelligence_status"][
        "investigation"
    ]["status"]

    investigation_status = result[
        "investigation"
    ]["investigation_status"]

    assert unified_status == investigation_status


def test_unified_investigation_finding_count_is_consistent():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = generate_unified_intelligence(project)

    finding_count = result[
        "investigation"
    ]["finding_count"]

    findings_length = len(
        result["investigation"]["findings"]
    )

    unified_count = result[
        "intelligence_status"
    ]["investigation"]["finding_count"]

    assert finding_count == findings_length
    assert unified_count == finding_count


def test_unified_recommended_actions_match_early_warning():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = generate_unified_intelligence(project)

    assert (
        result["recommended_actions"]
        == result["early_warning"]["recommendations"]
    )


# =========================================================
# MANAGEMENT-READY RESPONSE
# =========================================================


def test_unified_returns_management_ready_response():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = generate_unified_intelligence(project)

    assert result["project_id"] == project.id

    assert result["project_health"] in {
        "low",
        "medium",
        "high",
        "critical",
    }

    assert isinstance(
        result["executive_summary"],
        str,
    )

    assert isinstance(
        result["executive_insights"],
        list,
    )

    assert isinstance(
        result["recommended_actions"],
        list,
    )