from app.services.budget_intelligence import analyze_budget
from app.services.timeline_intelligence import analyze_timeline
from app.services.risk_intelligence import analyze_risk
from app.services.predictive_intelligence import predict_final_cost
from app.services.timeline_prediction import predict_completion_date


def investigate_project(project):
    """
    Aurex Investigation & Root-Cause Engine.

    Converts Aurex intelligence signals into:
    - investigation findings
    - supporting evidence
    - possible root causes
    - recommended investigation actions
    """

    # -------------------------------------------------
    # RUN EXISTING INTELLIGENCE
    # -------------------------------------------------

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

    cost_prediction = predict_final_cost(project)

    timeline_prediction = predict_completion_date(
        planned_start_date=project.planned_start_date,
        planned_end_date=project.planned_end_date,
        actual_start_date=project.actual_start_date,
        actual_progress=float(project.actual_progress),
    )

    # -------------------------------------------------
    # INVESTIGATION COLLECTIONS
    # -------------------------------------------------

    findings = []
    investigation_actions = []

    # -------------------------------------------------
    # BUDGET INVESTIGATION
    # -------------------------------------------------

    approved_budget = budget["approved_budget"]
    revised_budget = budget["revised_budget"]
    expenditure = budget["expenditure"]
    actual_progress = budget["actual_progress_percent"]

    if actual_progress > 0 and expenditure > 0:

        expenditure_ratio = (
            expenditure / revised_budget
        ) * 100 if revised_budget > 0 else 0

        if expenditure_ratio >= 75 and actual_progress < 50:

            findings.append({
                "category": "budget",
                "severity": "critical",
                "finding": (
                    "Expenditure is disproportionately high "
                    "relative to physical project progress."
                ),
                "evidence": {
                    "expenditure": expenditure,
                    "revised_budget": revised_budget,
                    "expenditure_utilization_percent": round(
                        expenditure_ratio,
                        2,
                    ),
                    "actual_progress_percent": actual_progress,
                },
                "possible_root_causes": [
                    "Cost escalation",
                    "Procurement inefficiency",
                    "Scope changes",
                    "Unplanned expenditure",
                ],
                "recommended_action": (
                    "Review expenditure records, procurement "
                    "contracts, approved scope changes and "
                    "major cost variations."
                ),
            })

            investigation_actions.append(
                "Investigate major expenditure transactions "
                "and procurement contracts."
            )

    # -------------------------------------------------
    # COST OVERRUN INVESTIGATION
    # -------------------------------------------------

    projected_overrun = cost_prediction.get(
        "projected_overrun",
        0,
    )

    projected_overrun_percent = cost_prediction.get(
        "projected_overrun_percent",
        0,
    )

    if projected_overrun > 0:

        severity = "medium"

        if projected_overrun_percent >= 25:
            severity = "critical"
        elif projected_overrun_percent >= 10:
            severity = "high"

        findings.append({
            "category": "cost_prediction",
            "severity": severity,
            "finding": (
                "The projected final project cost exceeds "
                "the revised budget."
            ),
            "evidence": {
                "revised_budget": revised_budget,
                "projected_final_cost": cost_prediction.get(
                    "projected_final_cost"
                ),
                "projected_overrun": projected_overrun,
                "projected_overrun_percent": (
                    projected_overrun_percent
                ),
            },
            "possible_root_causes": [
                "Cost escalation",
                "Low execution efficiency",
                "Procurement cost increases",
                "Scope expansion",
            ],
            "recommended_action": (
                "Investigate major cost drivers and compare "
                "actual expenditure against approved estimates."
            ),
        })

        investigation_actions.append(
            "Identify the largest contributors to projected "
            "cost overrun."
        )

    # -------------------------------------------------
    # PROGRESS GAP INVESTIGATION
    # -------------------------------------------------

    progress_gap = abs(
        float(
            timeline.get(
                "progress_gap_percent",
                0,
            )
        )
    )

    if progress_gap >= 10:

        severity = "medium"

        if progress_gap >= 25:
            severity = "critical"
        elif progress_gap >= 15:
            severity = "high"

        findings.append({
            "category": "progress",
            "severity": severity,
            "finding": (
                "Actual project progress is significantly "
                "behind planned progress."
            ),
            "evidence": {
                "planned_progress_percent": (
                    timeline["planned_progress_percent"]
                ),
                "actual_progress_percent": (
                    timeline["actual_progress_percent"]
                ),
                "progress_gap_percent": progress_gap,
            },
            "possible_root_causes": [
                "Execution slowdown",
                "Resource constraints",
                "Procurement delays",
                "Contractor performance issues",
                "Site or operational constraints",
            ],
            "recommended_action": (
                "Review milestone completion, resource "
                "availability, procurement status and "
                "contractor performance."
            ),
        })

        investigation_actions.append(
            "Investigate causes of the project progress gap."
        )

    # -------------------------------------------------
    # TIMELINE INVESTIGATION
    # -------------------------------------------------

    timeline_risk = timeline.get(
        "timeline_risk",
        "low",
    )

    predicted_delay = timeline_prediction.get(
        "predicted_delay_days",
        0,
    )

    if timeline_risk in ["high", "critical"]:

        findings.append({
            "category": "timeline",
            "severity": (
                "critical"
                if timeline_risk == "critical"
                else "high"
            ),
            "finding": (
                "Project execution indicates elevated "
                "timeline risk."
            ),
            "evidence": {
                "timeline_risk": timeline_risk,
                "remaining_planned_days": (
                    timeline["remaining_days"]
                ),
                "predicted_delay_days": predicted_delay,
                "progress_gap_percent": progress_gap,
            },
            "possible_root_causes": [
                "Milestone delays",
                "Resource constraints",
                "Procurement delays",
                "Execution inefficiency",
            ],
            "recommended_action": (
                "Review delayed milestones, dependencies, "
                "resource allocation and procurement schedules."
            ),
        })

        investigation_actions.append(
            "Review delayed milestones and project dependencies."
        )

    # -------------------------------------------------
    # RISK INVESTIGATION
    # -------------------------------------------------

    risk_score = risk.get(
        "overall_risk_score",
        0,
    )

    if risk_score >= 50:

        findings.append({
            "category": "overall_risk",
            "severity": (
                "critical"
                if risk_score >= 75
                else "high"
            ),
            "finding": (
                "Multiple project risk indicators are "
                "simultaneously elevated."
            ),
            "evidence": {
                "overall_risk_score": risk_score,
                "overall_risk_level": risk.get(
                    "overall_risk_level"
                ),
                "budget_risk": risk.get(
                    "budget_risk"
                ),
                "timeline_risk": risk.get(
                    "timeline_risk"
                ),
            },
            "possible_root_causes": [
                "Combined financial and execution issues",
                "Weak project monitoring",
                "Planning deficiencies",
                "Operational inefficiencies",
            ],
            "recommended_action": (
                "Conduct a comprehensive project review "
                "covering financial, timeline and execution data."
            ),
        })

        investigation_actions.append(
            "Conduct a comprehensive project risk review."
        )

    # -------------------------------------------------
    # DETERMINE INVESTIGATION STATUS
    # -------------------------------------------------

    if risk_score >= 75:
        investigation_status = "critical"
    elif risk_score >= 50:
        investigation_status = "high"
    elif risk_score >= 25:
        investigation_status = "medium"
    else:
        investigation_status = "low"

    # -------------------------------------------------
    # EXECUTIVE INVESTIGATION SUMMARY
    # -------------------------------------------------

    if findings:

        executive_summary = (
            f"Aurex identified {len(findings)} investigation "
            "finding(s) requiring management review."
        )

    else:

        executive_summary = (
            "Aurex did not identify any major investigation "
            "findings from the available project data."
        )

    # -------------------------------------------------
    # RETURN INVESTIGATION INTELLIGENCE
    # -------------------------------------------------

    return {
        "project_id": project.id,
        "investigation_status": investigation_status,
        "risk_score": risk_score,
        "finding_count": len(findings),
        "findings": findings,
        "investigation_actions": investigation_actions,
        "executive_summary": executive_summary,
        "source_intelligence": {
            "budget": budget,
            "timeline": timeline,
            "risk": risk,
            "cost_prediction": cost_prediction,
            "timeline_prediction": timeline_prediction,
        },
    }