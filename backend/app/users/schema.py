from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.users.enums import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.EMPLOYEE


class UserUpdate(BaseModel):
    full_name: str = Field(min_length=3, max_length=100)
    role: UserRole
    is_active: bool


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)