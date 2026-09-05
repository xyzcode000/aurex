from copy import deepcopy
from datetime import timedelta

from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk


def simulate_scenario(
    project,
    budget_change_percent: float = 0,
    delay_days: int = 0,
    progress_change_percent: float = 0,
):
    """
    Aurex Scenario Intelligence Engine

    Simulates possible changes to a project and compares
    the current project risk with the simulated project risk.

    Supported simulations:
    - Budget increase/decrease
    - Project delay
    - Progress improvement/reduction
    """

    # -----------------------------------------
    # CREATE A COPY OF THE PROJECT
    # IMPORTANT:
    # We never modify the real database object.
    # -----------------------------------------

    simulated_project = deepcopy(project)

    # -----------------------------------------
    # CURRENT INTELLIGENCE
    # -----------------------------------------

    current_risk = analyze_risk(project)

    # -----------------------------------------
    # SIMULATE BUDGET CHANGE
    # -----------------------------------------

    current_budget = float(
        simulated_project.approved_budget
    )

    budget_change_amount = (
        current_budget *
        (budget_change_percent / 100)
    )

    simulated_project.approved_budget = (
        current_budget +
        budget_change_amount
    )

    # -----------------------------------------
    # SIMULATE PROJECT DELAY
    # -----------------------------------------

    if delay_days != 0:

        simulated_project.planned_end_date = (
            simulated_project.planned_end_date +
            timedelta(days=delay_days)
        )

    # -----------------------------------------
    # SIMULATE PROGRESS CHANGE
    # -----------------------------------------

    simulated_progress = (
        float(simulated_project.actual_progress) +
        progress_change_percent
    )

    # Keep progress between 0 and 100
    simulated_progress = max(
        0,
        min(simulated_progress, 100),
    )

    simulated_project.actual_progress = (
        simulated_progress
    )

    # -----------------------------------------
    # SIMULATED INTELLIGENCE
    # -----------------------------------------

    simulated_budget = analyze_budget(
        simulated_project
    )

    simulated_timeline = analyze_timeline(
        planned_start_date=simulated_project.planned_start_date,
        planned_end_date=simulated_project.planned_end_date,
        actual_start_date=simulated_project.actual_start_date,
        actual_end_date=simulated_project.actual_end_date,
        planned_progress=float(
            simulated_project.planned_progress
        ),
        actual_progress=float(
            simulated_project.actual_progress
        ),
    )

    # -----------------------------------------
    # SIMULATED RISK
    # -----------------------------------------

    simulated_risk = calculate_simulated_risk(
        project_id=project.id,
        budget_result=simulated_budget,
        timeline_result=simulated_timeline,
    )

    # -----------------------------------------
    # RISK COMPARISON
    # -----------------------------------------

    current_score = current_risk[
        "overall_risk_score"
    ]

    simulated_score = simulated_risk[
        "overall_risk_score"
    ]

    risk_change = (
        simulated_score -
        current_score
    )

    # -----------------------------------------
    # IMPACT ANALYSIS
    # -----------------------------------------

    if risk_change > 0:
        impact = "risk_increased"

    elif risk_change < 0:
        impact = "risk_reduced"

    else:
        impact = "no_significant_change"

    # -----------------------------------------
    # AUREX RECOMMENDATION
    # -----------------------------------------

    if simulated_score >= 75:

        recommendation = (
            "Critical risk scenario detected. "
            "Immediate intervention and corrective "
            "action are recommended."
        )

    elif simulated_score >= 50:

        recommendation = (
            "High risk scenario detected. "
            "Management should closely monitor the "
            "project and take corrective action."
        )

    elif simulated_score >= 25:

        recommendation = (
            "Moderate risk scenario detected. "
            "Preventive action should be considered."
        )

    else:

        recommendation = (
            "Scenario results indicate manageable "
            "project risk."
        )

    # -----------------------------------------
    # RETURN COMPLETE SCENARIO ANALYSIS
    # -----------------------------------------

    return {
        "project_id": project.id,

        "scenario": {
            "budget_change_percent":
                budget_change_percent,

            "delay_days":
                delay_days,

            "progress_change_percent":
                progress_change_percent,
        },

        "current_risk": current_risk,

        "simulated_risk": simulated_risk,

        "risk_change": risk_change,

        "impact": impact,

        "recommendation": recommendation,
    }


def calculate_simulated_risk(
    project_id,
    budget_result,
    timeline_result,
):
    """
    Calculates risk from simulated Budget and Timeline
    Intelligence results.
    """

    risk_score = 0

    risk_factors = []

    # -----------------------------------------
    # BUDGET RISK
    # -----------------------------------------

    budget_risk = budget_result.get(
        "budget_risk",
        "low",
    )

    if budget_risk == "medium":

        risk_score += 20

        risk_factors.append(
            "Moderate budget risk detected"
        )

    elif budget_risk == "high":

        risk_score += 35

        risk_factors.append(
            "High budget risk detected"
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
            "High timeline risk detected"
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
            f"Critical progress gap: {progress_gap}%"
        )

    elif progress_gap >= 15:

        risk_score += 15

        risk_factors.append(
            f"Significant progress gap: {progress_gap}%"
        )

    elif progress_gap >= 5:

        risk_score += 5

        risk_factors.append(
            f"Minor progress gap: {progress_gap}%"
        )

    # -----------------------------------------
    # LIMIT SCORE
    # -----------------------------------------

    risk_score = min(
        round(risk_score),
        100,
    )

    # -----------------------------------------
    # OVERALL RISK LEVEL
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
    # RETURN SIMULATED RISK
    # -----------------------------------------

    return {
        "project_id": project_id,

        "overall_risk_score": risk_score,

        "overall_risk_level": overall_risk,

        "budget_risk": budget_risk,

        "timeline_risk": timeline_risk,

        "progress_gap_percent": progress_gap,

        "risk_factors": risk_factors,
    }