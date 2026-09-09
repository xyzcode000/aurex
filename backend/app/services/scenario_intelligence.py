from copy import deepcopy
from datetime import timedelta

from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk
from app.services.predictive_intelligence import predict_final_cost
from app.services.timeline_prediction import predict_completion_date


# =============================================================
# MAIN SCENARIO ENGINE
# =============================================================

def simulate_scenario(
    project,
    budget_change_percent: float = 0,
    delay_days: int = 0,
    progress_change_percent: float = 0,
):
    """
    Aurex Scenario Intelligence Engine.

    Simulates hypothetical project changes without modifying
    the real database project.

    Supported simulations:
    - Budget increase/decrease
    - Execution delay
    - Progress improvement/reduction

    IMPORTANT:
    delay_days represents an additional hypothetical
    execution delay. It does NOT modify the official
    planned completion date.
    """

    # =========================================================
    # SAFE SIMULATION COPY
    # =========================================================

    simulated_project = deepcopy(project)

    # =========================================================
    # CURRENT INTELLIGENCE
    # =========================================================

    current_budget = analyze_budget(project)

    current_risk = analyze_risk(project)

    current_cost_prediction = predict_final_cost(project)

    current_timeline_prediction = predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(project.actual_progress or 0),
    )

    # =========================================================
    # SIMULATE BUDGET CHANGE
    # =========================================================

    current_approved_budget = float(
        simulated_project.approved_budget or 0
    )

    budget_change_amount = (
        current_approved_budget
        * (budget_change_percent / 100)
    )

    new_approved_budget = (
        current_approved_budget
        + budget_change_amount
    )

    simulated_project.approved_budget = max(
        0,
        new_approved_budget,
    )

    # Keep revised budget aligned with the same
    # hypothetical budget change.

    if simulated_project.revised_budget is not None:

        current_revised_budget = float(
            simulated_project.revised_budget
        )

        new_revised_budget = (
            current_revised_budget
            + budget_change_amount
        )

        simulated_project.revised_budget = max(
            0,
            new_revised_budget,
        )

    # =========================================================
    # SIMULATE PROGRESS CHANGE
    # =========================================================

    current_progress = float(
        simulated_project.actual_progress or 0
    )

    simulated_progress = (
        current_progress
        + progress_change_percent
    )

    simulated_progress = max(
        0,
        min(simulated_progress, 100),
    )

    simulated_project.actual_progress = (
        simulated_progress
    )

    # =========================================================
    # SIMULATED BUDGET INTELLIGENCE
    # =========================================================

    simulated_budget = analyze_budget(
        simulated_project
    )

    # =========================================================
    # SIMULATED TIMELINE INTELLIGENCE
    # =========================================================

    simulated_timeline = analyze_timeline(
        planned_start_date=(
            simulated_project.planned_start_date
        ),
        planned_end_date=(
            simulated_project.planned_end_date
        ),
        actual_start_date=(
            simulated_project.actual_start_date
        ),
        actual_end_date=(
            simulated_project.actual_end_date
        ),
        planned_progress=float(
            simulated_project.planned_progress or 0
        ),
        actual_progress=float(
            simulated_project.actual_progress or 0
        ),
    )

    # =========================================================
    # SIMULATED COST PREDICTION
    # =========================================================

    simulated_cost_prediction = predict_final_cost(
        simulated_project
    )

    # =========================================================
    # SIMULATED TIMELINE PREDICTION
    # =========================================================

    simulated_timeline_prediction = predict_completion_date(
        planned_start_date=(
            simulated_project.planned_start_date
        ),
        planned_end_date=(
            simulated_project.planned_end_date
        ),
        actual_start_date=(
            simulated_project.actual_start_date
        ),
        actual_progress=float(
            simulated_project.actual_progress or 0
        ),
    )

    # =========================================================
    # APPLY HYPOTHETICAL EXECUTION DELAY
    # =========================================================

    simulated_timeline_prediction = apply_execution_delay(
        timeline_prediction=(
            simulated_timeline_prediction
        ),
        planned_end_date=(
            simulated_project.planned_end_date
        ),
        delay_days=delay_days,
    )

    # =========================================================
    # SIMULATED RISK
    # =========================================================

    simulated_risk = analyze_risk(
        simulated_project
    )

    # =========================================================
    # APPLY SCENARIO-SPECIFIC DELAY RISK
    # =========================================================

    simulated_risk = apply_scenario_delay_risk(
        simulated_risk=simulated_risk,
        delay_days=delay_days,
    )

    # =========================================================
    # RISK COMPARISON
    # =========================================================

    current_score = float(
        current_risk.get(
            "overall_risk_score",
            0,
        )
    )

    simulated_score = float(
        simulated_risk.get(
            "overall_risk_score",
            0,
        )
    )

    risk_change = (
        simulated_score
        - current_score
    )

    # =========================================================
    # SCENARIO IMPACT
    # =========================================================

    if risk_change > 0:

        impact = "risk_increased"

    elif risk_change < 0:

        impact = "risk_reduced"

    else:

        impact = "no_significant_change"

    # =========================================================
    # PROJECT HEALTH
    # =========================================================

    current_health = determine_project_health(
        current_risk=current_risk,
        cost_prediction=current_cost_prediction,
        timeline_prediction=current_timeline_prediction,
    )

    simulated_health = determine_project_health(
        current_risk=simulated_risk,
        cost_prediction=simulated_cost_prediction,
        timeline_prediction=simulated_timeline_prediction,
    )

    # =========================================================
    # FINANCIAL IMPACT
    # =========================================================

    current_projected_cost = (
        current_cost_prediction.get(
            "projected_final_cost"
        )
    )

    simulated_projected_cost = (
        simulated_cost_prediction.get(
            "projected_final_cost"
        )
    )

    projected_cost_change = None

    if (
        current_projected_cost is not None
        and simulated_projected_cost is not None
    ):

        projected_cost_change = round(
            float(simulated_projected_cost)
            - float(current_projected_cost),
            2,
        )

    current_overrun = (
        current_cost_prediction.get(
            "projected_overrun"
        )
    )

    simulated_overrun = (
        simulated_cost_prediction.get(
            "projected_overrun"
        )
    )

    current_overrun_percent = (
        current_cost_prediction.get(
            "projected_overrun_percent"
        )
    )

    simulated_overrun_percent = (
        simulated_cost_prediction.get(
            "projected_overrun_percent"
        )
    )

    overrun_change_percentage_points = None

    if (
        current_overrun_percent is not None
        and simulated_overrun_percent is not None
    ):

        overrun_change_percentage_points = round(
            float(simulated_overrun_percent)
            - float(current_overrun_percent),
            2,
        )

    # =========================================================
    # TIMELINE IMPACT
    # =========================================================

    current_predicted_delay = (
        current_timeline_prediction.get(
            "predicted_delay_days"
        )
    )

    simulated_predicted_delay = (
        simulated_timeline_prediction.get(
            "predicted_delay_days"
        )
    )

    predicted_delay_change = None

    if (
        current_predicted_delay is not None
        and simulated_predicted_delay is not None
    ):

        predicted_delay_change = (
            simulated_predicted_delay
            - current_predicted_delay
        )

    # =========================================================
    # RECOMMENDATION
    # =========================================================

    recommendation = generate_recommendation(
        risk_change=risk_change,
        simulated_risk=simulated_risk,
        simulated_cost_prediction=(
            simulated_cost_prediction
        ),
        simulated_timeline_prediction=(
            simulated_timeline_prediction
        ),
        simulated_health=simulated_health,
    )

    # =========================================================
    # EXECUTIVE SUMMARY
    # =========================================================

    scenario_summary = generate_scenario_summary(
        current_health=current_health,
        simulated_health=simulated_health,
        risk_change=risk_change,
        current_overrun_percent=(
            current_overrun_percent
        ),
        simulated_overrun_percent=(
            simulated_overrun_percent
        ),
        predicted_delay_change=(
            predicted_delay_change
        ),
        delay_days=delay_days,
    )

    # =========================================================
    # FINAL RESPONSE
    # =========================================================

    return {
        "project_id": project.id,

        "scenario": {
            "budget_change_percent": (
                budget_change_percent
            ),
            "delay_days": delay_days,
            "progress_change_percent": (
                progress_change_percent
            ),
        },

        "current_state": {
            "health": current_health,
            "risk": current_risk,
            "budget": current_budget,
            "cost_prediction": (
                current_cost_prediction
            ),
            "timeline_prediction": (
                current_timeline_prediction
            ),
        },

        "simulated_state": {
            "health": simulated_health,
            "risk": simulated_risk,
            "budget": simulated_budget,
            "timeline": simulated_timeline,
            "cost_prediction": (
                simulated_cost_prediction
            ),
            "timeline_prediction": (
                simulated_timeline_prediction
            ),
        },

        "comparison": {
            "risk_change": round(
                risk_change,
                2,
            ),

            "impact": impact,

            "financial_impact": {
                "current_projected_cost": (
                    current_projected_cost
                ),
                "simulated_projected_cost": (
                    simulated_projected_cost
                ),
                "projected_cost_change": (
                    projected_cost_change
                ),
                "current_projected_overrun": (
                    current_overrun
                ),
                "simulated_projected_overrun": (
                    simulated_overrun
                ),
                "current_overrun_percent": (
                    current_overrun_percent
                ),
                "simulated_overrun_percent": (
                    simulated_overrun_percent
                ),
                "overrun_change_percentage_points": (
                    overrun_change_percentage_points
                ),
            },

            "timeline_impact": {
                "scenario_delay_days": delay_days,

                "current_predicted_delay_days": (
                    current_predicted_delay
                ),

                "simulated_predicted_delay_days": (
                    simulated_predicted_delay
                ),

                "predicted_delay_change_days": (
                    predicted_delay_change
                ),

                "current_completion_date": (
                    current_timeline_prediction.get(
                        "predicted_completion_date"
                    )
                ),

                "simulated_completion_date": (
                    simulated_timeline_prediction.get(
                        "predicted_completion_date"
                    )
                ),

                "planned_completion_date": (
                    project.planned_end_date
                ),
            },

            "risk_impact": {
                "current_risk_score": (
                    current_score
                ),

                "simulated_risk_score": (
                    simulated_score
                ),

                "risk_change": round(
                    risk_change,
                    2,
                ),

                "current_risk_level": (
                    current_risk.get(
                        "overall_risk_level"
                    )
                ),

                "simulated_risk_level": (
                    simulated_risk.get(
                        "overall_risk_level"
                    )
                ),
            },

            "health_change": (
                f"{current_health} -> "
                f"{simulated_health}"
            ),
        },

        "scenario_summary": scenario_summary,

        "recommendation": recommendation,
    }


# =============================================================
# EXECUTION DELAY
# =============================================================

def apply_execution_delay(
    timeline_prediction,
    planned_end_date,
    delay_days,
):
    """
    Applies hypothetical execution delay to the
    predicted completion date.

    The official planned completion date is never modified.
    """

    if delay_days <= 0:
        return timeline_prediction

    predicted_completion = (
        timeline_prediction.get(
            "predicted_completion_date"
        )
    )

    if predicted_completion is None:
        return timeline_prediction

    delayed_completion = (
        predicted_completion
        + timedelta(days=delay_days)
    )

    predicted_delay = (
        delayed_completion
        - planned_end_date
    ).days

    predicted_delay = max(
        0,
        predicted_delay,
    )

    result = dict(
        timeline_prediction
    )

    result["predicted_completion_date"] = (
        delayed_completion
    )

    result["predicted_delay_days"] = (
        predicted_delay
    )

    result["recovery_margin_days"] = max(
        0,
        -(
            delayed_completion
            - planned_end_date
        ).days,
    )

    # ---------------------------------------------------------
    # Prediction status
    # ---------------------------------------------------------

    if predicted_delay > 90:

        result["prediction_status"] = (
            "critically_delayed"
        )

        result["prediction_message"] = (
            "The scenario introduces an execution "
            "delay that is expected to push project "
            "completion significantly beyond the "
            "planned completion date."
        )

    elif predicted_delay > 30:

        result["prediction_status"] = (
            "delayed"
        )

        result["prediction_message"] = (
            "The scenario introduces an execution "
            "delay that is expected to push project "
            "completion beyond the planned timeline."
        )

    elif predicted_delay > 0:

        result["prediction_status"] = (
            "slightly_delayed"
        )

        result["prediction_message"] = (
            "The scenario introduces an execution "
            "delay that is expected to cause a minor "
            "completion delay."
        )

    else:

        result["prediction_status"] = (
            "on_track"
        )

    return result


# =============================================================
# SCENARIO DELAY RISK
# =============================================================

def apply_scenario_delay_risk(
    simulated_risk,
    delay_days,
):
    """
    Adds scenario-specific execution-delay risk.

    The core Risk Engine remains unchanged.
    """

    if delay_days <= 0:
        return simulated_risk

    result = dict(
        simulated_risk
    )

    original_score = float(
        result.get(
            "overall_risk_score",
            0,
        )
    )

    # ---------------------------------------------------------
    # Delay risk weighting
    # ---------------------------------------------------------

    if delay_days >= 180:

        delay_risk_points = 30
        delay_risk_level = "critical"

    elif delay_days >= 90:

        delay_risk_points = 20
        delay_risk_level = "high"

    elif delay_days >= 30:

        delay_risk_points = 10
        delay_risk_level = "medium"

    else:

        delay_risk_points = 5
        delay_risk_level = "low"

    new_score = min(
        round(
            original_score
            + delay_risk_points
        ),
        100,
    )

    if new_score >= 75:

        overall_level = "critical"

    elif new_score >= 50:

        overall_level = "high"

    elif new_score >= 25:

        overall_level = "medium"

    else:

        overall_level = "low"

    risk_factors = list(
        result.get(
            "risk_factors",
            [],
        )
    )

    risk_factors.append(
        f"Scenario introduces an additional "
        f"{delay_days}-day execution delay "
        f"({delay_risk_level} scenario impact)."
    )

    result["overall_risk_score"] = (
        new_score
    )

    result["overall_risk_level"] = (
        overall_level
    )

    result["scenario_delay_risk"] = (
        delay_risk_level
    )

    result["scenario_delay_risk_points"] = (
        delay_risk_points
    )

    result["risk_factors"] = (
        risk_factors
    )

    result["intelligence_summary"] = (
        f"Simulated scenario risk is "
        f"{overall_level} with an overall "
        f"risk score of {new_score}."
    )

    return result


# =============================================================
# PROJECT HEALTH
# =============================================================

def determine_project_health(
    current_risk,
    cost_prediction,
    timeline_prediction,
):
    """
    Determines overall project health using
    aggregate risk and predictive threats.
    """

    risk_score = float(
        current_risk.get(
            "overall_risk_score",
            0,
        )
    )

    cost_status = cost_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    timeline_status = timeline_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    if (
        risk_score >= 75
        or cost_status == "critical"
        or timeline_status == "critically_delayed"
    ):
        return "critical"

    if (
        risk_score >= 50
        or cost_status == "high"
        or timeline_status == "delayed"
    ):
        return "high"

    if (
        risk_score >= 25
        or cost_status == "medium"
        or timeline_status == "slightly_delayed"
    ):
        return "medium"

    return "low"


# =============================================================
# RECOMMENDATION
# =============================================================

def generate_recommendation(
    risk_change,
    simulated_risk,
    simulated_cost_prediction,
    simulated_timeline_prediction,
    simulated_health,
):
    """
    Generates a decision-oriented recommendation.
    """

    cost_status = simulated_cost_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    timeline_status = simulated_timeline_prediction.get(
        "prediction_status",
        "insufficient_data",
    )

    predicted_delay = simulated_timeline_prediction.get(
        "predicted_delay_days"
    )

    if simulated_health == "critical":

        return (
            "Critical scenario detected. Immediate "
            "management intervention is recommended. "
            "Review financial exposure, execution "
            "performance, and schedule recovery actions."
        )

    if cost_status == "critical":

        return (
            "The scenario produces a critical projected "
            "cost outcome. Immediate financial review "
            "and expenditure investigation are recommended."
        )

    if timeline_status == "critically_delayed":

        return (
            "The scenario produces a critical completion "
            "delay. Immediate schedule recovery and "
            "execution intervention are recommended."
        )

    if (
        predicted_delay is not None
        and predicted_delay > 0
    ):

        return (
            f"The scenario predicts a {predicted_delay}-day "
            "completion delay. Schedule recovery measures "
            "should be evaluated."
        )

    if risk_change < 0:

        return (
            "The simulated scenario reduces overall "
            "project risk. The proposed change may "
            "improve project resilience, subject to "
            "financial and operational feasibility."
        )

    if risk_change > 0:

        return (
            "The simulated scenario increases project "
            "risk. Management should review the financial, "
            "schedule, and execution implications before "
            "implementing the proposed change."
        )

    return (
        "The simulated scenario produces manageable "
        "project conditions. Routine monitoring remains "
        "recommended."
    )


# =============================================================
# EXECUTIVE SUMMARY
# =============================================================

def generate_scenario_summary(
    current_health,
    simulated_health,
    risk_change,
    current_overrun_percent,
    simulated_overrun_percent,
    predicted_delay_change,
    delay_days,
):
    """
    Generates an executive-level explanation
    of the scenario outcome.
    """

    summary_parts = []

    summary_parts.append(
        f"Project health changes from "
        f"{current_health} to {simulated_health}."
    )

    if risk_change > 0:

        summary_parts.append(
            f"Overall risk increases by "
            f"{round(risk_change, 2)} points."
        )

    elif risk_change < 0:

        summary_parts.append(
            f"Overall risk decreases by "
            f"{round(abs(risk_change), 2)} points."
        )

    else:

        summary_parts.append(
            "Overall risk score remains unchanged."
        )

    # ---------------------------------------------------------
    # Financial impact
    # ---------------------------------------------------------

    if (
        current_overrun_percent is not None
        and simulated_overrun_percent is not None
    ):

        overrun_change = (
            float(simulated_overrun_percent)
            - float(current_overrun_percent)
        )

        if overrun_change > 0:

            summary_parts.append(
                f"Projected budget overrun increases "
                f"from {current_overrun_percent}% to "
                f"{simulated_overrun_percent}%."
            )

        elif overrun_change < 0:

            summary_parts.append(
                f"Projected budget overrun improves "
                f"from {current_overrun_percent}% to "
                f"{simulated_overrun_percent}%."
            )

        else:

            summary_parts.append(
                f"Projected budget overrun remains at "
                f"{simulated_overrun_percent}%."
            )

    # ---------------------------------------------------------
    # Scenario delay
    # ---------------------------------------------------------

    if delay_days > 0:

        summary_parts.append(
            f"The scenario introduces an additional "
            f"{delay_days}-day execution delay."
        )

    # ---------------------------------------------------------
    # Predicted timeline change
    # ---------------------------------------------------------

    if predicted_delay_change is not None:

        if predicted_delay_change > 0:

            summary_parts.append(
                f"Predicted completion delay increases "
                f"by {predicted_delay_change} days."
            )

        elif predicted_delay_change < 0:

            summary_parts.append(
                f"Predicted completion delay improves "
                f"by {abs(predicted_delay_change)} days."
            )

        elif delay_days == 0:

            summary_parts.append(
                "Predicted completion timing remains unchanged."
            )

    return " ".join(
        summary_parts
    )