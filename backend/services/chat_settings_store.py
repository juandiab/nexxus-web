from __future__ import annotations

from config import settings
from models.chat_settings import PROVIDER_DEFAULT_MODELS, VALID_PROVIDERS
from services.llm_settings_store import (
    RuntimeLlmConfig,
    get_admin_settings_view as _get_admin_view,
    get_runtime_config as _get_runtime,
    save_admin_settings as _save_admin,
)

RuntimeChatConfig = RuntimeLlmConfig

SETTINGS_ID = "jpbot"


def _env_fallback_config() -> RuntimeLlmConfig:
    provider = settings.ai_provider.strip().lower()
    if provider not in VALID_PROVIDERS:
        provider = "deepseek" if settings.ai_api_key else "deepseek"
    model = settings.ai_model.strip() or PROVIDER_DEFAULT_MODELS.get(provider, "")
    return RuntimeLlmConfig(
        provider=provider,
        model=model,
        api_key=settings.ai_api_key.strip(),
        enabled=bool(settings.ai_api_key.strip()),
    )


async def get_runtime_config() -> RuntimeLlmConfig:
    return await _get_runtime(SETTINGS_ID, env_fallback=_env_fallback_config)


async def get_admin_settings_view() -> dict:
    return await _get_admin_view(SETTINGS_ID, env_fallback=_env_fallback_config)


async def save_admin_settings(**kwargs) -> dict:
    return await _save_admin(SETTINGS_ID, **kwargs)
