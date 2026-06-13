from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable

from config import settings
from crypto import decrypt, encrypt
from db import get_database
from models.chat_settings import PROVIDER_DEFAULT_MODELS, VALID_PROVIDERS

COLLECTION = "chat_settings"


@dataclass(frozen=True)
class RuntimeLlmConfig:
    provider: str
    model: str
    api_key: str
    enabled: bool

    @property
    def configured(self) -> bool:
        return bool(self.enabled and self.provider and self.model and self.api_key)


def _mask_api_key(api_key: str) -> str:
    if not api_key:
        return ""
    if len(api_key) <= 4:
        return "••••"
    return f"{'•' * 8}{api_key[-4:]}"


def _normalize_provider(provider: str) -> str:
    return provider.strip().lower()


def _normalize_model(model: str, provider: str) -> str:
    cleaned = model.strip()
    if cleaned:
        return cleaned
    return PROVIDER_DEFAULT_MODELS.get(provider, "")


async def _load_document(settings_id: str) -> dict[str, Any] | None:
    db = get_database()
    return await db[COLLECTION].find_one({"_id": settings_id})


def _doc_to_runtime(doc: dict[str, Any]) -> RuntimeLlmConfig:
    provider = _normalize_provider(str(doc.get("provider", "")))
    model = _normalize_model(str(doc.get("model", "")), provider)
    encrypted = str(doc.get("apiKeyEncrypted", "")).strip()
    api_key = decrypt(encrypted) if encrypted else ""
    return RuntimeLlmConfig(
        provider=provider,
        model=model,
        api_key=api_key,
        enabled=bool(doc.get("enabled", True)),
    )


def _empty_runtime(*, provider: str = "deepseek", model: str = "") -> RuntimeLlmConfig:
    return RuntimeLlmConfig(
        provider=provider,
        model=model or PROVIDER_DEFAULT_MODELS.get(provider, ""),
        api_key="",
        enabled=False,
    )


async def get_runtime_config(
    settings_id: str,
    *,
    env_fallback: Callable[[], RuntimeLlmConfig] | None = None,
) -> RuntimeLlmConfig:
    try:
        doc = await _load_document(settings_id)
    except Exception:
        return env_fallback() if env_fallback else _empty_runtime()

    if not doc:
        return env_fallback() if env_fallback else _empty_runtime()

    try:
        return _doc_to_runtime(doc)
    except ValueError:
        return env_fallback() if env_fallback else _empty_runtime()


async def get_admin_settings_view(
    settings_id: str,
    *,
    default_provider: str = "deepseek",
    env_fallback: Callable[[], RuntimeLlmConfig] | None = None,
) -> dict[str, Any]:
    doc = await _load_document(settings_id)
    if doc:
        runtime = _doc_to_runtime(doc)
        return {
            "provider": runtime.provider,
            "model": runtime.model,
            "enabled": runtime.enabled,
            "configured": bool(runtime.api_key),
            "apiKeyMasked": _mask_api_key(runtime.api_key),
            "updatedAt": doc.get("updatedAt"),
            "updatedBy": doc.get("updatedBy"),
        }

    fallback = env_fallback() if env_fallback else _empty_runtime(provider=default_provider)
    return {
        "provider": fallback.provider or default_provider,
        "model": fallback.model or PROVIDER_DEFAULT_MODELS.get(default_provider, ""),
        "enabled": fallback.enabled,
        "configured": bool(fallback.api_key),
        "apiKeyMasked": _mask_api_key(fallback.api_key),
        "updatedAt": None,
        "updatedBy": None,
    }


async def save_admin_settings(
    settings_id: str,
    *,
    provider: str,
    model: str,
    enabled: bool,
    api_key: str | None,
    updated_by: str,
) -> dict[str, Any]:
    cleaned_provider = _normalize_provider(provider)
    if cleaned_provider not in VALID_PROVIDERS:
        raise ValueError(f"Unsupported provider '{provider}'")

    cleaned_model = _normalize_model(model, cleaned_provider)
    if not cleaned_model:
        raise ValueError("Model is required")

    existing = await _load_document(settings_id)
    encrypted_key = ""
    if existing and existing.get("apiKeyEncrypted"):
        encrypted_key = str(existing["apiKeyEncrypted"])

    if api_key is not None and api_key.strip():
        if not settings.encryption_key.strip():
            raise ValueError("ENCRYPTION_KEY is not configured on the server")
        encrypted_key = encrypt(api_key.strip())

    if not encrypted_key:
        raise ValueError("API key is required")

    doc = {
        "_id": settings_id,
        "provider": cleaned_provider,
        "model": cleaned_model,
        "apiKeyEncrypted": encrypted_key,
        "enabled": enabled,
        "updatedAt": datetime.now(UTC),
        "updatedBy": updated_by,
    }
    db = get_database()
    await db[COLLECTION].replace_one({"_id": settings_id}, doc, upsert=True)
    return await get_admin_settings_view(settings_id, default_provider=cleaned_provider)
