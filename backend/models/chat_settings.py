from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ChatProvider = Literal["openai", "anthropic", "gemini", "deepseek", "openrouter"]

VALID_PROVIDERS: frozenset[str] = frozenset(
    {"openai", "anthropic", "gemini", "deepseek", "openrouter"}
)

PROVIDER_DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-sonnet-4-20250514",
    "gemini": "gemini-2.0-flash",
    "deepseek": "deepseek-chat",
    "openrouter": "openai/gpt-4o-mini",
}


class ModelOption(BaseModel):
    id: str
    label: str


class ProviderOption(BaseModel):
    id: str
    label: str
    defaultModel: str
    models: list[ModelOption] = Field(default_factory=list)


class ChatSettingsResponse(BaseModel):
    provider: str
    model: str
    enabled: bool
    configured: bool
    apiKeyMasked: str = ""
    updatedAt: datetime | None = None
    updatedBy: str | None = None
    providers: list[ProviderOption]
    models: list[ModelOption] = Field(default_factory=list)


class ProviderModelsResponse(BaseModel):
    provider: str
    defaultModel: str
    models: list[ModelOption]


class ChatSettingsWrite(BaseModel):
    provider: str = Field(min_length=1, max_length=32)
    model: str = Field(min_length=1, max_length=128)
    enabled: bool = True
    apiKey: str = Field(default="", max_length=512)


class ChatSettingsTestResponse(BaseModel):
    success: bool
    message: str
    replyPreview: str = ""
