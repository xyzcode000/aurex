from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_management import (
    UserCreate,
    UserUpdate,
    UserDeactivate,
    UserManagementResponse,
)
from app.services.user_management_service import (
    create_user,
    get_all_users,
    update_user,
    set_user_active_status,
)
from app.core.dependencies import require_admin


router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)


@router.post(
    "/",
    response_model=UserManagementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = create_user(db, user_data)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    return user


@router.get(
    "/",
    response_model=list[UserManagementResponse],
)
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return get_all_users(db)


@router.put(
    "/{user_id}",
    response_model=UserManagementResponse,
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = update_user(
        db,
        user_id,
        user_data,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.patch(
    "/{user_id}/status",
    response_model=UserManagementResponse,
)
def change_user_status(
    user_id: int,
    status_data: UserDeactivate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = set_user_active_status(
        db,
        user_id,
        status_data.is_active,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user