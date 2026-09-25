from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user_management import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        return None

    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_all_users(db: Session):
    return db.query(User).order_by(User.id).all()


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.role is not None:
        user.role = user_data.role

    db.commit()
    db.refresh(user)

    return user


def set_user_active_status(
    db: Session,
    user_id: int,
    is_active: bool
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return user