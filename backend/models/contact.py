from pydantic import BaseModel, EmailStr, field_validator


class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    company: str = ""
    service: str = ""
    message: str

    @field_validator("name", "message")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("message")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 10:
            raise ValueError("Message must be at least 10 characters")
        return v


class ContactResponse(BaseModel):
    success: bool
    message: str
