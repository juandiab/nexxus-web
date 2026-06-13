from __future__ import annotations

from services.llm_settings_store import (
    RuntimeLlmConfig,
    get_admin_settings_view as _get_admin_view,
    get_runtime_config as _get_runtime,
    save_admin_settings as _save_admin,
)

SETTINGS_ID = "blog_assistant"


async def get_runtime_config() -> RuntimeLlmConfig:
    return await _get_runtime(SETTINGS_ID)


async def get_admin_settings_view() -> dict:
    return await _get_admin_view(SETTINGS_ID, default_provider="openai")


async def save_admin_settings(**kwargs) -> dict:
    return await _save_admin(SETTINGS_ID, **kwargs)
