from decimal import Decimal
from types import SimpleNamespace

from app.services.predictive_intelligence import predict_final_cost


def make_project(
    project_id=1,
    approved_budget=100000000,
    revised_budget=110000000,
    expenditure=40000000,
    actual_progress=40,
):
    return SimpleNamespace(
        id=project_id,
        approved_budget=Decimal(str(approved_budget)),
        revised_budget=(
            Decimal(str(revised_budget))
            if revised_budget is not None
            else None
        ),
        expenditure=Decimal(str(expenditure)),
        actual_progress=Decimal(str(actual_progress)),
    )


def test_cost_prediction_calculates_projected_final_cost():
    project = make_project(
        expenditure=40000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["projected_final_cost"] == 100000000


def test_cost_prediction_calculates_projected_overrun():
    project = make_project(
        revised_budget=90000000,
        expenditure=40000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["projected_overrun"] == 10000000
    assert result["projected_overrun_percent"] == 11.11


def test_cost_prediction_status_is_low_when_within_budget():
    project = make_project(
        revised_budget=110000000,
        expenditure=40000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["prediction_status"] == "low"


def test_cost_prediction_status_is_high_when_above_110_percent():
    project = make_project(
        revised_budget=90000000,
        expenditure=40000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["projected_final_cost"] == 100000000
    assert result["prediction_status"] == "high"


def test_cost_prediction_status_is_critical_when_above_125_percent():
    project = make_project(
        revised_budget=90000000,
        expenditure=50000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["projected_final_cost"] == 125000000
    assert result["prediction_status"] == "critical"


def test_cost_prediction_status_is_critical_for_large_overrun():
    project = make_project(
        revised_budget=90000000,
        expenditure=60000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["projected_final_cost"] == 150000000
    assert result["prediction_status"] == "critical"


def test_cost_prediction_handles_insufficient_progress():
    project = make_project(
        expenditure=40000000,
        actual_progress=0,
    )

    result = predict_final_cost(project)

    assert result["projected_final_cost"] is None
    assert result["projected_overrun"] is None
    assert result["projected_overrun_percent"] is None
    assert result["prediction_status"] == "insufficient_data"


def test_cost_prediction_defaults_revised_budget_to_approved_budget():
    project = make_project(
        approved_budget=100000000,
        revised_budget=None,
        expenditure=40000000,
        actual_progress=40,
    )

    result = predict_final_cost(project)

    assert result["revised_budget"] == 100000000
    assert result["projected_final_cost"] == 100000000
    assert result["prediction_status"] == "low"