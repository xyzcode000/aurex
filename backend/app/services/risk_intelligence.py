from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.timeline_prediction import predict_completion_date


def analyze_risk(project):
    """
    Aurex Risk Intelligence Engine

    Produces an explainable project risk assessment by
    separating financial, milestone-execution and
    calendar-based schedule signals.

    Risk dimensions:
    1. Financial risk
    2. Milestone / reported progress risk
    3. Calendar schedule risk
    4. Predicted completion risk
    """

    # =====================================================
    # BUDGET INTELLIGENCE
    # =====================================================

    budget_result = analyze_budget(project)

    budget_risk = budget_result.get(
        "budget_risk",
        "low",
    )

    # =====================================================
    # TIMELINE INTELLIGENCE
    # =====================================================

    timeline_result = analyze_timeline(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=float(project.planned_progress),
        actual_progress=float(project.actual_progress),
    )

    # =====================================================
    # TIMELINE PREDICTION
    # =====================================================

    timeline_prediction = predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(project.actual_progress),
    )

    # =====================================================
    # PROGRESS / MILESTONE SIGNAL
    # =====================================================

    progress_gap = float(
        timeline_result.get(
            "progress_gap_percent",
            0,
        )
    )

    # Positive gap means actual progress is behind
    # the reported/planned milestone progress.

    if progress_gap >= 30:
        milestone_risk = "critical"

    elif progress_gap >= 15:
        milestone_risk = "high"

    elif progress_gap >= 5:
        milestone_risk = "medium"

    else:
        milestone_risk = "low"

    # =====================================================
    # CALENDAR-BASED SCHEDULE SIGNAL
    # =====================================================

    calendar_difference = float(
        timeline_prediction.get(
            "calendar_progress_difference_percent",
            0,
        )
    )

    calendar_status = timeline_prediction.get(
        "current_schedule_status",
        "unknown",
    )

    # Calendar schedule risk is intentionally separate
    # from the reported milestone gap.

    if calendar_status == "critically_delayed":
        calendar_schedule_risk = "critical"

    elif calendar_status == "delayed":
        calendar_schedule_risk = "high"

    elif calendar_status == "slightly_delayed":
        calendar_schedule_risk = "medium"

    elif calendar_status == "ahead_of_schedule":
        calendar_schedule_risk = "low"

    elif calendar_status == "on_track":
        calendar_schedule_risk = "low"

    else:
        calendar_schedule_risk = "low"

    # =====================================================
    # PREDICTED COMPLETION SIGNAL
    # =====================================================

    prediction_status = timeline_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    predicted_delay_days = timeline_prediction.get(
        "predicted_delay_days"
    )

    # =====================================================
    # RISK SCORE
    # =====================================================

    risk_score = 0

    risk_factors = []

    # -----------------------------------------------------
    # FINANCIAL RISK
    # -----------------------------------------------------

    if budget_risk == "medium":
        risk_score += 20

        risk_factors.append(
            "Moderate financial risk detected."
        )

    elif budget_risk == "high":
        risk_score += 35

        risk_factors.append(
            "High financial risk detected due to "
            "budget utilization and spending patterns."
        )

    # -----------------------------------------------------
    # MILESTONE / EXECUTION RISK
    # -----------------------------------------------------

    if milestone_risk == "medium":
        risk_score += 10

        risk_factors.append(
            f"Moderate reported milestone gap detected: "
            f"{progress_gap}%."
        )

    elif milestone_risk == "high":
        risk_score += 20

        risk_factors.append(
            f"Significant reported milestone gap detected: "
            f"{progress_gap}%."
        )

    elif milestone_risk == "critical":
        risk_score += 30

        risk_factors.append(
            f"Critical reported milestone gap detected: "
            f"{progress_gap}%."
        )

    # -----------------------------------------------------
    # CALENDAR SCHEDULE RISK
    # -----------------------------------------------------

    if calendar_schedule_risk == "medium":
        risk_score += 10

        risk_factors.append(
            "Minor calendar-based schedule pressure detected."
        )

    elif calendar_schedule_risk == "high":
        risk_score += 20

        risk_factors.append(
            "High calendar-based schedule risk detected."
        )

    elif calendar_schedule_risk == "critical":
        risk_score += 30

        risk_factors.append(
            "Critical calendar-based schedule risk detected."
        )

    elif calendar_schedule_risk == "low":
        if calendar_status == "ahead_of_schedule":
            risk_factors.append(
                f"Calendar-based execution is "
                f"{round(calendar_difference, 2)}% ahead of schedule."
            )

    # -----------------------------------------------------
    # PREDICTED COMPLETION RISK
    # -----------------------------------------------------

    if prediction_status == "slightly_delayed":
        risk_score += 10

        risk_factors.append(
            f"Completion is predicted to experience "
            f"a minor delay of {predicted_delay_days} days."
        )

    elif prediction_status == "delayed":
        risk_score += 20

        risk_factors.append(
            f"Completion is predicted to exceed the "
            f"planned timeline by {predicted_delay_days} days."
        )

    elif prediction_status == "critically_delayed":
        risk_score += 30

        risk_factors.append(
            f"Completion is predicted to experience "
            f"a critical delay of {predicted_delay_days} days."
        )

    # =====================================================
    # SCORE LIMIT
    # =====================================================

    risk_score = min(
        round(risk_score),
        100,
    )

    # =====================================================
    # OVERALL RISK LEVEL
    # =====================================================

    if risk_score >= 75:
        overall_risk = "critical"

    elif risk_score >= 50:
        overall_risk = "high"

    elif risk_score >= 25:
        overall_risk = "medium"

    else:
        overall_risk = "low"

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    if overall_risk == "critical":

        intelligence_summary = (
            "Critical project risk detected. "
            "Immediate management intervention is recommended."
        )

    elif overall_risk == "high":

        intelligence_summary = (
            "High project risk detected. "
            "The project requires close monitoring "
            "and corrective action."
        )

    elif overall_risk == "medium":

        intelligence_summary = (
            "Moderate project risk detected. "
            "Preventive actions should be considered."
        )

    else:

        intelligence_summary = (
            "Project risk is currently low. "
            "Continue regular monitoring."
        )

    # =====================================================
    # RETURN AUREX RISK INTELLIGENCE
    # =====================================================

    return {
        "project_id": project.id,

        "overall_risk_score": risk_score,

        "overall_risk_level": overall_risk,

        "budget_risk": budget_risk,

        "milestone_risk": milestone_risk,

        "calendar_schedule_risk": calendar_schedule_risk,

        "calendar_schedule_status": calendar_status,

        "progress_gap_percent": progress_gap,

        "calendar_progress_difference_percent": round(
            calendar_difference,
            2,
        ),

        "predicted_completion_status": prediction_status,

        "predicted_delay_days": predicted_delay_days,

        "risk_factors": risk_factors,

        "intelligence_summary": intelligence_summary,
    }