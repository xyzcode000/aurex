from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk
from app.services.predictive_intelligence import predict_final_cost
from app.services.timeline_prediction import predict_completion_date


def generate_early_warning(project):
    """
    Aurex Early Warning Engine.

    Combines current project intelligence with
    predictive intelligence to generate actionable
    project warnings.
    """

    # -------------------------------------------------
    # RUN EXISTING INTELLIGENCE ENGINES
    # -------------------------------------------------

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

    # -------------------------------------------------
    # WARNING COLLECTION
    # -------------------------------------------------

    warnings = []
    recommendations = []

    # -------------------------------------------------
    # BUDGET WARNINGS
    # -------------------------------------------------

    budget_risk = budget_result.get(
        "budget_risk",
        "low",
    )

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

    # -------------------------------------------------
    # COST PREDICTION WARNINGS
    # -------------------------------------------------

    prediction_status = cost_prediction.get(
        "prediction_status"
    )

    projected_overrun_percent = cost_prediction.get(
        "projected_overrun_percent"
    )

    if prediction_status == "critical":
        warnings.append(
            "Projected final cost indicates a critical "
            f"budget overrun of {projected_overrun_percent}%."
        )

        recommendations.append(
            "Immediate financial intervention and "
            "expenditure investigation are recommended."
        )

    elif prediction_status == "high":
        warnings.append(
            "Projected final cost indicates a significant "
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

    # -------------------------------------------------
    # TIMELINE WARNINGS
    # -------------------------------------------------

    timeline_risk = timeline_result.get(
        "timeline_risk",
        "low",
    )

    if timeline_risk == "critical":
        warnings.append(
            "Critical timeline risk detected."
        )

        recommendations.append(
            "Immediate project schedule intervention is recommended."
        )

    elif timeline_risk == "high":
        warnings.append(
            "High timeline risk detected."
        )

        recommendations.append(
            "Project execution and milestone progress "
            "should be closely monitored."
        )

    elif timeline_risk == "medium":
        warnings.append(
            "Moderate timeline risk detected."
        )

        recommendations.append(
            "Monitor project milestones and progress."
        )

    # -------------------------------------------------
    # COMPLETION PREDICTION WARNINGS
    # -------------------------------------------------

    timeline_prediction_status = timeline_prediction.get(
        "prediction_status"
    )

    predicted_delay_days = timeline_prediction.get(
        "predicted_delay_days"
    )

    if timeline_prediction_status == "critically_delayed":
        warnings.append(
            "Project completion is predicted to experience "
            f"a critical delay of {predicted_delay_days} days."
        )

        recommendations.append(
            "Immediate schedule recovery action is recommended."
        )

    elif timeline_prediction_status == "delayed":
        warnings.append(
            "Project completion is predicted to exceed "
            f"the planned timeline by {predicted_delay_days} days."
        )

        recommendations.append(
            "Corrective timeline action should be considered."
        )

    elif timeline_prediction_status == "slightly_delayed":
        warnings.append(
            "Project completion is predicted to experience "
            f"a minor delay of {predicted_delay_days} days."
        )

        recommendations.append(
            "Monitor execution closely to prevent further delay."
        )

    # -------------------------------------------------
    # PROGRESS WARNINGS
    # -------------------------------------------------

    progress_gap = abs(
        float(
            timeline_result.get(
                "progress_gap_percent",
                0,
            )
        )
    )

    if progress_gap >= 25:
        warnings.append(
            f"Critical progress gap detected: {progress_gap}%."
        )

        recommendations.append(
            "Project execution should be reviewed against "
            "planned milestones."
        )

    elif progress_gap >= 15:
        warnings.append(
            f"Significant progress gap detected: {progress_gap}%."
        )

        recommendations.append(
            "Management should investigate causes of "
            "execution slowdown."
        )

    elif progress_gap >= 5:
        warnings.append(
            f"Minor progress gap detected: {progress_gap}%."
        )

    # -------------------------------------------------
    # DETERMINE OVERALL STATUS
    # -------------------------------------------------

    risk_score = float(
        risk_result.get(
            "overall_risk_score",
            0,
        )
    )

    if (
        risk_score >= 75
        or prediction_status == "critical"
        or timeline_prediction_status == "critically_delayed"
    ):
        overall_status = "critical"
        priority = "immediate_action"

    elif (
        risk_score >= 50
        or prediction_status == "high"
        or timeline_prediction_status == "delayed"
    ):
        overall_status = "high"
        priority = "urgent_attention"

    elif (
        risk_score >= 25
        or prediction_status == "medium"
        or timeline_prediction_status == "slightly_delayed"
    ):
        overall_status = "medium"
        priority = "monitor_closely"

    else:
        overall_status = "low"
        priority = "routine_monitoring"

    # -------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------

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

    # -------------------------------------------------
    # RETURN UNIFIED INTELLIGENCE
    # -------------------------------------------------

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