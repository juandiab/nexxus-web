from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

Role = Literal["admin", "blog", "licensing", "user"]


class UserResponse(BaseModel):
    id: str
    username: str
    displayName: str
    email: str | None = None
    role: Role
    active: bool = True
    mustChangePassword: bool = False
    passkeyRequired: bool = False
    passkeyCount: int = 0
    setupComplete: bool = False
    createdAt: datetime | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    user: UserResponse


class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str = Field(min_length=8)


class MessageResponse(BaseModel):
    message: str
