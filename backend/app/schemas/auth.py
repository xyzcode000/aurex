from typing import Literal

from pydantic import BaseModel, EmailStr, Field


# =========================================================
# ROLE DEFINITIONS
# =========================================================

UserRole = Literal[
    "admin",
    "project_manager",
    "analyst",
    "viewer",
]


# =========================================================
# REGISTER
# =========================================================

class RegisterRequest(BaseModel):
    email: EmailStr

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
    )


# =========================================================
# LOGIN
# =========================================================

class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        ...,
        min_length=1,
        max_length=72,
    )


# =========================================================
# USER RESPONSE
# =========================================================

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool

    model_config = {
        "from_attributes": True,
    }


# =========================================================
# TOKEN RESPONSE
# =========================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================================================
# ADMIN USER CREATION
# =========================================================

class AdminUserCreateRequest(BaseModel):
    email: EmailStr

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
    )

    role: UserRole = "viewer"


# =========================================================
# ADMIN USER UPDATE
# =========================================================

class AdminUserUpdateRequest(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    role: UserRole | None = None

    is_active: bool | None = None