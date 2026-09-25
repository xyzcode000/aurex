from datetime import date
from decimal import Decimal

from app.ml.dataset_builder import (
    build_project_training_rows,
)
from app.models.project_snapshot import ProjectSnapshot


def make_snapshot(
    *,
    snapshot_id: int,
    project_id: int,
    observation_date: date,
    approved_budget: str = "100000000",
    revised_budget: str | None = "110000000",
    expenditure: str = "40000000",
    planned_progress: str = "50",
    actual_progress: str = "40",
    planned_start_date: date = date(2026, 1, 1),
    planned_end_date: date = date(2027, 1, 1),
    actual_start_date: date | None = date(2026, 1, 15),
    actual_end_date: date | None = None,
    status: str = "in_progress",
):
    return ProjectSnapshot(
        id=snapshot_id,
        project_id=project_id,
        observation_date=observation_date,
        implementing_agency="Test Agency",
        location="Chhattisgarh",
        status=status,
        approved_budget=Decimal(approved_budget),
        revised_budget=(
            Decimal(revised_budget)
            if revised_budget is not None
            else None
        ),
        expenditure=Decimal(expenditure),
        planned_start_date=planned_start_date,
        planned_end_date=planned_end_date,
        actual_start_date=actual_start_date,
        actual_end_date=actual_end_date,
        planned_progress=Decimal(planned_progress),
        actual_progress=Decimal(actual_progress),
    )


def test_training_row_uses_observation_snapshot_features():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
            expenditure="40000000",
            planned_progress="45",
            actual_progress="35",
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            expenditure="125000000",
            planned_progress="100",
            actual_progress="100",
            actual_end_date=date(2027, 3, 31),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1

    row = rows[0]

    assert row["observation_date"] == date(2026, 3, 31)
    assert row["expenditure"] == 40000000.0
    assert row["planned_progress"] == 45.0
    assert row["actual_progress"] == 35.0
    assert row["progress_gap"] == 10.0


def test_future_cost_overrun_is_calculated_from_future_snapshot():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            expenditure="125000000",
            planned_progress="100",
            actual_progress="100",
            actual_end_date=date(2027, 3, 31),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1

    # (125 - 110) / 110 * 100
    expected = (
        (125000000 - 110000000)
        / 110000000
        * 100
    )

    assert rows[0]["future_cost_overrun_percent"] == expected


def test_future_time_overrun_is_calculated_from_future_snapshot():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            expenditure="110000000",
            planned_progress="100",
            actual_progress="100",
            actual_end_date=date(2027, 4, 1),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1

    assert rows[0]["future_time_overrun_days"] == 90


def test_incomplete_future_snapshot_is_not_used_as_label():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            expenditure="120000000",
            actual_progress="80",
            actual_end_date=None,
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert rows == []


def test_completed_snapshot_can_be_identified_by_100_percent_progress():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            expenditure="110000000",
            actual_progress="100",
            actual_end_date=None,
        ),
    ]

    rows = build_project_training_rows(snapshots)

    # Time target cannot be calculated without actual_end_date,
    # so the row must still be excluded.
    assert rows == []


def test_missing_revised_budget_falls_back_to_approved_budget():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
            approved_budget="100000000",
            revised_budget=None,
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            approved_budget="100000000",
            revised_budget=None,
            expenditure="120000000",
            actual_progress="100",
            actual_end_date=date(2027, 1, 1),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1

    assert rows[0]["future_cost_overrun_percent"] == 20.0


def test_future_snapshot_must_be_strictly_later():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 3, 31),
            expenditure="120000000",
            actual_progress="100",
            actual_end_date=date(2027, 2, 1),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert rows == []


def test_snapshots_are_processed_chronologically():
    snapshots = [
        make_snapshot(
            snapshot_id=3,
            project_id=1,
            observation_date=date(2026, 12, 31),
            expenditure="120000000",
            actual_progress="100",
            actual_end_date=date(2027, 2, 1),
        ),
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 6, 30),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 2

    assert rows[0]["observation_date"] == date(2026, 3, 31)
    assert rows[1]["observation_date"] == date(2026, 6, 30)


def test_progress_gap_is_planned_minus_actual():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
            planned_progress="70",
            actual_progress="45",
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            actual_progress="100",
            actual_end_date=date(2027, 1, 1),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1
    assert rows[0]["progress_gap"] == 25.0


def test_budget_change_percent_is_calculated():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
            approved_budget="100000000",
            revised_budget="120000000",
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            actual_progress="100",
            actual_end_date=date(2027, 1, 1),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1
    assert rows[0]["budget_change_percent"] == 20.0
    assert rows[0]["has_revision"] == 1


def test_expenditure_ratio_uses_effective_budget():
    snapshots = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
            revised_budget="120000000",
            expenditure="60000000",
        ),
        make_snapshot(
            snapshot_id=2,
            project_id=1,
            observation_date=date(2026, 12, 31),
            actual_progress="100",
            actual_end_date=date(2027, 1, 1),
        ),
    ]

    rows = build_project_training_rows(snapshots)

    assert len(rows) == 1

    assert rows[0]["expenditure_ratio"] == 0.5


def test_different_projects_are_independent():
    project_one = [
        make_snapshot(
            snapshot_id=1,
            project_id=1,
            observation_date=date(2026, 3, 31),
        ),
    ]

    project_two = [
        make_snapshot(
            snapshot_id=2,
            project_id=2,
            observation_date=date(2026, 3, 31),
        ),
        make_snapshot(
            snapshot_id=3,
            project_id=2,
            observation_date=date(2026, 12, 31),
            actual_progress="100",
            actual_end_date=date(2027, 1, 1),
        ),
    ]

    rows_one = build_project_training_rows(project_one)
    rows_two = build_project_training_rows(project_two)

    assert rows_one == []
    assert len(rows_two) == 1
    assert rows_two[0]["project_id"] == 2