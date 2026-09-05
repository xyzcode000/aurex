from decimal import Decimal


def predict_final_cost(project):
    """
    Predict the projected final cost of a project
    based on current expenditure and actual progress.
    """

    approved_budget = float(project.approved_budget or 0)

    revised_budget = float(
        project.revised_budget
        if project.revised_budget is not None
        else approved_budget
    )

    expenditure = float(project.expenditure or 0)
    actual_progress = float(project.actual_progress or 0)

    # -------------------------------------------------
    # SAFETY CHECK
    # -------------------------------------------------

    if actual_progress <= 0:
        return {
            "project_id": project.id,
            "approved_budget": approved_budget,
            "revised_budget": revised_budget,
            "current_expenditure": expenditure,
            "actual_progress_percent": actual_progress,
            "projected_final_cost": None,
            "projected_overrun": None,
            "projected_overrun_percent": None,
            "prediction_status": "insufficient_data",
            "prediction_message": (
                "Insufficient progress data to calculate "
                "a reliable final cost prediction."
            ),
        }

    # -------------------------------------------------
    # PROJECTED FINAL COST
    # -------------------------------------------------

    progress_ratio = actual_progress / 100

    projected_final_cost = expenditure / progress_ratio

    # -------------------------------------------------
    # OVERRUN CALCULATION
    # -------------------------------------------------

    projected_overrun = projected_final_cost - revised_budget

    if revised_budget > 0:
        projected_overrun_percent = (
            projected_overrun / revised_budget
        ) * 100
    else:
        projected_overrun_percent = 0

    # -------------------------------------------------
    # PREDICTION STATUS
    # -------------------------------------------------

    if projected_final_cost > revised_budget * 1.25:
        prediction_status = "critical"

    elif projected_final_cost > revised_budget * 1.10:
        prediction_status = "high"

    elif projected_final_cost > revised_budget:
        prediction_status = "medium"

    else:
        prediction_status = "low"

    # -------------------------------------------------
    # MANAGEMENT MESSAGE
    # -------------------------------------------------

    if prediction_status == "critical":
        prediction_message = (
            "Projected final cost indicates a critical "
            "budget overrun. Immediate financial "
            "intervention is recommended."
        )

    elif prediction_status == "high":
        prediction_message = (
            "Projected final cost indicates a significant "
            "budget overrun. Corrective financial action "
            "should be considered."
        )

    elif prediction_status == "medium":
        prediction_message = (
            "Projected final cost is above the revised "
            "budget. Financial monitoring is recommended."
        )

    else:
        prediction_message = (
            "Projected final cost remains within the "
            "revised budget."
        )

    # -------------------------------------------------
    # RETURN PREDICTION
    # -------------------------------------------------

    return {
        "project_id": project.id,
        "approved_budget": round(approved_budget, 2),
        "revised_budget": round(revised_budget, 2),
        "current_expenditure": round(expenditure, 2),
        "actual_progress_percent": round(actual_progress, 2),
        "projected_final_cost": round(
            projected_final_cost,
            2,
        ),
        "projected_overrun": round(
            max(projected_overrun, 0),
            2,
        ),
        "projected_overrun_percent": round(
            max(projected_overrun_percent, 0),
            2,
        ),
        "prediction_status": prediction_status,
        "prediction_message": prediction_message,
    }