from pydantic import BaseModel, EmailStr, Field, field_validator

ALLOWED_SERVICES = [
    "WAF & API Protection",
    "NetScaler / ADC",
    "Zero-Trust Architecture",
    "Multicloud Security",
    "AI & Automation",
    "Citrix Virtual Apps & Desktops",
    "Other / Discovery Call",
]

ALLOWED_CRITICALITY = [
    "Planning — not happening yet",
    "Low — minor impact",
    "Medium — degraded service",
    "High — major impact",
    "Critical — production down",
]

ALLOWED_TECHNOLOGIES = [
    "NetScaler ADC",
    "NetScaler Gateway",
    "F5 BIG-IP",
    "Citrix Virtual Apps & Desktops",
    "Citrix Cloud",
    "Okta / Identity",
    "Other",
]

ALLOWED_ENQUIRY_TYPES = [
    "Troubleshooting / incident",
    "Support request",
    "New project / implementation",
    "Assessment / discovery",
    "General enquiry",
]

MAX_MESSAGE_LEN = 2000
MAX_HISTORY_MESSAGES = 40


class ChatMessage(BaseModel):
    role: str
    content: str

    @field_validator("role")
    @classmethod
    def valid_role(cls, v: str) -> str:
        if v not in ("user", "assistant"):
            raise ValueError("Invalid message role")
        return v

    @field_validator("content")
    @classmethod
    def bounded_content(cls, v: str) -> str:
        text = v.strip()
        if not text:
            raise ValueError("Message cannot be empty")
        if len(text) > MAX_MESSAGE_LEN:
            raise ValueError(f"Message exceeds {MAX_MESSAGE_LEN} characters")
        return text


class ChatProfile(BaseModel):
    enquiry_type: str
    name: str
    email: EmailStr
    company: str = ""
    service: str
    criticality: str = ""
    users_affected: str = ""
    technologies: list[str] = Field(default_factory=list)
    technology_other: str = ""
    platform_version: str = ""
    platform_model: str = ""

    @field_validator("enquiry_type")
    @classmethod
    def enquiry_type_ok(cls, v: str) -> str:
        t = v.strip()
        if t not in ALLOWED_ENQUIRY_TYPES:
            raise ValueError("Invalid enquiry type")
        return t

    @field_validator("name")
    @classmethod
    def name_ok(cls, v: str) -> str:
        name = v.strip()
        if len(name) < 2:
            raise ValueError("Name is too short")
        if len(name) > 120:
            raise ValueError("Name is too long")
        return name

    @field_validator("company", "technology_other", "platform_version", "platform_model")
    @classmethod
    def strip_bounded(cls, v: str) -> str:
        return v.strip()[:200]

    @field_validator("users_affected")
    @classmethod
    def users_ok(cls, v: str) -> str:
        text = v.strip()
        if len(text) > 200:
            raise ValueError("Users affected is too long")
        return text or "Not specified"

    @field_validator("criticality")
    @classmethod
    def criticality_default(cls, v: str) -> str:
        c = v.strip()
        if not c:
            return "Planning — not happening yet"
        if c not in ALLOWED_CRITICALITY:
            raise ValueError("Invalid criticality selection")
        return c

    @field_validator("service")
    @classmethod
    def service_ok(cls, v: str) -> str:
        service = v.strip()
        if service not in ALLOWED_SERVICES:
            raise ValueError("Invalid service selection")
        return service

    @field_validator("technologies")
    @classmethod
    def technologies_ok(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("Select at least one technology")
        cleaned = []
        for t in v:
            t = t.strip()
            if t not in ALLOWED_TECHNOLOGIES:
                raise ValueError(f"Invalid technology: {t}")
            if t not in cleaned:
                cleaned.append(t)
        return cleaned


class ChatRequest(BaseModel):
    profile: ChatProfile
    messages: list[ChatMessage] = Field(default_factory=list, max_length=MAX_HISTORY_MESSAGES)


class ChatResponse(BaseModel):
    reply: str
    configured: bool
    ready_to_submit: bool = False


class ChatSubmitRequest(BaseModel):
    profile: ChatProfile
    messages: list[ChatMessage] = Field(default_factory=list, max_length=MAX_HISTORY_MESSAGES)


class ChatSubmitResponse(BaseModel):
    success: bool
    message: str


class ChatOptionsResponse(BaseModel):
    services: list[str]
    criticality: list[str]
    technologies: list[str]
    enquiry_types: list[str]
