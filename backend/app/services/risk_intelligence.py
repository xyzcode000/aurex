from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline


def analyze_risk(project):
    """
    Aurex Risk Intelligence Engine

    Combines Budget Intelligence and Timeline Intelligence
    to generate an overall project risk assessment.
    """

    # -----------------------------------------
    # GET BUDGET INTELLIGENCE
    # -----------------------------------------

    budget_result = analyze_budget(project)

    # -----------------------------------------
    # GET TIMELINE INTELLIGENCE
    # -----------------------------------------

    timeline_result = analyze_timeline(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_end_date=project.actual_end_date,
        planned_progress=float(project.planned_progress),
        actual_progress=float(project.actual_progress),
    )

    # -----------------------------------------
    # INITIAL RISK SCORE
    # -----------------------------------------

    risk_score = 0

    risk_factors = []

    # -----------------------------------------
    # BUDGET RISK
    # -----------------------------------------

    budget_risk = budget_result.get("budget_risk", "low")

    if budget_risk == "medium":
        risk_score += 20
        risk_factors.append(
            "Moderate budget risk detected"
        )

    elif budget_risk == "high":
        risk_score += 35
        risk_factors.append(
            "High budget risk detected due to spending patterns"
        )

    # -----------------------------------------
    # TIMELINE RISK
    # -----------------------------------------

    timeline_risk = timeline_result.get(
        "timeline_risk",
        "low",
    )

    if timeline_risk == "medium":
        risk_score += 25
        risk_factors.append(
            "Moderate timeline risk detected"
        )

    elif timeline_risk == "high":
        risk_score += 40
        risk_factors.append(
            "High timeline risk detected due to project delay"
        )

    # -----------------------------------------
    # PROGRESS GAP RISK
    # -----------------------------------------

    progress_gap = abs(
        float(
            timeline_result.get(
                "progress_gap_percent",
                0,
            )
        )
    )

    if progress_gap >= 30:
        risk_score += 25
        risk_factors.append(
            f"Critical progress gap detected: {progress_gap}%"
        )

    elif progress_gap >= 15:
        risk_score += 15
        risk_factors.append(
            f"Significant progress gap detected: {progress_gap}%"
        )

    elif progress_gap >= 5:
        risk_score += 5
        risk_factors.append(
            f"Minor progress gap detected: {progress_gap}%"
        )

    # -----------------------------------------
    # LIMIT SCORE TO 100
    # -----------------------------------------

    risk_score = min(
        round(risk_score),
        100,
    )

    # -----------------------------------------
    # DETERMINE OVERALL RISK LEVEL
    # -----------------------------------------

    if risk_score >= 75:
        overall_risk = "critical"

    elif risk_score >= 50:
        overall_risk = "high"

    elif risk_score >= 25:
        overall_risk = "medium"

    else:
        overall_risk = "low"

    # -----------------------------------------
    # GENERATE INTELLIGENCE SUMMARY
    # -----------------------------------------

    if overall_risk == "critical":
        intelligence_summary = (
            "Critical project risk detected. Immediate "
            "management intervention is recommended."
        )

    elif overall_risk == "high":
        intelligence_summary = (
            "High project risk detected. The project "
            "requires close monitoring and corrective action."
        )

    elif overall_risk == "medium":
        intelligence_summary = (
            "Moderate project risk detected. Preventive "
            "actions should be considered."
        )

    else:
        intelligence_summary = (
            "Project risk is currently low. Continue "
            "regular monitoring."
        )

    # -----------------------------------------
    # RETURN AUREX RISK INTELLIGENCE
    # -----------------------------------------

    return {
        "project_id": project.id,

        "overall_risk_score": risk_score,

        "overall_risk_level": overall_risk,

        "budget_risk": budget_risk,

        "timeline_risk": timeline_risk,

        "progress_gap_percent": progress_gap,

        "risk_factors": risk_factors,

        "intelligence_summary": intelligence_summary,
    }