import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User


# =========================================================
# ISOLATED TEST DATABASE
# =========================================================

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=test_engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# =========================================================
# HELPERS
# =========================================================


def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}@example.com"


def register_and_login(
    *,
    full_name: str = "API Test User",
) -> str:
    email = unique_email("projects_api")

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": full_name,
            "password": "StrongPassword123!",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def register_and_login_as_project_manager(
    *,
    full_name: str = "Project Manager Test User",
) -> str:
    email = unique_email("project_manager")

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": full_name,
            "password": "StrongPassword123!",
        },
    )

    assert register_response.status_code == 201

    # Promote the test user directly inside the isolated test DB.
    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        assert user is not None

        user.role = "project_manager"

        db.commit()

    finally:
        db.close()

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
    }


def valid_project_payload() -> dict:
    return {
        "name": "API Contract Test Project",
        "description": "Project created during API contract testing.",
        "implementing_agency": "Aurex Test Agency",
        "location": "Test Location",
        "status": "planned",
        "approved_budget": "100000000",
        "revised_budget": "110000000",
        "expenditure": "20000000",
        "planned_start_date": "2026-01-01",
        "planned_end_date": "2027-01-01",
        "actual_start_date": "2026-01-15",
        "actual_end_date": None,
        "planned_progress": "30",
        "actual_progress": "20",
    }


# =========================================================
# PROJECT ACCESS
# =========================================================


def test_projects_endpoint_requires_authentication():
    response = client.get("/api/projects")

    assert response.status_code == 401


def test_invalid_project_id_is_rejected():
    token = register_and_login()

    response = client.get(
        "/api/projects/0",
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_nonexistent_project_returns_404():
    token = register_and_login()

    response = client.get(
        "/api/projects/999999999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


# =========================================================
# PROJECT CREATION / RBAC
# =========================================================


def test_viewer_cannot_create_project():
    token = register_and_login()

    response = client.post(
        "/api/projects",
        headers=auth_headers(token),
        json=valid_project_payload(),
    )

    assert response.status_code == 403


def test_project_manager_can_create_project():
    token = register_and_login_as_project_manager()

    response = client.post(
        "/api/projects",
        headers=auth_headers(token),
        json=valid_project_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "API Contract Test Project"
    assert data["implementing_agency"] == "Aurex Test Agency"
    assert data["location"] == "Test Location"
    assert data["status"] == "planned"


# =========================================================
# PROJECT VALIDATION
# =========================================================


def test_invalid_project_payload_returns_422():
    token = register_and_login_as_project_manager()

    payload = valid_project_payload()
    payload["approved_budget"] = "-100"

    response = client.post(
        "/api/projects",
        headers=auth_headers(token),
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_progress_returns_422():
    token = register_and_login_as_project_manager()

    payload = valid_project_payload()
    payload["actual_progress"] = "150"

    response = client.post(
        "/api/projects",
        headers=auth_headers(token),
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_planned_dates_returns_422():
    token = register_and_login_as_project_manager()

    payload = valid_project_payload()
    payload["planned_start_date"] = "2027-01-01"
    payload["planned_end_date"] = "2026-01-01"

    response = client.post(
        "/api/projects",
        headers=auth_headers(token),
        json=payload,
    )

    assert response.status_code == 422


# =========================================================
# SCENARIO VALIDATION
# =========================================================


def test_invalid_scenario_budget_change_returns_422():
    token = register_and_login()

    response = client.post(
        "/api/projects/999999999/intelligence/scenario",
        headers=auth_headers(token),
        json={
            "budget_change_percent": 150,
            "delay_days": 0,
            "progress_change_percent": 0,
        },
    )

    assert response.status_code == 422


def test_invalid_scenario_delay_returns_422():
    token = register_and_login()

    response = client.post(
        "/api/projects/999999999/intelligence/scenario",
        headers=auth_headers(token),
        json={
            "budget_change_percent": 0,
            "delay_days": -1,
            "progress_change_percent": 0,
        },
    )

    assert response.status_code == 422


# =========================================================
# PROJECT LIST
# =========================================================


def test_authenticated_user_can_list_projects():
    token = register_and_login()

    response = client.get(
        "/api/projects",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_project_list_rejects_invalid_pagination():
    token = register_and_login()

    response = client.get(
        "/api/projects?skip=-1",
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_project_list_rejects_excessive_limit():
    token = register_and_login()

    response = client.get(
        "/api/projects?limit=101",
        headers=auth_headers(token),
    )

    assert response.status_code == 422


# =========================================================
# SNAPSHOT CONTRACT
# =========================================================


def test_snapshot_for_nonexistent_project_returns_404():
    token = register_and_login_as_project_manager()

    response = client.post(
        "/api/projects/999999999/snapshots",
        headers=auth_headers(token),
        json={
            "observation_date": "2026-09-23",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_project_manager_can_create_snapshot():
    token = register_and_login_as_project_manager()

    create_response = client.post(
        "/api/projects",
        headers=auth_headers(token),
        json=valid_project_payload(),
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    snapshot_response = client.post(
        f"/api/projects/{project_id}/snapshots",
        headers=auth_headers(token),
        json={
            "observation_date": "2026-09-23",
        },
    )

    assert snapshot_response.status_code == 201

    snapshot = snapshot_response.json()

    assert snapshot["project_id"] == project_id
    assert snapshot["observation_date"] == "2026-09-23"


# =========================================================
# INTELLIGENCE NOT-FOUND CONTRACT
# =========================================================


def test_budget_intelligence_nonexistent_project_returns_404():
    token = register_and_login()

    response = client.get(
        "/api/projects/999999999/intelligence/budget",
        headers=auth_headers(token),
    )

    assert response.status_code == 404


def test_risk_intelligence_nonexistent_project_returns_404():
    token = register_and_login()

    response = client.get(
        "/api/projects/999999999/intelligence/risk",
        headers=auth_headers(token),
    )

    assert response.status_code == 404


def test_unified_intelligence_nonexistent_project_returns_404():
    token = register_and_login()

    response = client.get(
        "/api/projects/999999999/intelligence",
        headers=auth_headers(token),
    )

    assert response.status_code == 404


# =========================================================
# SECURITY CONFIGURATION
# =========================================================

def test_cors_allows_configured_frontend_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin")
        == "http://localhost:5173"
    )


def test_cors_rejects_unconfigured_frontend_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://malicious.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert (
        response.headers.get("access-control-allow-origin")
        != "http://malicious.example"
    )


def test_authenticated_request_without_bearer_token_returns_401():
    response = client.get("/api/projects")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required."


def test_authenticated_request_with_invalid_token_returns_401():
    response = client.get(
        "/api/projects",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid or expired authentication token."
    )
