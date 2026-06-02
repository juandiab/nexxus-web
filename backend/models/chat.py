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
    name: str
    email: EmailStr
    company: str = ""
    service: str

    @field_validator("name")
    @classmethod
    def name_ok(cls, v: str) -> str:
        name = v.strip()
        if len(name) < 2:
            raise ValueError("Name is too short")
        if len(name) > 120:
            raise ValueError("Name is too long")
        return name

    @field_validator("company")
    @classmethod
    def company_ok(cls, v: str) -> str:
        return v.strip()[:200]

    @field_validator("service")
    @classmethod
    def service_ok(cls, v: str) -> str:
        service = v.strip()
        if service not in ALLOWED_SERVICES:
            raise ValueError("Invalid service selection")
        return service


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
    contact_message: str = ""
