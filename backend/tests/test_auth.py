import uuid

import pytest

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

@pytest.fixture(autouse=True)
def clean_test_database():
    from app.models.user import User

    # Re-assert this test module's database override before every test.
    # Other test modules may modify the global FastAPI override.
    previous_override = app.dependency_overrides.get(get_db)

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()

    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

    yield

    # Restore whatever override existed before this test.
    if previous_override is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = previous_override
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


# =========================================================
# ADMIN USER MANAGEMENT
# =========================================================


def create_admin_and_get_token():
    from app.core.security import hash_password
    from app.models.user import User

    email = unique_email("admin_test")

    db = TestingSessionLocal()

    try:
        admin = User(
            email=email,
            full_name="Test Administrator",
            hashed_password=hash_password("AdminPassword123!"),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

    finally:
        db.close()

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "AdminPassword123!",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_non_admin_cannot_access_user_management():
    email = unique_email("normal_user")

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "full_name": "Normal User",
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
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_admin_can_create_user():
    token = create_admin_and_get_token()

    email = unique_email("created_by_admin")

    response = client.post(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "Created Analyst",
            "password": "StrongPassword123!",
            "role": "analyst",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["full_name"] == "Created Analyst"
    assert data["role"] == "analyst"
    assert data["is_active"] is True

    assert "password" not in data
    assert "hashed_password" not in data


def test_admin_cannot_create_user_with_invalid_role():
    token = create_admin_and_get_token()

    response = client.post(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": unique_email("invalid_role"),
            "full_name": "Invalid Role User",
            "password": "StrongPassword123!",
            "role": "superuser",
        },
    )

    assert response.status_code == 422


def test_admin_cannot_create_duplicate_user():
    token = create_admin_and_get_token()

    email = unique_email("duplicate_admin_create")

    first_response = client.post(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "First User",
            "password": "StrongPassword123!",
            "role": "viewer",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "Second User",
            "password": "StrongPassword123!",
            "role": "viewer",
        },
    )

    assert second_response.status_code == 409


def test_admin_can_list_users():
    token = create_admin_and_get_token()

    response = client.get(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    for user in data:
        assert "id" in user
        assert "email" in user
        assert "role" in user
        assert "is_active" in user

        assert "hashed_password" not in user
        assert "password" not in user


def test_admin_can_update_user_role():
    token = create_admin_and_get_token()

    email = unique_email("role_update")

    create_response = client.post(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "Role Update User",
            "password": "StrongPassword123!",
            "role": "viewer",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/admin/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "role": "analyst",
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["role"] == "analyst"


def test_admin_can_deactivate_user():
    token = create_admin_and_get_token()

    email = unique_email("deactivate_user")

    create_response = client.post(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "Deactivate User",
            "password": "StrongPassword123!",
            "role": "viewer",
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/admin/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "is_active": False,
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["is_active"] is False

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 403

    assert (
        login_response.json()["detail"]
        == "User account is inactive."
    )


def test_last_active_admin_cannot_be_deactivated():
    token = create_admin_and_get_token()

    response = client.get(
        "/api/admin/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    admins = [
        user
        for user in response.json()
        if user["role"] == "admin"
        and user["is_active"] is True
    ]

    assert len(admins) >= 1

    admin_id = admins[0]["id"]

    update_response = client.put(
        f"/api/admin/users/{admin_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "is_active": False,
        },
    )

    assert update_response.status_code == 409