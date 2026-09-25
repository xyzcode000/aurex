from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.models.project_snapshot import ProjectSnapshot


@dataclass(frozen=True)
class HistoricalTrajectory:
    observation_count: int

    first_observation_date: date | None
    latest_observation_date: date | None

    progress_change: Decimal
    expenditure_change: Decimal

    progress_velocity: Decimal | None
    latest_progress_velocity: Decimal | None

    expenditure_velocity: Decimal | None
    latest_expenditure_velocity: Decimal | None

    progress_acceleration: Decimal | None

    progress_gap_change: Decimal | None

    progress_trend: str
    expenditure_trend: str
    progress_direction: str

    schedule_trajectory: str


def _calculate_trend(change: Decimal) -> str:
    if change > 0:
        return "increasing"

    if change < 0:
        return "decreasing"

    return "stable"


def _calculate_velocity(
    earlier: ProjectSnapshot,
    later: ProjectSnapshot,
) -> Decimal | None:
    elapsed_days = (
        later.observation_date
        - earlier.observation_date
    ).days

    if elapsed_days <= 0:
        return None

    progress_change = (
        later.actual_progress
        - earlier.actual_progress
    )

    return progress_change / Decimal(elapsed_days)


def _calculate_expenditure_velocity(
    earlier: ProjectSnapshot,
    later: ProjectSnapshot,
) -> Decimal | None:
    elapsed_days = (
        later.observation_date
        - earlier.observation_date
    ).days

    if elapsed_days <= 0:
        return None

    expenditure_change = (
        later.expenditure
        - earlier.expenditure
    )

    return expenditure_change / Decimal(elapsed_days)


def _calculate_schedule_trajectory(
    gap_change: Decimal | None,
) -> str:
    if gap_change is None:
        return "unknown"

    if gap_change < 0:
        return "catching_up"

    if gap_change > 0:
        return "falling_behind"

    return "stable"


def calculate_historical_trajectory(
    snapshots: list[ProjectSnapshot],
) -> HistoricalTrajectory:

    if not snapshots:
        return HistoricalTrajectory(
            observation_count=0,
            first_observation_date=None,
            latest_observation_date=None,
            progress_change=Decimal("0"),
            expenditure_change=Decimal("0"),
            progress_velocity=None,
            latest_progress_velocity=None,
            expenditure_velocity=None,
            latest_expenditure_velocity=None,
            progress_acceleration=None,
            progress_gap_change=None,
            progress_trend="stable",
            expenditure_trend="stable",
            progress_direction="stable",
            schedule_trajectory="unknown",
        )

    ordered_snapshots = sorted(
        snapshots,
        key=lambda snapshot: snapshot.observation_date,
    )

    first = ordered_snapshots[0]
    latest = ordered_snapshots[-1]

    progress_change = (
        latest.actual_progress
        - first.actual_progress
    )

    expenditure_change = (
        latest.expenditure
        - first.expenditure
    )

    elapsed_days = (
        latest.observation_date
        - first.observation_date
    ).days

    if elapsed_days > 0:
        progress_velocity = (
            progress_change / Decimal(elapsed_days)
        )

        expenditure_velocity = (
            expenditure_change / Decimal(elapsed_days)
        )
    else:
        progress_velocity = None
        expenditure_velocity = None

    latest_progress_velocity = None
    latest_expenditure_velocity = None
    progress_acceleration = None

    if len(ordered_snapshots) >= 2:
        previous = ordered_snapshots[-2]

        latest_progress_velocity = _calculate_velocity(
            previous,
            latest,
        )

        latest_expenditure_velocity = (
            _calculate_expenditure_velocity(
                previous,
                latest,
            )
        )

    if len(ordered_snapshots) >= 3:
        previous = ordered_snapshots[-2]
        before_previous = ordered_snapshots[-3]

        previous_velocity = _calculate_velocity(
            before_previous,
            previous,
        )

        if (
            previous_velocity is not None
            and latest_progress_velocity is not None
        ):
            progress_acceleration = (
                latest_progress_velocity
                - previous_velocity
            )

    first_progress_gap = (
        first.planned_progress
        - first.actual_progress
    )

    latest_progress_gap = (
        latest.planned_progress
        - latest.actual_progress
    )

    progress_gap_change = (
        latest_progress_gap
        - first_progress_gap
    )

    return HistoricalTrajectory(
        observation_count=len(ordered_snapshots),
        first_observation_date=first.observation_date,
        latest_observation_date=latest.observation_date,
        progress_change=progress_change,
        expenditure_change=expenditure_change,
        progress_velocity=progress_velocity,
        latest_progress_velocity=latest_progress_velocity,
        expenditure_velocity=expenditure_velocity,
        latest_expenditure_velocity=latest_expenditure_velocity,
        progress_acceleration=progress_acceleration,
        progress_gap_change=progress_gap_change,
        progress_trend=_calculate_trend(progress_change),
        expenditure_trend=_calculate_trend(expenditure_change),
        progress_direction=_calculate_trend(
            latest_progress_velocity
            if latest_progress_velocity is not None
            else progress_change
        ),
        schedule_trajectory=_calculate_schedule_trajectory(
            progress_gap_change
        ),
    )