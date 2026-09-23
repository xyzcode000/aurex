import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


# =========================================================
# TEST DATABASE
# =========================================================

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
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


# Create the test schema once for the authentication test suite.
Base.metadata.create_all(bind=test_engine)

# Make the application use the isolated test database.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# =========================================================
# HELPERS
# =========================================================


def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}@example.com"


# =========================================================
# REGISTRATION
# =========================================================


def test_register_user_success():
    email = unique_email("auth_test_user")

    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": "Auth Test User",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["full_name"] == "Auth Test User"
    assert data["role"] == "viewer"
    assert data["is_active"] is True
    assert "id" in data

    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email_is_rejected():
    email = unique_email("duplicate_auth_test")

    payload = {
        "email": email,
        "full_name": "Duplicate Test User",
        "password": "StrongPassword123!",
    }

    first_response = client.post(
        "/api/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409


# =========================================================
# LOGIN
# =========================================================


def test_login_success():
    email = unique_email("login_test_user")

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": "Login Test User",
            "password": "StrongPassword123!",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20


def test_login_wrong_password_is_rejected():
    email = unique_email("wrong_password_test")

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": "Wrong Password User",
            "password": "CorrectPassword123!",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_nonexistent_user_is_rejected():
    email = unique_email("does_not_exist")

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "SomePassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


# =========================================================
# PROTECTED API
# =========================================================


def test_projects_endpoint_requires_authentication():
    response = client.get("/api/projects")

    assert response.status_code == 401


def test_projects_endpoint_rejects_invalid_token():
    response = client.get(
        "/api/projects",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401


def test_projects_endpoint_accepts_valid_token():
    email = unique_email("protected_test_user")

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": "Protected Test User",
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

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/projects",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)