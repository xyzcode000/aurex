from datetime import date

from app.services.timeline_intelligence import analyze_timeline


def test_timeline_calculates_planned_duration():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=None,
        planned_progress=50,
        actual_progress=50,
    )

    assert result["total_planned_days"] == 365


def test_timeline_calculates_progress_gap():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=None,
        planned_progress=60,
        actual_progress=40,
    )

    assert result["progress_gap_percent"] == 20


def test_timeline_status_is_on_track_when_progress_meets_plan():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=None,
        planned_progress=50,
        actual_progress=50,
    )

    assert result["progress_status"] == "on_track"
    assert result["timeline_risk"] == "low"


def test_timeline_status_is_slightly_delayed():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=None,
        planned_progress=50,
        actual_progress=45,
    )

    assert result["progress_status"] == "slightly_delayed"
    assert result["timeline_risk"] == "medium"


def test_timeline_status_is_delayed():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=None,
        planned_progress=60,
        actual_progress=40,
    )

    assert result["progress_status"] == "delayed"
    assert result["timeline_risk"] == "high"


def test_timeline_status_is_critically_delayed():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=None,
        planned_progress=70,
        actual_progress=40,
    )

    assert result["progress_status"] == "critically_delayed"
    assert result["timeline_risk"] == "critical"


def test_actual_end_date_calculates_confirmed_delay():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2026, 12, 31),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=date(2027, 2, 1),
        planned_progress=100,
        actual_progress=100,
    )

    assert result["delay_days"] == 32


def test_project_completed_on_time_has_no_delay():
    result = analyze_timeline(
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2026, 12, 31),
        actual_start_date=date(2026, 1, 1),
        actual_end_date=date(2026, 12, 31),
        planned_progress=100,
        actual_progress=100,
    )

    assert result["delay_days"] == 0