from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User


# =========================================================
# BEARER AUTHENTICATION
# =========================================================

security = HTTPBearer(
    auto_error=False,
)


# =========================================================
# CURRENT AUTHENTICATED USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        security
    ),
    db: Session = Depends(get_db),
) -> User:
    """
    Authenticate the current request using a JWT.

    Flow:
        Request
          ↓
        Bearer Token
          ↓
        Decode JWT
          ↓
        Extract User ID
          ↓
        Find User
          ↓
        Check Account Status
          ↓
        Authenticated User
    """

    # -----------------------------------------------------
    # AUTHORIZATION HEADER
    # -----------------------------------------------------

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    token = credentials.credentials

    # -----------------------------------------------------
    # DECODE JWT
    # -----------------------------------------------------

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # -----------------------------------------------------
    # EXTRACT USER ID
    # -----------------------------------------------------

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # -----------------------------------------------------
    # CHECK ACCOUNT STATUS
    # -----------------------------------------------------

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user


# =========================================================
# ROLE-BASED AUTHORIZATION
# =========================================================

def require_roles(*allowed_roles: str) -> Callable:
    """
    Creates a reusable role authorization dependency.

    Examples:

        Depends(require_roles("admin"))

    or:

        Depends(
            require_roles(
                "admin",
                "project_manager",
            )
        )
    """

    def role_checker(
        current_user: User = Depends(
            get_current_user
        ),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have permission "
                    "to perform this action."
                ),
            )

        return current_user

    return role_checker