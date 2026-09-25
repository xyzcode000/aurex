from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.project_snapshot import ProjectSnapshot


def _to_float(value: Decimal | int | float | None) -> float | None:
    """Convert Decimal/numeric database values into JSON/ML-friendly floats."""
    if value is None:
        return None

    return float(value)


def _percentage_change(
    current: float | None,
    baseline: float | None,
) -> float:
    """
    Calculate percentage change from baseline.

    Returns 0 when the baseline is unavailable or non-positive.
    """
    if current is None or baseline is None or baseline <= 0:
        return 0.0

    return ((current - baseline) / baseline) * 100.0


def _calculate_elapsed_days(
    observation_date: date,
    actual_start_date: date | None,
) -> int | None:
    """Calculate execution days known as of the observation date."""
    if actual_start_date is None:
        return None

    return max(
        (observation_date - actual_start_date).days,
        0,
    )


def _calculate_planned_duration_days(
    planned_start_date: date | None,
    planned_end_date: date | None,
) -> int | None:
    """Calculate the project's planned duration."""
    if planned_start_date is None or planned_end_date is None:
        return None

    return max(
        (planned_end_date - planned_start_date).days,
        0,
    )


def _calculate_remaining_planned_days(
    observation_date: date,
    planned_end_date: date | None,
) -> int | None:
    """
    Calculate remaining planned days at the observation date.

    Negative values are clamped to zero because a project cannot
    have negative remaining planned duration.
    """
    if planned_end_date is None:
        return None

    return max(
        (planned_end_date - observation_date).days,
        0,
    )


def _build_features(
    snapshot: ProjectSnapshot,
) -> dict[str, Any]:
    """
    Build features using only information contained in the observation
    snapshot.

    Future snapshot information must never enter this function.
    """
    approved_budget = _to_float(snapshot.approved_budget)
    revised_budget = _to_float(snapshot.revised_budget)
    expenditure = _to_float(snapshot.expenditure)
    planned_progress = _to_float(snapshot.planned_progress)
    actual_progress = _to_float(snapshot.actual_progress)

    effective_budget = (
        revised_budget
        if revised_budget is not None
        else approved_budget
    )

    progress_gap = None

    if planned_progress is not None and actual_progress is not None:
        progress_gap = planned_progress - actual_progress

    expenditure_ratio = None

    if (
        expenditure is not None
        and effective_budget is not None
        and effective_budget > 0
    ):
        expenditure_ratio = (
            expenditure / effective_budget
        )

    return {
        "project_id": snapshot.project_id,
        "observation_date": snapshot.observation_date,

        # Financial features
        "approved_budget": approved_budget,
        "revised_budget": revised_budget,
        "expenditure": expenditure,
        "budget_change_percent": _percentage_change(
            revised_budget,
            approved_budget,
        ),
        "expenditure_ratio": expenditure_ratio,
        "has_revision": (
            1
            if revised_budget is not None
            else 0
        ),

        # Progress features
        "planned_progress": planned_progress,
        "actual_progress": actual_progress,
        "progress_gap": progress_gap,

        # Timeline features
        "planned_duration_days": _calculate_planned_duration_days(
            snapshot.planned_start_date,
            snapshot.planned_end_date,
        ),
        "elapsed_days": _calculate_elapsed_days(
            snapshot.observation_date,
            snapshot.actual_start_date,
        ),
        "remaining_planned_days": _calculate_remaining_planned_days(
            snapshot.observation_date,
            snapshot.planned_end_date,
        ),

        # Context features
        "status": snapshot.status,
        "implementing_agency": snapshot.implementing_agency,
        "location": snapshot.location,
    }


def _is_completed_snapshot(
    snapshot: ProjectSnapshot,
) -> bool:
    """
    Determine whether a snapshot contains a usable completed-project
    outcome.

    We require either:
    - actual progress >= 100%, or
    - an actual completion date.
    """
    actual_progress = _to_float(snapshot.actual_progress)

    return bool(
        (
            actual_progress is not None
            and actual_progress >= 100.0
        )
        or snapshot.actual_end_date is not None
    )


def _calculate_future_cost_overrun_percent(
    final_snapshot: ProjectSnapshot,
) -> float | None:
    """
    Calculate final expenditure overrun against the effective
    final/revised budget.

    The target is only calculated when a valid budget exists.
    """
    final_expenditure = _to_float(
        final_snapshot.expenditure
    )

    revised_budget = _to_float(
        final_snapshot.revised_budget
    )

    approved_budget = _to_float(
        final_snapshot.approved_budget
    )

    effective_budget = (
        revised_budget
        if revised_budget is not None
        else approved_budget
    )

    if (
        final_expenditure is None
        or effective_budget is None
        or effective_budget <= 0
    ):
        return None

    return max(
        ((final_expenditure - effective_budget) / effective_budget)
        * 100.0,
        0.0,
    )


def _calculate_future_time_overrun_days(
    final_snapshot: ProjectSnapshot,
) -> int | None:
    """
    Calculate final schedule overrun.

    A positive value means completion occurred after the planned
    completion date.
    """
    if (
        final_snapshot.actual_end_date is None
        or final_snapshot.planned_end_date is None
    ):
        return None

    return max(
        (
            final_snapshot.actual_end_date
            - final_snapshot.planned_end_date
        ).days,
        0,
    )


def _find_future_completed_snapshot(
    snapshots: list[ProjectSnapshot],
    observation_index: int,
) -> ProjectSnapshot | None:
    """
    Find the first strictly later completed snapshot.

    This is the core temporal-leakage protection rule.
    """
    observation_date = snapshots[
        observation_index
    ].observation_date

    for future_snapshot in snapshots[
        observation_index + 1 :
    ]:
        if future_snapshot.observation_date <= observation_date:
            continue

        if _is_completed_snapshot(future_snapshot):
            return future_snapshot

    return None


def build_project_training_rows(
    snapshots: list[ProjectSnapshot],
) -> list[dict[str, Any]]:
    """
    Build leakage-safe ML training rows for one project.

    Every row represents a historical observation whose target
    comes from a strictly later completed snapshot.
    """
    ordered_snapshots = sorted(
        snapshots,
        key=lambda snapshot: (
            snapshot.observation_date,
            snapshot.id,
        ),
    )

    rows: list[dict[str, Any]] = []

    for index, snapshot in enumerate(
        ordered_snapshots
    ):
        future_snapshot = _find_future_completed_snapshot(
            ordered_snapshots,
            index,
        )

        if future_snapshot is None:
            continue

        future_cost_overrun = (
            _calculate_future_cost_overrun_percent(
                future_snapshot
            )
        )

        future_time_overrun = (
            _calculate_future_time_overrun_days(
                future_snapshot
            )
        )

        if (
            future_cost_overrun is None
            or future_time_overrun is None
        ):
            continue

        features = _build_features(snapshot)

        rows.append(
            {
                **features,

                # Future labels
                "future_cost_overrun_percent": (
                    future_cost_overrun
                ),
                "future_time_overrun_days": (
                    future_time_overrun
                ),
            }
        )

    return rows


def build_training_dataset(
    db: Session,
) -> list[dict[str, Any]]:
    """
    Build the complete leakage-safe training dataset.

    Projects are processed independently so that future information
    from one project can never become the target of another project.
    """
    project_ids = [
        project_id
        for (project_id,) in (
            db.query(
                ProjectSnapshot.project_id
            )
            .distinct()
            .order_by(
                ProjectSnapshot.project_id.asc()
            )
            .all()
        )
    ]

    dataset: list[dict[str, Any]] = []

    for project_id in project_ids:
        snapshots = (
            db.query(ProjectSnapshot)
            .filter(
                ProjectSnapshot.project_id
                == project_id
            )
            .order_by(
                ProjectSnapshot.observation_date.asc(),
                ProjectSnapshot.id.asc(),
            )
            .all()
        )

        dataset.extend(
            build_project_training_rows(
                snapshots
            )
        )

    return dataset