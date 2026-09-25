from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    AdminUserCreateRequest,
    AdminUserUpdateRequest,
    UserResponse,
)


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


def get_user_or_404(
    db: Session,
    user_id: int,
) -> User:
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


def count_active_admins(db: Session) -> int:
    return (
        db.query(User)
        .filter(
            User.role == "admin",
            User.is_active.is_(True),
        )
        .count()
    )


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: AdminUserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/users",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return (
        db.query(User)
        .order_by(User.id.asc())
        .all()
    )


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user_data: AdminUserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    user = get_user_or_404(
        db,
        user_id,
    )

    resulting_role = (
        user_data.role
        if user_data.role is not None
        else user.role
    )

    resulting_active_state = (
        user_data.is_active
        if user_data.is_active is not None
        else user.is_active
    )

    # -----------------------------------------------------
    # LAST ACTIVE ADMIN PROTECTION
    # -----------------------------------------------------

    is_currently_active_admin = (
        user.role == "admin"
        and user.is_active
    )

    will_stop_being_active_admin = (
        resulting_role != "admin"
        or not resulting_active_state
    )

    if (
        is_currently_active_admin
        and will_stop_being_active_admin
        and count_active_admins(db) <= 1
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The last active administrator "
                "cannot be removed or deactivated."
            ),
        )

    # -----------------------------------------------------
    # APPLY USER CHANGES
    # -----------------------------------------------------

    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.role is not None:
        user.role = user_data.role

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user