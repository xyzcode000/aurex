from pydantic import BaseModel, EmailStr, Field
from typing import Literal


Role = Literal["admin", "project_manager", "analyst", "viewer"]


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    role: Role


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    role: Role | None = None


class UserDeactivate(BaseModel):
    is_active: bool


class UserManagementResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: Role
    is_active: bool