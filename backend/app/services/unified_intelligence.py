from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk
from app.services.predictive_intelligence import predict_final_cost
from app.services.timeline_prediction import predict_completion_date
from app.services.early_warning import generate_early_warning
from app.services.investigation_engine import investigate_project


def generate_unified_intelligence(project):
    """
    Aurex Unified Intelligence Engine.

    Orchestrates all Aurex intelligence modules into
    one consolidated project intelligence report.
    """

    # ---------------------------------------------------------
    # 1. CORE INTELLIGENCE
    # ---------------------------------------------------------

    budget = analyze_budget(project)

    timeline = analyze_timeline(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=float(project.planned_progress),
        actual_progress=float(project.actual_progress),
    )

    risk = analyze_risk(project)

    # ---------------------------------------------------------
    # 2. PREDICTIVE INTELLIGENCE
    # ---------------------------------------------------------

    cost_prediction = predict_final_cost(project)

    timeline_prediction = predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(project.actual_progress),
    )

    # ---------------------------------------------------------
    # 3. EARLY WARNING
    # ---------------------------------------------------------

    early_warning = generate_early_warning(project)

    # ---------------------------------------------------------
    # 4. INVESTIGATION
    # ---------------------------------------------------------

    investigation = investigate_project(project)

    # ---------------------------------------------------------
    # 5. EXECUTIVE INTELLIGENCE
    # ---------------------------------------------------------

    risk_score = float(
        risk.get("overall_risk_score", 0)
    )

    risk_level = risk.get(
        "overall_risk_level",
        "low",
    )

    prediction_status = cost_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    timeline_prediction_status = timeline_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    # ---------------------------------------------------------
    # 6. PROJECT HEALTH
    # ---------------------------------------------------------

    if (
        risk_score >= 75
        or prediction_status == "critical"
        or timeline_prediction_status == "critically_delayed"
    ):
        project_health = "critical"

    elif (
        risk_score >= 50
        or prediction_status == "high"
        or timeline_prediction_status == "delayed"
    ):
        project_health = "high"

    elif (
        risk_score >= 25
        or prediction_status == "medium"
        or timeline_prediction_status == "slightly_delayed"
    ):
        project_health = "medium"

    else:
        project_health = "low"

    # ---------------------------------------------------------
    # 7. KEY METRICS
    # ---------------------------------------------------------

    reported_progress_gap = float(
        timeline.get("progress_gap_percent", 0)
    )

    calendar_progress_difference = float(
        timeline_prediction.get(
            "calendar_progress_difference_percent",
            0,
        )
    )

    predicted_delay_days = timeline_prediction.get(
        "predicted_delay_days"
    )

    recovery_margin_days = timeline_prediction.get(
        "recovery_margin_days"
    )

    projected_overrun_percent = cost_prediction.get(
        "projected_overrun_percent"
    )

    # ---------------------------------------------------------
    # 8. EXECUTIVE INSIGHT
    # ---------------------------------------------------------

    executive_insights = []

    if projected_overrun_percent is not None:
        if projected_overrun_percent > 0:
            executive_insights.append(
                f"Projected final cost is "
                f"{projected_overrun_percent}% above the "
                "revised budget."
            )

    if reported_progress_gap > 0:
        executive_insights.append(
            f"Actual progress is "
            f"{reported_progress_gap}% behind the "
            "reported milestone plan."
        )

    if calendar_progress_difference > 0:
        executive_insights.append(
            f"Calendar-based execution is currently "
            f"{round(calendar_progress_difference, 2)}% "
            "ahead of schedule."
        )

    elif calendar_progress_difference < 0:
        executive_insights.append(
            f"Calendar-based execution is currently "
            f"{round(abs(calendar_progress_difference), 2)}% "
            "behind schedule."
        )

    if predicted_delay_days is not None:
        if predicted_delay_days > 0:
            executive_insights.append(
                f"Current execution rate predicts a "
                f"{predicted_delay_days}-day completion delay."
            )
        elif recovery_margin_days:
            executive_insights.append(
                f"Current execution rate projects completion "
                f"{recovery_margin_days} days before the "
                "planned completion date."
            )

    # ---------------------------------------------------------
    # 9. EXECUTIVE SUMMARY
    # ---------------------------------------------------------

    if project_health == "critical":
        executive_summary = (
            "Aurex has identified critical project conditions "
            "requiring immediate management intervention."
        )

    elif project_health == "high":
        executive_summary = (
            "Aurex has identified significant project risks "
            "requiring urgent management attention."
        )

    elif project_health == "medium":
        executive_summary = (
            "Aurex has identified moderate project risks "
            "requiring close monitoring."
        )

    else:
        executive_summary = (
            "Aurex has identified no major immediate threats. "
            "Routine project monitoring is recommended."
        )

    # ---------------------------------------------------------
    # 10. FINAL UNIFIED RESPONSE
    # ---------------------------------------------------------

    return {
        "project_id": project.id,

        "project_health": project_health,

        "executive_summary": executive_summary,

        "executive_insights": executive_insights,

        "risk": {
            "score": risk_score,
            "level": risk_level,
        },

        "financial_intelligence": {
            "budget": budget,
            "cost_prediction": cost_prediction,
        },

        "timeline_intelligence": {
            "timeline": timeline,
            "timeline_prediction": timeline_prediction,
        },

        "early_warning": early_warning,

        "investigation": investigation,

        "recommended_actions": (
            early_warning.get(
                "recommendations",
                [],
            )
        ),
    }