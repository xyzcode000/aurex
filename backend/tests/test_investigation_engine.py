from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.services.investigation_engine import investigate_project


def make_project(
    project_id=1,
    approved_budget=100000000,
    revised_budget=100000000,
    expenditure=10000000,
    planned_start_date=date(2026, 1, 1),
    planned_end_date=date(2027, 12, 31),
    actual_start_date=date(2026, 1, 1),
    actual_end_date=None,
    planned_progress=20,
    actual_progress=20,
):
    return SimpleNamespace(
        id=project_id,
        approved_budget=Decimal(str(approved_budget)),
        revised_budget=Decimal(str(revised_budget)),
        expenditure=Decimal(str(expenditure)),
        planned_start_date=planned_start_date,
        planned_end_date=planned_end_date,
        actual_start_date=actual_start_date,
        actual_end_date=actual_end_date,
        planned_progress=Decimal(str(planned_progress)),
        actual_progress=Decimal(str(actual_progress)),
    )


def test_investigation_returns_expected_top_level_fields():
    project = make_project()

    result = investigate_project(project)

    expected_fields = {
        "project_id",
        "investigation_status",
        "risk_score",
        "finding_count",
        "findings",
        "investigation_actions",
        "executive_summary",
        "source_intelligence",
    }

    assert expected_fields.issubset(result.keys())


def test_investigation_returns_project_id():
    project = make_project(project_id=99)

    result = investigate_project(project)

    assert result["project_id"] == 99


def test_investigation_detects_cost_overrun():
    project = make_project(
        revised_budget=90000000,
        expenditure=50000000,
        actual_progress=40,
    )

    result = investigate_project(project)

    categories = {
        finding["category"]
        for finding in result["findings"]
    }

    assert "cost_prediction" in categories


def test_investigation_detects_progress_problem():
    project = make_project(
        planned_progress=70,
        actual_progress=40,
    )

    result = investigate_project(project)

    categories = {
        finding["category"]
        for finding in result["findings"]
    }

    assert "progress" in categories


def test_investigation_detects_milestone_risk():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = investigate_project(project)

    categories = {
        finding["category"]
        for finding in result["findings"]
    }

    assert "milestone" in categories


def test_investigation_detects_confirmed_delay():
    project = make_project(
        planned_start_date=date(2025, 1, 1),
        planned_end_date=date(2026, 1, 1),
        actual_start_date=date(2025, 1, 1),
        actual_end_date=date(2026, 4, 15),
        planned_progress=100,
        actual_progress=100,
    )

    result = investigate_project(project)

    categories = {
        finding["category"]
        for finding in result["findings"]
    }

    assert "confirmed_delay" in categories


def test_investigation_findings_contain_required_structure():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = investigate_project(project)

    assert len(result["findings"]) > 0

    finding = result["findings"][0]

    expected_fields = {
        "category",
        "severity",
        "finding",
        "evidence",
        "possible_root_causes",
        "recommended_action",
    }

    assert expected_fields.issubset(finding.keys())


def test_investigation_generates_actions_for_findings():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = investigate_project(project)

    assert len(result["investigation_actions"]) > 0


def test_investigation_status_is_valid():
    project = make_project()

    result = investigate_project(project)

    assert result["investigation_status"] in {
        "low",
        "medium",
        "high",
        "critical",
    }


def test_finding_count_matches_findings_list():
    project = make_project(
        planned_progress=70,
        actual_progress=30,
    )

    result = investigate_project(project)

    assert result["finding_count"] == len(result["findings"])