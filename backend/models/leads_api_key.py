from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

LeadsApiKeyAgent = Literal["leads", "chief-of-staff"]
LEADS_API_SCOPES = ("leads:write",)


class LeadsApiKeyCreate(BaseModel):
    name: str
    agent: LeadsApiKeyAgent = "leads"
    scopes: list[str] = Field(default_factory=lambda: ["leads:write"])

    @field_validator("name")
    @classmethod
    def name_required(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Name is required")
        return cleaned

    @field_validator("scopes")
    @classmethod
    def scopes_valid(cls, v: list[str]) -> list[str]:
        cleaned = [s.strip() for s in v if s.strip()]
        if not cleaned:
            return ["leads:write"]
        invalid = [s for s in cleaned if s not in LEADS_API_SCOPES]
        if invalid:
            raise ValueError(f"Invalid scopes: {', '.join(invalid)}")
        return cleaned


class LeadsApiKey(BaseModel):
    id: str
    name: str
    key_prefix: str
    agent: LeadsApiKeyAgent
    scopes: list[str]
    created_by: str
    created_at: datetime
    last_used_at: datetime | None = None
    revoked_at: datetime | None = None


class LeadsApiKeyCreated(BaseModel):
    id: str
    name: str
    key_prefix: str
    agent: LeadsApiKeyAgent
    scopes: list[str]
    api_key: str
    created_at: datetime
