from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk
from app.services.predictive_intelligence import predict_final_cost
from app.services.timeline_prediction import predict_completion_date


def generate_early_warning(project):
    # ---------------------------------------------------------
    # 1. CORE INTELLIGENCE
    # ---------------------------------------------------------

    budget_result = analyze_budget(project)

    timeline_result = analyze_timeline(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=float(project.planned_progress),
        actual_progress=float(project.actual_progress),
    )

    risk_result = analyze_risk(project)

    cost_prediction = predict_final_cost(project)

    timeline_prediction = predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(project.actual_progress),
    )

    # ---------------------------------------------------------
    # 2. WARNING COLLECTION
    # ---------------------------------------------------------

    warnings = []
    recommendations = []

    # ---------------------------------------------------------
    # 3. BUDGET WARNINGS
    # ---------------------------------------------------------

    budget_risk = budget_result.get("budget_risk", "low")

    if budget_risk == "high":
        warnings.append(
            "High budget risk detected."
        )
        recommendations.append(
            "Immediate financial review is recommended."
        )

    elif budget_risk == "medium":
        warnings.append(
            "Moderate budget risk detected."
        )
        recommendations.append(
            "Monitor expenditure and budget utilization closely."
        )

    # ---------------------------------------------------------
    # 4. COST PREDICTION WARNINGS
    # ---------------------------------------------------------

    prediction_status = cost_prediction.get(
        "prediction_status"
    )

    projected_overrun_percent = cost_prediction.get(
        "projected_overrun_percent"
    )

    if prediction_status == "critical":
        warnings.append(
            f"Projected final cost indicates a critical "
            f"budget overrun of {projected_overrun_percent}%."
        )

        recommendations.append(
            "Immediate financial intervention and "
            "expenditure investigation are recommended."
        )

    elif prediction_status == "high":
        warnings.append(
            f"Projected final cost indicates a significant "
            f"budget overrun of {projected_overrun_percent}%."
        )

        recommendations.append(
            "Corrective financial action should be considered."
        )

    elif prediction_status == "medium":
        warnings.append(
            "Projected final cost is above the revised budget."
        )

        recommendations.append(
            "Continue financial monitoring."
        )

    # ---------------------------------------------------------
    # 5. CURRENT TIMELINE / EXECUTION WARNINGS
    # ---------------------------------------------------------

    timeline_risk = timeline_result.get(
        "timeline_risk",
        "low"
    )

    reported_progress_gap = float(
        timeline_result.get(
            "progress_gap_percent",
            0
        )
    )

    if timeline_risk == "critical":
        warnings.append(
            "Critical timeline execution risk detected."
        )

        recommendations.append(
            "Immediate project schedule intervention "
            "is recommended."
        )

    elif timeline_risk == "high":
        warnings.append(
            "High timeline execution risk detected."
        )

        recommendations.append(
            "Project execution and milestone progress "
            "should be closely monitored."
        )

    elif timeline_risk == "medium":
        warnings.append(
            "Moderate timeline execution risk detected."
        )

        recommendations.append(
            "Monitor project milestones and progress."
        )

    # ---------------------------------------------------------
    # 6. REPORTED PROGRESS GAP
    # ---------------------------------------------------------

    if reported_progress_gap >= 25:
        warnings.append(
            f"Critical reported progress gap detected: "
            f"{reported_progress_gap}%."
        )

        recommendations.append(
            "Project execution should be reviewed against "
            "planned milestones."
        )

    elif reported_progress_gap >= 15:
        warnings.append(
            f"Significant reported progress gap detected: "
            f"{reported_progress_gap}%."
        )

        recommendations.append(
            "Management should investigate causes "
            "of execution slowdown."
        )

    elif reported_progress_gap >= 5:
        warnings.append(
            f"Minor reported progress gap detected: "
            f"{reported_progress_gap}%."
        )

    # ---------------------------------------------------------
    # 7. CALENDAR-BASED SCHEDULE INTELLIGENCE
    # ---------------------------------------------------------

    calendar_difference = float(
        timeline_result.get(
            "calendar_progress_difference_percent",
            0
        )
    )

    calendar_status = timeline_result.get(
        "calendar_schedule_status",
        "unknown"
    )

    if calendar_status == "critically_delayed":
        warnings.append(
            "Calendar-based schedule analysis indicates "
            "critical execution delay."
        )

        recommendations.append(
            "Immediate schedule recovery planning "
            "is recommended."
        )

    elif calendar_status == "delayed":
        warnings.append(
            "Calendar-based schedule analysis indicates "
            "project execution delay."
        )

        recommendations.append(
            "Review current execution rate and "
            "schedule recovery options."
        )

    elif calendar_status == "slightly_delayed":
        warnings.append(
            "Calendar-based schedule analysis indicates "
            "minor schedule pressure."
        )

    # ---------------------------------------------------------
    # 8. CONFIRMED ACTUAL DELAY
    # ---------------------------------------------------------
    # IMPORTANT:
    # delay_days only represents confirmed delay based
    # on an actual completion date.
    #
    # A value of 0 does NOT mean there is no timeline risk.

    confirmed_delay_days = int(
        timeline_result.get(
            "delay_days",
            0
        )
    )

    if confirmed_delay_days > 0:
        warnings.append(
            f"Confirmed project completion delay detected: "
            f"{confirmed_delay_days} days."
        )

        recommendations.append(
            "Review the causes of the confirmed completion delay "
            "and implement schedule recovery measures."
        )

    # ---------------------------------------------------------
    # 9. PREDICTED COMPLETION DELAY
    # ---------------------------------------------------------

    timeline_prediction_status = timeline_prediction.get(
        "prediction_status"
    )

    predicted_delay_days = timeline_prediction.get(
        "predicted_delay_days"
    )

    if timeline_prediction_status == "critically_delayed":

        warnings.append(
            f"Project completion is predicted to experience "
            f"a critical delay of {predicted_delay_days} days."
        )

        recommendations.append(
            "Immediate schedule recovery action is recommended."
        )

    elif timeline_prediction_status == "delayed":

        warnings.append(
            f"Project completion is predicted to exceed "
            f"the planned timeline by {predicted_delay_days} days."
        )

        recommendations.append(
            "Corrective timeline action should be considered."
        )

    elif timeline_prediction_status == "slightly_delayed":

        warnings.append(
            f"Project completion is predicted to experience "
            f"a minor delay of {predicted_delay_days} days."
        )

        recommendations.append(
            "Monitor execution closely to prevent further delay."
        )

    # ---------------------------------------------------------
    # 10. IMPORTANT POSITIVE INTELLIGENCE
    # ---------------------------------------------------------

    # The project may be behind reported milestones but
    # still be ahead of the calendar-based schedule.

    if (
        reported_progress_gap > 0
        and calendar_difference > 0
        and timeline_prediction_status == "on_track"
    ):
        warnings.append(
            f"Project is {reported_progress_gap}% behind its "
            f"reported milestone plan, but calendar-based "
            f"execution is currently ahead by "
            f"{round(calendar_difference, 2)}%."
        )

        recommendations.append(
            "Reconcile reported milestone targets with the "
            "calendar-based project schedule."
        )

    # ---------------------------------------------------------
    # 11. OVERALL STATUS
    # ---------------------------------------------------------

    risk_score = float(
        risk_result.get(
            "overall_risk_score",
            0
        )
    )

    if (
        risk_score >= 75
        or prediction_status == "critical"
        or timeline_prediction_status == "critically_delayed"
        or confirmed_delay_days > 90
    ):
        overall_status = "critical"
        priority = "immediate_action"

    elif (
        risk_score >= 50
        or prediction_status == "high"
        or timeline_prediction_status == "delayed"
        or confirmed_delay_days > 30
    ):
        overall_status = "high"
        priority = "urgent_attention"

    elif (
        risk_score >= 25
        or prediction_status == "medium"
        or timeline_prediction_status == "slightly_delayed"
        or confirmed_delay_days > 0
    ):
        overall_status = "medium"
        priority = "monitor_closely"

    else:
        overall_status = "low"
        priority = "routine_monitoring"

    # ---------------------------------------------------------
    # 12. EXECUTIVE SUMMARY
    # ---------------------------------------------------------

    if overall_status == "critical":

        executive_summary = (
            "Aurex has detected critical project conditions "
            "requiring immediate management intervention."
        )

    elif overall_status == "high":

        executive_summary = (
            "Aurex has detected significant project risks "
            "requiring urgent management attention."
        )

    elif overall_status == "medium":

        executive_summary = (
            "Aurex has detected moderate project risks. "
            "The project should be monitored closely."
        )

    else:

        executive_summary = (
            "Aurex has detected no major immediate threats. "
            "Routine project monitoring is recommended."
        )

    # ---------------------------------------------------------
    # 13. FINAL RESPONSE
    # ---------------------------------------------------------

    return {
        "project_id": project.id,

        "overall_status": overall_status,

        "priority": priority,

        "risk_score": risk_score,

        "warnings": warnings,

        "recommendations": recommendations,

        "executive_summary": executive_summary,

        "intelligence": {
            "budget": budget_result,

            "timeline": timeline_result,

            "risk": risk_result,

            "cost_prediction": cost_prediction,

            "timeline_prediction": timeline_prediction,
        },
    }