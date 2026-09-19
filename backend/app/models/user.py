from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utc_now() -> datetime:
    """
    Return the current UTC time as a naive datetime.

    The database currently uses DateTime(timezone=False), so we keep
    the stored representation compatible with the existing schema
    while avoiding deprecated datetime.utcnow().
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    """
    Aurex User Model.

    Stores authentication and authorization information
    for users accessing the Aurex platform.
    """

    __tablename__ = "users"

    # =========================================================
    # PRIMARY KEY
    # =========================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =========================================================
    # USER INFORMATION
    # =========================================================

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # =========================================================
    # AUTHORIZATION
    # =========================================================

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="viewer",
        index=True,
    )

    # =========================================================
    # ACCOUNT STATUS
    # =========================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )