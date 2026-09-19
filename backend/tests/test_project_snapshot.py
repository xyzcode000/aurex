from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.project import Project
from app.models.project_snapshot import ProjectSnapshot
from app.services.project_snapshot_service import create_project_snapshot


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_project(db_session):
    project = Project(
        name="Test Highway Project",
        description="Test infrastructure project",
        implementing_agency="Test Agency",
        location="Chhattisgarh",
        status="in_progress",
        approved_budget=Decimal("100000000"),
        revised_budget=Decimal("110000000"),
        expenditure=Decimal("40000000"),
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 15),
        actual_end_date=None,
        planned_progress=Decimal("50"),
        actual_progress=Decimal("40"),
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    return project


def test_snapshot_can_be_created(db_session, sample_project):
    snapshot = create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 13),
    )

    assert snapshot.id is not None
    assert snapshot.project_id == sample_project.id
    assert snapshot.observation_date == date(2026, 9, 13)


def test_snapshot_captures_project_state(db_session, sample_project):
    snapshot = create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 13),
    )

    assert snapshot.implementing_agency == sample_project.implementing_agency
    assert snapshot.location == sample_project.location
    assert snapshot.status == sample_project.status
    assert snapshot.approved_budget == sample_project.approved_budget
    assert snapshot.revised_budget == sample_project.revised_budget
    assert snapshot.expenditure == sample_project.expenditure
    assert snapshot.planned_progress == sample_project.planned_progress
    assert snapshot.actual_progress == sample_project.actual_progress
    assert snapshot.planned_start_date == sample_project.planned_start_date
    assert snapshot.planned_end_date == sample_project.planned_end_date
    assert snapshot.actual_start_date == sample_project.actual_start_date
    assert snapshot.actual_end_date == sample_project.actual_end_date


def test_snapshot_does_not_modify_project(db_session, sample_project):
    original_values = {
        "name": sample_project.name,
        "approved_budget": sample_project.approved_budget,
        "revised_budget": sample_project.revised_budget,
        "expenditure": sample_project.expenditure,
        "planned_progress": sample_project.planned_progress,
        "actual_progress": sample_project.actual_progress,
        "status": sample_project.status,
    }

    create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 13),
    )

    db_session.refresh(sample_project)

    assert sample_project.name == original_values["name"]
    assert sample_project.approved_budget == original_values["approved_budget"]
    assert sample_project.revised_budget == original_values["revised_budget"]
    assert sample_project.expenditure == original_values["expenditure"]
    assert sample_project.planned_progress == original_values["planned_progress"]
    assert sample_project.actual_progress == original_values["actual_progress"]
    assert sample_project.status == original_values["status"]


def test_duplicate_snapshot_is_rejected(db_session, sample_project):
    create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 13),
    )

    with pytest.raises(
        ValueError,
        match="A snapshot for this project and observation date already exists.",
    ):
        create_project_snapshot(
            db=db_session,
            project=sample_project,
            observation_date=date(2026, 9, 13),
        )


def test_different_observation_dates_are_allowed(db_session, sample_project):
    first_snapshot = create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 13),
    )

    second_snapshot = create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 14),
    )

    assert first_snapshot.id != second_snapshot.id
    assert first_snapshot.observation_date == date(2026, 9, 13)
    assert second_snapshot.observation_date == date(2026, 9, 14)


def test_snapshots_are_stored_in_chronological_order(db_session, sample_project):
    create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 14),
    )

    create_project_snapshot(
        db=db_session,
        project=sample_project,
        observation_date=date(2026, 9, 13),
    )

    snapshots = (
        db_session.query(ProjectSnapshot)
        .filter(ProjectSnapshot.project_id == sample_project.id)
        .order_by(ProjectSnapshot.observation_date.asc())
        .all()
    )

    assert len(snapshots) == 2
    assert snapshots[0].observation_date == date(2026, 9, 13)
    assert snapshots[1].observation_date == date(2026, 9, 14)