from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.services.scenario_intelligence import simulate_scenario


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


def test_scenario_returns_expected_top_level_fields():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=30,
        progress_change_percent=5,
    )

    expected_fields = {
        "project_id",
        "scenario",
        "current_state",
        "simulated_state",
        "comparison",
        "scenario_summary",
        "recommendation",
    }

    assert expected_fields.issubset(result.keys())


def test_scenario_preserves_project_id():
    project = make_project(project_id=99)

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=30,
        progress_change_percent=5,
    )

    assert result["project_id"] == 99


def test_scenario_records_input_parameters():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=45,
        progress_change_percent=-5,
    )

    scenario = result["scenario"]

    assert scenario["budget_change_percent"] == 10
    assert scenario["delay_days"] == 45
    assert scenario["progress_change_percent"] == -5


def test_budget_increase_changes_simulated_budget():
    project = make_project(
        approved_budget=100000000,
        revised_budget=100000000,
    )

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=0,
        progress_change_percent=0,
    )

    simulated_budget = result["simulated_state"]["budget"]

    assert simulated_budget["approved_budget"] == 110000000
    assert simulated_budget["revised_budget"] == 110000000


def test_budget_decrease_changes_simulated_budget():
    project = make_project(
        approved_budget=100000000,
        revised_budget=100000000,
    )

    result = simulate_scenario(
        project,
        budget_change_percent=-10,
        delay_days=0,
        progress_change_percent=0,
    )

    simulated_budget = result["simulated_state"]["budget"]

    assert simulated_budget["approved_budget"] == 90000000
    assert simulated_budget["revised_budget"] == 90000000


def test_progress_change_affects_simulated_progress():
    project = make_project(actual_progress=40)

    result = simulate_scenario(
        project,
        budget_change_percent=0,
        delay_days=0,
        progress_change_percent=10,
    )

    simulated_budget = result["simulated_state"]["budget"]
    simulated_timeline = result["simulated_state"]["timeline"]
    simulated_cost = result["simulated_state"]["cost_prediction"]

    assert simulated_budget["actual_progress_percent"] == 50
    assert simulated_timeline["actual_progress_percent"] == 50
    assert simulated_cost["actual_progress_percent"] == 50


def test_delay_is_recorded_as_scenario_effect():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=0,
        delay_days=90,
        progress_change_percent=0,
    )

    assert result["scenario"]["delay_days"] == 90

    risk = result["simulated_state"]["risk"]

    assert risk["scenario_delay_risk"] == "high"
    assert risk["scenario_delay_risk_points"] == 20


def test_original_project_is_not_mutated():
    project = make_project(
        approved_budget=100000000,
        revised_budget=100000000,
        actual_progress=40,
    )

    original_approved = project.approved_budget
    original_revised = project.revised_budget
    original_progress = project.actual_progress

    simulate_scenario(
        project,
        budget_change_percent=20,
        delay_days=90,
        progress_change_percent=15,
    )

    assert project.approved_budget == original_approved
    assert project.revised_budget == original_revised
    assert project.actual_progress == original_progress


def test_scenario_contains_current_state():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=30,
        progress_change_percent=5,
    )

    current = result["current_state"]

    assert current is not None
    assert "risk" in current
    assert "budget" in current
    assert "cost_prediction" in current
    assert "timeline_prediction" in current


def test_scenario_contains_simulated_state():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=30,
        progress_change_percent=5,
    )

    simulated = result["simulated_state"]

    assert simulated is not None
    assert "risk" in simulated
    assert "budget" in simulated
    assert "timeline" in simulated
    assert "cost_prediction" in simulated
    assert "timeline_prediction" in simulated


def test_scenario_contains_comparison():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=30,
        progress_change_percent=5,
    )

    comparison = result["comparison"]

    assert "risk_change" in comparison
    assert "financial_impact" in comparison
    assert "timeline_impact" in comparison
    assert "risk_impact" in comparison
    assert "health_change" in comparison


def test_scenario_contains_recommendation_and_summary():
    project = make_project()

    result = simulate_scenario(
        project,
        budget_change_percent=10,
        delay_days=30,
        progress_change_percent=-5,
    )

    assert isinstance(result["scenario_summary"], str)
    assert len(result["scenario_summary"]) > 0

    assert isinstance(result["recommendation"], str)
    assert len(result["recommendation"]) > 0