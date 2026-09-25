from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password
)
from app.models.user import User
from app.schemas.auth import LoginRequest


def authenticate_user(
    db: Session,
    login_data: LoginRequest
) -> str | None:
    """
    Authenticate a user and return a JWT access token.

    Returns None when the credentials are invalid
    or the account is inactive.
    """

    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        login_data.password,
        user.hashed_password
    ):
        return None

    return create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role
    )