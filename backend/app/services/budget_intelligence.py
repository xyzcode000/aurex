from decimal import Decimal

from app.models.project import Project


def analyze_budget(project: Project) -> dict:
    """
    Analyze project budget health and detect
    potential cost overrun risks.
    """

    approved_budget = project.approved_budget
    revised_budget = (
        project.revised_budget
        if project.revised_budget is not None
        else approved_budget
    )

    expenditure = project.expenditure
    progress = project.actual_progress

    # Avoid division by zero
    if revised_budget <= 0:
        return {
            "budget_utilization": 0,
            "budget_status": "invalid_budget",
            "budget_risk": "unknown",
        }

    budget_utilization = (
        expenditure / revised_budget
    ) * Decimal("100")

    # Compare spending with actual work completed
    spending_progress_gap = (
        budget_utilization - progress
    )

    # Budget status
    if expenditure > revised_budget:
        budget_status = "over_budget"
        budget_risk = "critical"

    elif spending_progress_gap > Decimal("30"):
        budget_status = "high_spending"
        budget_risk = "high"

    elif spending_progress_gap > Decimal("15"):
        budget_status = "spending_ahead_of_progress"
        budget_risk = "medium"

    else:
        budget_status = "healthy"
        budget_risk = "low"

    return {
        "approved_budget": float(approved_budget),
        "revised_budget": float(revised_budget),
        "expenditure": float(expenditure),
        "budget_utilization_percent": round(
            float(budget_utilization),
            2,
        ),
        "actual_progress_percent": float(progress),
        "spending_progress_gap": round(
            float(spending_progress_gap),
            2,
        ),
        "budget_status": budget_status,
        "budget_risk": budget_risk,
    }