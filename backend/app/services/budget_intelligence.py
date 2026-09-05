def analyze_budget(project):
    approved_budget = float(project.approved_budget or 0)
    revised_budget = float(
        project.revised_budget
        if project.revised_budget is not None
        else approved_budget
    )
    expenditure = float(project.expenditure or 0)

    planned_progress = float(project.planned_progress or 0)
    actual_progress = float(project.actual_progress or 0)

    budget_difference = revised_budget - approved_budget

    budget_change_percent = 0.0

    if approved_budget > 0:
        budget_change_percent = (
            budget_difference / approved_budget
        ) * 100

    spending_progress_gap = actual_progress - planned_progress

    projected_expenditure = expenditure

    if actual_progress > 0:
        projected_expenditure = (
            expenditure / actual_progress
        ) * 100

    budget_risk = "low"

    if projected_expenditure > revised_budget:
        budget_risk = "high"

    elif projected_expenditure > revised_budget * 0.9:
        budget_risk = "medium"

    return {
        "approved_budget": approved_budget,
        "revised_budget": revised_budget,
        "expenditure": expenditure,
        "budget_difference": round(
            budget_difference,
            2,
        ),
        "budget_change_percent": round(
            budget_change_percent,
            2,
        ),
        "planned_progress_percent": planned_progress,
        "actual_progress_percent": actual_progress,
        "spending_progress_gap": round(
            spending_progress_gap,
            2,
        ),
        "projected_expenditure": round(
            projected_expenditure,
            2,
        ),
        "budget_risk": budget_risk,
    }