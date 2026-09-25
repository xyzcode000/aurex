from datetime import date
from decimal import Decimal

from app.models.project_snapshot import ProjectSnapshot
from app.services.trajectory_intelligence import (
    calculate_historical_trajectory,
)


def make_snapshot(
    observation_date: date,
    planned_progress: str,
    actual_progress: str,
    expenditure: str,
):
    return ProjectSnapshot(
        project_id=1,
        observation_date=observation_date,
        snapshot_type="observation",
        implementing_agency="Test Agency",
        location="Chhattisgarh",
        status="in_progress",
        approved_budget=Decimal("100000000"),
        revised_budget=Decimal("110000000"),
        expenditure=Decimal(expenditure),
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 15),
        actual_end_date=None,
        planned_progress=Decimal(planned_progress),
        actual_progress=Decimal(actual_progress),
    )


def test_empty_snapshot_history():
    result = calculate_historical_trajectory([])

    assert result.observation_count == 0
    assert result.first_observation_date is None
    assert result.latest_observation_date is None
    assert result.progress_change == Decimal("0")
    assert result.expenditure_change == Decimal("0")
    assert result.progress_velocity is None
    assert result.expenditure_velocity is None
    assert result.progress_gap_change is None


def test_single_snapshot_has_no_velocity():
    snapshot = make_snapshot(
        date(2026, 1, 1),
        "20",
        "15",
        "10000000",
    )

    result = calculate_historical_trajectory([snapshot])

    assert result.observation_count == 1
    assert result.progress_change == Decimal("0")
    assert result.expenditure_change == Decimal("0")
    assert result.progress_velocity is None
    assert result.expenditure_velocity is None


def test_trajectory_calculates_changes():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "15",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "30",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second]
    )

    assert result.observation_count == 2

    assert result.progress_change == Decimal("15")
    assert result.expenditure_change == Decimal("15000000")

    assert result.first_observation_date == date(2026, 1, 1)
    assert result.latest_observation_date == date(2026, 2, 1)

    assert result.progress_velocity == (
        Decimal("15") / Decimal("31")
    )

    assert result.expenditure_velocity == (
        Decimal("15000000") / Decimal("31")
    )


def test_trajectory_calculates_progress_gap_change():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "15",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "30",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second]
    )

    # First gap: 20 - 15 = 5
    # Latest gap: 40 - 30 = 10
    # Change: 10 - 5 = +5
    assert result.progress_gap_change == Decimal("5")


def test_trajectory_orders_snapshots_by_date():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "15",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "30",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [second, first]
    )

    assert result.first_observation_date == date(2026, 1, 1)
    assert result.latest_observation_date == date(2026, 2, 1)


def test_progress_and_expenditure_trends():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "15",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "30",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second]
    )

    assert result.progress_trend == "increasing"
    assert result.expenditure_trend == "increasing"

def test_latest_velocity_uses_latest_observation_interval():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "10",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "25",
        "20000000",
    )

    third = make_snapshot(
        date(2026, 2, 11),
        "50",
        "35",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second, third]
    )

    assert result.latest_progress_velocity == (
        Decimal("10") / Decimal("10")
    )


def test_progress_acceleration_is_calculated():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "10",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "25",
        "20000000",
    )

    third = make_snapshot(
        date(2026, 2, 11),
        "50",
        "35",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second, third]
    )

    previous_velocity = Decimal("15") / Decimal("31")
    latest_velocity = Decimal("10") / Decimal("10")

    assert result.progress_acceleration == (
        latest_velocity - previous_velocity
    )


def test_latest_expenditure_velocity_is_calculated():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "10",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "40",
        "25",
        "20000000",
    )

    third = make_snapshot(
        date(2026, 2, 11),
        "50",
        "35",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second, third]
    )

    assert result.latest_expenditure_velocity == (
        Decimal("5000000") / Decimal("10")
    )
def test_schedule_trajectory_detects_falling_behind():
    first = make_snapshot(
        date(2026, 1, 1),
        "20",
        "15",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "50",
        "35",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second]
    )

    assert result.schedule_trajectory == "falling_behind"


def test_schedule_trajectory_detects_catching_up():
    first = make_snapshot(
        date(2026, 1, 1),
        "50",
        "30",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "70",
        "60",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second]
    )

    assert result.schedule_trajectory == "catching_up"


def test_schedule_trajectory_detects_stable_gap():
    first = make_snapshot(
        date(2026, 1, 1),
        "30",
        "20",
        "10000000",
    )

    second = make_snapshot(
        date(2026, 2, 1),
        "50",
        "40",
        "25000000",
    )

    result = calculate_historical_trajectory(
        [first, second]
    )

    assert result.schedule_trajectory == "stable"