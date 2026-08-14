from typing import Literal, Self

from pydantic import BaseModel, EmailStr, field_validator, model_validator

JPILOT_USE_TYPES = ("company", "consultant", "personal")
JPILOT_COMPANY_SIZES = ("1–10", "11–50", "51–200", "201–1000", "1000+")
_JPILOT_SIZE_ALIASES = {
    "1-10": "1–10",
    "11-50": "11–50",
    "51-200": "51–200",
    "201-1000": "201–1000",
    "1000+": "1000+",
}


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


class JpilotInterestRequest(BaseModel):
    name: str
    email: EmailStr
    use_type: Literal["company", "consultant", "personal"]
    country: str
    company: str = ""
    company_size: str = ""

    @field_validator("name", "country")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("company", "company_size")
    @classmethod
    def strip_optional(cls, v: str) -> str:
        return (v or "").strip()

    @field_validator("company_size")
    @classmethod
    def normalize_size(cls, v: str) -> str:
        if not v:
            return ""
        return _JPILOT_SIZE_ALIASES.get(v, v)

    @model_validator(mode="after")
    def validate_conditional_fields(self) -> Self:
        if self.use_type == "company":
            if not self.company:
                raise ValueError("Company is required when use type is Company")
            if self.company_size not in JPILOT_COMPANY_SIZES:
                raise ValueError("Company size is required when use type is Company")
        elif self.use_type == "personal":
            self.company = ""
            self.company_size = ""
        else:
            self.company_size = ""
        return self


class ContactResponse(BaseModel):
    success: bool
    message: str
