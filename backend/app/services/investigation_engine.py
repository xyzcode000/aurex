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

    Uses the current Aurex Risk Intelligence architecture:
    - Budget Risk
    - Milestone Risk
    - Calendar Schedule Risk
    - Predicted Completion Status
    """

    # -------------------------------------------------
    # 1. RUN EXISTING INTELLIGENCE
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
    # 2. INVESTIGATION COLLECTIONS
    # -------------------------------------------------

    findings = []
    investigation_actions = []

    # -------------------------------------------------
    # 3. BUDGET INVESTIGATION
    # -------------------------------------------------

    revised_budget = budget["revised_budget"]
    expenditure = budget["expenditure"]
    actual_progress = budget["actual_progress_percent"]

    if actual_progress > 0 and expenditure > 0:

        expenditure_ratio = (
            (expenditure / revised_budget) * 100
            if revised_budget > 0
            else 0
        )

        if expenditure_ratio >= 75 and actual_progress < 50:

            findings.append(
                {
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
                }
            )

            investigation_actions.append(
                "Investigate major expenditure transactions "
                "and procurement contracts."
            )

    # -------------------------------------------------
    # 4. COST OVERRUN INVESTIGATION
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

        findings.append(
            {
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
            }
        )

        investigation_actions.append(
            "Identify the largest contributors to projected "
            "cost overrun."
        )

    # -------------------------------------------------
    # 5. REPORTED PROGRESS GAP INVESTIGATION
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

        findings.append(
            {
                "category": "progress",
                "severity": severity,
                "finding": (
                    "Actual project progress is significantly "
                    "behind the reported milestone plan."
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
            }
        )

        investigation_actions.append(
            "Investigate causes of the reported project "
            "progress gap."
        )

    # -------------------------------------------------
    # 6. MILESTONE RISK INVESTIGATION
    # -------------------------------------------------

    milestone_risk = risk.get(
        "milestone_risk",
        "low",
    )

    if milestone_risk in ["medium", "high", "critical"]:

        if milestone_risk == "critical":
            severity = "critical"
        elif milestone_risk == "high":
            severity = "high"
        else:
            severity = "medium"

        findings.append(
            {
                "category": "milestone",
                "severity": severity,
                "finding": (
                    "Reported milestone execution indicates "
                    "elevated project delivery risk."
                ),
                "evidence": {
                    "milestone_risk": milestone_risk,
                    "planned_progress_percent": (
                        timeline["planned_progress_percent"]
                    ),
                    "actual_progress_percent": (
                        timeline["actual_progress_percent"]
                    ),
                    "progress_gap_percent": progress_gap,
                },
                "possible_root_causes": [
                    "Milestone delays",
                    "Resource constraints",
                    "Procurement delays",
                    "Contractor performance issues",
                    "Execution inefficiency",
                ],
                "recommended_action": (
                    "Review delayed milestones, dependencies, "
                    "resource allocation and procurement schedules."
                ),
            }
        )

        investigation_actions.append(
            "Review milestone execution and identify "
            "the causes of milestone risk."
        )

    # -------------------------------------------------
    # 7. CALENDAR SCHEDULE INVESTIGATION
    # -------------------------------------------------

    calendar_schedule_risk = risk.get(
        "calendar_schedule_risk",
        "low",
    )

    calendar_schedule_status = risk.get(
        "calendar_schedule_status",
        "unknown",
    )

    calendar_difference = float(
        risk.get(
            "calendar_progress_difference_percent",
            0,
        )
    )

    if calendar_schedule_risk in [
        "medium",
        "high",
        "critical",
    ]:

        if calendar_schedule_risk == "critical":
            severity = "critical"
        elif calendar_schedule_risk == "high":
            severity = "high"
        else:
            severity = "medium"

        findings.append(
            {
                "category": "calendar_schedule",
                "severity": severity,
                "finding": (
                    "Calendar-based schedule analysis indicates "
                    "elevated execution risk."
                ),
                "evidence": {
                    "calendar_schedule_risk": (
                        calendar_schedule_risk
                    ),
                    "calendar_schedule_status": (
                        calendar_schedule_status
                    ),
                    "calendar_progress_difference_percent": (
                        round(calendar_difference, 2)
                    ),
                    "remaining_planned_days": (
                        timeline["remaining_days"]
                    ),
                },
                "possible_root_causes": [
                    "Execution slowdown",
                    "Resource constraints",
                    "Procurement delays",
                    "Schedule dependency issues",
                ],
                "recommended_action": (
                    "Review current execution rate, schedule "
                    "dependencies and available recovery options."
                ),
            }
        )

        investigation_actions.append(
            "Investigate calendar-based schedule pressure "
            "and recovery options."
        )

    # -------------------------------------------------
    # 8. CONFIRMED COMPLETION DELAY
    # -------------------------------------------------

    confirmed_delay_days = int(
        timeline.get(
            "delay_days",
            0,
        )
    )

    if confirmed_delay_days > 0:

        if confirmed_delay_days > 90:
            severity = "critical"
        elif confirmed_delay_days > 30:
            severity = "high"
        else:
            severity = "medium"

        findings.append(
            {
                "category": "confirmed_delay",
                "severity": severity,
                "finding": (
                    "The project has a confirmed completion "
                    "delay based on the actual completion date."
                ),
                "evidence": {
                    "confirmed_delay_days": confirmed_delay_days,
                    "planned_end_date": (
                        timeline["planned_end_date"]
                    ),
                    "actual_end_date": (
                        timeline["actual_end_date"]
                    ),
                },
                "possible_root_causes": [
                    "Execution delays",
                    "Resource constraints",
                    "Procurement delays",
                    "Contractor performance issues",
                    "External operational constraints",
                ],
                "recommended_action": (
                    "Investigate the causes of the confirmed "
                    "completion delay and implement recovery measures."
                ),
            }
        )

        investigation_actions.append(
            "Investigate the causes of the confirmed "
            "completion delay."
        )

    # -------------------------------------------------
    # 9. PREDICTED COMPLETION INVESTIGATION
    # -------------------------------------------------

    predicted_completion_status = risk.get(
        "predicted_completion_status",
        timeline_prediction.get(
            "prediction_status",
            "unknown",
        ),
    )

    predicted_delay_days = timeline_prediction.get(
        "predicted_delay_days",
        0,
    )

    if predicted_completion_status in [
        "slightly_delayed",
        "delayed",
        "critically_delayed",
    ]:

        if predicted_completion_status == "critically_delayed":
            severity = "critical"
        elif predicted_completion_status == "delayed":
            severity = "high"
        else:
            severity = "medium"

        findings.append(
            {
                "category": "completion_prediction",
                "severity": severity,
                "finding": (
                    "Current execution rate indicates a predicted "
                    "completion delay."
                ),
                "evidence": {
                    "predicted_completion_status": (
                        predicted_completion_status
                    ),
                    "predicted_delay_days": (
                        predicted_delay_days
                    ),
                    "current_schedule_status": (
                        timeline_prediction.get(
                            "current_schedule_status"
                        )
                    ),
                    "predicted_completion_date": (
                        timeline_prediction.get(
                            "predicted_completion_date"
                        )
                    ),
                },
                "possible_root_causes": [
                    "Low execution rate",
                    "Resource constraints",
                    "Schedule inefficiency",
                    "Procurement or dependency delays",
                ],
                "recommended_action": (
                    "Review execution rate and implement "
                    "schedule recovery measures."
                ),
            }
        )

        investigation_actions.append(
            "Review predicted completion delay and "
            "develop a schedule recovery plan."
        )

    # -------------------------------------------------
    # 10. OVERALL RISK INVESTIGATION
    # -------------------------------------------------

    risk_score = float(
        risk.get(
            "overall_risk_score",
            0,
        )
    )

    risk_level = risk.get(
        "overall_risk_level",
        "low",
    )

    if risk_score >= 50:

        findings.append(
            {
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
                    "overall_risk_level": risk_level,
                    "budget_risk": risk.get(
                        "budget_risk"
                    ),
                    "milestone_risk": risk.get(
                        "milestone_risk"
                    ),
                    "calendar_schedule_risk": risk.get(
                        "calendar_schedule_risk"
                    ),
                    "calendar_schedule_status": risk.get(
                        "calendar_schedule_status"
                    ),
                    "predicted_completion_status": risk.get(
                        "predicted_completion_status"
                    ),
                    "predicted_delay_days": risk.get(
                        "predicted_delay_days"
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
                    "covering financial, milestone, schedule "
                    "and execution data."
                ),
            }
        )

        investigation_actions.append(
            "Conduct a comprehensive project risk review."
        )

    # -------------------------------------------------
    # 11. DETERMINE INVESTIGATION STATUS
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
    # 12. EXECUTIVE INVESTIGATION SUMMARY
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
    # 13. RETURN INVESTIGATION INTELLIGENCE
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