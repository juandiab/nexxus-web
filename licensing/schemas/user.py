from pydantic import BaseModel, EmailStr, Field

from schemas.auth import Role, UserResponse


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=2, max_length=64)
    displayName: str = Field(min_length=1, max_length=128)
    email: EmailStr
    role: Role = "user"


class UserUpdateRequest(BaseModel):
    displayName: str = Field(min_length=1, max_length=128)
    email: EmailStr
    role: Role


class UserActiveRequest(BaseModel):
    active: bool


class PasskeyItem(BaseModel):
    id: str
    label: str
    createdAt: object | None = None
    lastUsedAt: object | None = None


class UserListItem(UserResponse):
    pass


class UserDetailResponse(UserResponse):
    passkeys: list[PasskeyItem] = []
