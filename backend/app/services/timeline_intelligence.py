from datetime import date


def analyze_timeline(
    planned_start_date: date,
    planned_end_date: date,
    actual_start_date: date | None,
    actual_end_date: date | None,
    planned_progress: float,
    actual_progress: float,
):
    # -----------------------------------------
    # PROGRESS ANALYSIS
    # -----------------------------------------

    progress_gap = planned_progress - actual_progress

    if progress_gap <= 0:
        progress_status = "on_track"
    elif progress_gap <= 10:
        progress_status = "slightly_delayed"
    elif progress_gap <= 25:
        progress_status = "delayed"
    else:
        progress_status = "critically_delayed"

    # -----------------------------------------
    # DATE ANALYSIS
    # -----------------------------------------

    total_planned_days = (
        planned_end_date - planned_start_date
    ).days

    if actual_start_date is not None:
        elapsed_days = (
            date.today() - actual_start_date
        ).days
    else:
        elapsed_days = 0

    remaining_days = (
        planned_end_date - date.today()
    ).days

    # -----------------------------------------
    # DELAY ANALYSIS
    # -----------------------------------------

    delay_days = 0

    if actual_end_date is not None:
        delay_days = (
            actual_end_date - planned_end_date
        ).days

        if delay_days < 0:
            delay_days = 0

    # -----------------------------------------
    # TIMELINE RISK
    # -----------------------------------------

    if progress_gap <= 0:
        timeline_risk = "low"

    elif progress_gap <= 10:
        timeline_risk = "medium"

    elif progress_gap <= 25:
        timeline_risk = "high"

    else:
        timeline_risk = "critical"

    # -----------------------------------------
    # RETURN AUREX INTELLIGENCE
    # -----------------------------------------

    return {
        "planned_start_date": planned_start_date,
        "planned_end_date": planned_end_date,
        "actual_start_date": actual_start_date,
        "actual_end_date": actual_end_date,

        "total_planned_days": total_planned_days,
        "elapsed_days": elapsed_days,
        "remaining_days": remaining_days,

        "planned_progress_percent": planned_progress,
        "actual_progress_percent": actual_progress,
        "progress_gap_percent": progress_gap,

        "progress_status": progress_status,
        "delay_days": delay_days,
        "timeline_risk": timeline_risk,
    }