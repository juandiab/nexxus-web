from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

from models.chat_settings import PROVIDER_DEFAULT_MODELS, VALID_PROVIDERS

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_CACHE_TTL_SECONDS = 3600

_openrouter_cache: tuple[float, list[dict[str, str]]] | None = None


@dataclass(frozen=True)
class ModelOption:
    id: str
    label: str


STATIC_MODELS: dict[str, list[ModelOption]] = {
    "openai": [
        ModelOption("gpt-4o", "GPT-4o"),
        ModelOption("gpt-4o-mini", "GPT-4o Mini"),
        ModelOption("gpt-4-turbo", "GPT-4 Turbo"),
        ModelOption("gpt-4.1", "GPT-4.1"),
        ModelOption("gpt-4.1-mini", "GPT-4.1 Mini"),
        ModelOption("o3-mini", "o3-mini"),
        ModelOption("o1-mini", "o1-mini"),
    ],
    "anthropic": [
        ModelOption("claude-sonnet-4-20250514", "Claude Sonnet 4"),
        ModelOption("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet"),
        ModelOption("claude-3-5-haiku-20241022", "Claude 3.5 Haiku"),
        ModelOption("claude-3-opus-20240229", "Claude 3 Opus"),
    ],
    "gemini": [
        ModelOption("gemini-2.0-flash", "Gemini 2.0 Flash"),
        ModelOption("gemini-2.0-flash-lite", "Gemini 2.0 Flash Lite"),
        ModelOption("gemini-1.5-pro", "Gemini 1.5 Pro"),
        ModelOption("gemini-1.5-flash", "Gemini 1.5 Flash"),
    ],
    "deepseek": [
        ModelOption("deepseek-chat", "DeepSeek Chat"),
        ModelOption("deepseek-reasoner", "DeepSeek Reasoner"),
    ],
    "openrouter": [
        ModelOption("openai/gpt-4o-mini", "OpenAI GPT-4o Mini"),
        ModelOption("anthropic/claude-3.5-sonnet", "Anthropic Claude 3.5 Sonnet"),
        ModelOption("google/gemini-2.0-flash-001", "Google Gemini 2.0 Flash"),
        ModelOption("deepseek/deepseek-chat", "DeepSeek Chat"),
    ],
}


def _serialize_models(models: list[ModelOption]) -> list[dict[str, str]]:
    return [{"id": model.id, "label": model.label} for model in models]


def _ensure_current_model(models: list[ModelOption], current_model: str) -> list[ModelOption]:
    if not current_model:
        return models
    if any(model.id == current_model for model in models):
        return models
    return [ModelOption(current_model, f"{current_model} (saved)"), *models]


async def _fetch_openrouter_models() -> list[ModelOption]:
    global _openrouter_cache
    now = time.time()
    if _openrouter_cache and now - _openrouter_cache[0] < OPENROUTER_CACHE_TTL_SECONDS:
        return [ModelOption(item["id"], item["label"]) for item in _openrouter_cache[1]]

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(OPENROUTER_MODELS_URL)
        resp.raise_for_status()
        payload = resp.json()

    models: list[ModelOption] = []
    for entry in payload.get("data") or []:
        model_id = str(entry.get("id") or "").strip()
        if not model_id:
            continue
        name = str(entry.get("name") or model_id).strip()
        pricing = entry.get("pricing") or {}
        if pricing.get("prompt") is None and pricing.get("completion") is None:
            continue
        models.append(ModelOption(model_id, name))

    models.sort(key=lambda item: item.label.lower())
    if not models:
        models = list(STATIC_MODELS["openrouter"])

    serialized = _serialize_models(models)
    _openrouter_cache = (now, serialized)
    return models


async def get_models_for_provider(provider: str, *, current_model: str = "") -> list[ModelOption]:
    cleaned = provider.strip().lower()
    if cleaned not in VALID_PROVIDERS:
        raise ValueError(f"Unsupported provider '{provider}'")

    if cleaned == "openrouter":
        try:
            models = await _fetch_openrouter_models()
        except Exception:
            models = list(STATIC_MODELS["openrouter"])
    else:
        models = list(STATIC_MODELS[cleaned])

    return _ensure_current_model(models, current_model.strip())


def default_model_for_provider(provider: str) -> str:
    return PROVIDER_DEFAULT_MODELS.get(provider.strip().lower(), "")
