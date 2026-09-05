from datetime import datetime
from typing import Literal, Self
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

LeadSource = Literal["web_form", "referral", "manual", "linkedin", "other", "api"]
LeadStatus = Literal[
    "new",
    "researching",
    "proposal_draft",
    "proposal_sent",
    "negotiation",
    "won",
    "lost",
    "nurture",
]
LeadLocale = Literal["en", "es"]
PackageInterest = Literal["diagnostic", "pilot", "system", "retainer", "unknown"]
ProposalStatus = Literal["none", "draft", "sent", "accepted", "rejected"]
TimelineEventType = Literal["created", "status_changed", "proposal_sent", "note_added"]
ProposalKind = Literal["draft", "final"]
ProposalLanguage = Literal["en", "es"]
LeadsApiAgent = Literal["leads", "chief-of-staff"]

DEFAULT_OWNER = "JP / business@nexxus-tech.com"

LEAD_SOURCES: tuple[str, ...] = (
    "web_form",
    "referral",
    "manual",
    "linkedin",
    "other",
    "api",
)
LEAD_STATUSES: tuple[str, ...] = (
    "new",
    "researching",
    "proposal_draft",
    "proposal_sent",
    "negotiation",
    "won",
    "lost",
    "nurture",
)
PACKAGE_INTERESTS: tuple[str, ...] = (
    "diagnostic",
    "pilot",
    "system",
    "retainer",
    "unknown",
)
PROPOSAL_STATUSES: tuple[str, ...] = ("none", "draft", "sent", "accepted", "rejected")


class TimelineEvent(BaseModel):
    type: TimelineEventType
    at: datetime
    detail: str = ""
    by: str = "system"


class LeadProposal(BaseModel):
    id: str
    kind: ProposalKind
    language: ProposalLanguage
    filename: str
    storage_path: str
    email_subject: str = ""
    email_body: str = ""
    notes: str = ""
    uploaded_at: datetime
    uploaded_by_agent: LeadsApiAgent = "leads"


class LeadBase(BaseModel):
    company_name: str
    website: str = ""
    contact_name: str = ""
    contact_email: EmailStr | None = None
    contact_phone: str = ""
    country: str = ""
    locale: LeadLocale = "en"
    source: LeadSource = "manual"
    status: LeadStatus = "new"
    package_interest: PackageInterest = "unknown"
    notes: str = ""
    research_summary: str = ""
    proposal_status: ProposalStatus = "none"
    proposal_sent_at: datetime | None = None
    owner: str = DEFAULT_OWNER
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    utm_term: str = ""
    utm_content: str = ""

    @field_validator("company_name")
    @classmethod
    def company_required(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Company name is required")
        return cleaned

    @field_validator(
        "website",
        "contact_name",
        "contact_phone",
        "country",
        "notes",
        "research_summary",
        "owner",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
    )
    @classmethod
    def strip_optional(cls, v: str) -> str:
        return (v or "").strip()

    @field_validator("contact_email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v: str | None) -> str | None:
        if v is None or not str(v).strip():
            return None
        return str(v).strip()


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    company_name: str | None = None
    website: str | None = None
    contact_name: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    country: str | None = None
    locale: LeadLocale | None = None
    source: LeadSource | None = None
    status: LeadStatus | None = None
    package_interest: PackageInterest | None = None
    notes: str | None = None
    research_summary: str | None = None
    proposal_status: ProposalStatus | None = None
    proposal_sent_at: datetime | None = None
    owner: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_term: str | None = None
    utm_content: str | None = None

    @field_validator("company_name")
    @classmethod
    def company_not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Company name cannot be empty")
        return v.strip() if v is not None else None

    @field_validator("contact_email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v: str | None) -> str | None:
        if v is None or not str(v).strip():
            return None
        return str(v).strip()


class LeadNoteCreate(BaseModel):
    note: str

    @field_validator("note")
    @classmethod
    def note_required(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Note cannot be empty")
        return cleaned


class Lead(BaseModel):
    id: str
    company_name: str
    website: str = ""
    contact_name: str = ""
    contact_email: str | None = None
    contact_phone: str = ""
    country: str = ""
    locale: LeadLocale = "en"
    source: LeadSource = "manual"
    status: LeadStatus = "new"
    package_interest: PackageInterest = "unknown"
    notes: str = ""
    research_summary: str = ""
    proposal_status: ProposalStatus = "none"
    proposal_sent_at: datetime | None = None
    owner: str = DEFAULT_OWNER
    created_at: datetime
    updated_at: datetime
    last_touch_at: datetime
    archived: bool = False
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    utm_term: str = ""
    utm_content: str = ""
    timeline: list[TimelineEvent] = Field(default_factory=list)
    idempotency_key: str | None = None
    external_id: str | None = None
    proposals: list[LeadProposal] = Field(default_factory=list)
    last_api_sync_at: datetime | None = None
    last_api_agent: LeadsApiAgent | None = None


class WebFormLeadInput(BaseModel):
    """Payload for creating a lead from public website forms."""

    company_name: str
    contact_name: str = ""
    contact_email: EmailStr | None = None
    contact_phone: str = ""
    country: str = ""
    locale: LeadLocale = "en"
    package_interest: PackageInterest = "unknown"
    notes: str = ""
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    utm_term: str = ""
    utm_content: str = ""

    @model_validator(mode="after")
    def require_contact(self) -> Self:
        if not self.company_name.strip():
            raise ValueError("Company name is required")
        return self


def new_lead_id() -> str:
    return str(uuid4())


def new_proposal_id() -> str:
    return str(uuid4())


class LeadIngestCreate(BaseModel):
    company_name: str
    website: str = ""
    contact_name: str = ""
    contact_email: EmailStr | None = None
    contact_phone: str = ""
    country: str = ""
    locale: LeadLocale = "en"
    status: LeadStatus = "new"
    package_interest: PackageInterest = "unknown"
    research_summary: str = ""
    notes: str = ""
    note: str = ""
    external_id: str | None = None
    idempotency_key: str | None = None

    @field_validator("company_name")
    @classmethod
    def company_required(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Company name is required")
        return cleaned

    @field_validator(
        "website",
        "contact_name",
        "contact_phone",
        "country",
        "research_summary",
        "notes",
        "note",
        "external_id",
        "idempotency_key",
    )
    @classmethod
    def strip_optional(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.strip()

    @field_validator("contact_email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v: str | None) -> str | None:
        if v is None or not str(v).strip():
            return None
        return str(v).strip()


class LeadIngestUpdate(BaseModel):
    company_name: str | None = None
    website: str | None = None
    contact_name: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    country: str | None = None
    locale: LeadLocale | None = None
    status: LeadStatus | None = None
    package_interest: PackageInterest | None = None
    research_summary: str | None = None
    notes: str | None = None
    note: str | None = None
    proposal_status: ProposalStatus | None = None
    proposal_sent_at: datetime | None = None
    external_id: str | None = None

    @field_validator("company_name")
    @classmethod
    def company_not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Company name cannot be empty")
        return v.strip() if v is not None else None

    @field_validator("contact_email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v: str | None) -> str | None:
        if v is None or not str(v).strip():
            return None
        return str(v).strip()


class LeadIngestResponse(BaseModel):
    id: str
    admin_url: str
    existing: bool = False


class LeadListPage(BaseModel):
    items: list[Lead]
    page: int
    limit: int
    total: int
    pages: int
