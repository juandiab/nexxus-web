from __future__ import annotations

import httpx

from models.chat_settings import PROVIDER_DEFAULT_MODELS, VALID_PROVIDERS
from services.llm_settings_store import RuntimeLlmConfig

OPENAI_COMPAT_BASE_URLS = {
    "openai": "https://api.openai.com",
    "deepseek": "https://api.deepseek.com",
    "openrouter": "https://openrouter.ai/api",
}


async def chat_completion(
    config: RuntimeLlmConfig,
    *,
    system: str,
    messages: list[dict],
    json_mode: bool = False,
    max_tokens: int = 1024,
) -> str:
    if not config.configured:
        raise ValueError("JPbot LLM is not configured")

    provider = config.provider
    if provider not in VALID_PROVIDERS:
        raise ValueError(f"Unsupported provider '{provider}'")

    if provider in OPENAI_COMPAT_BASE_URLS:
        return await _openai_compatible(
            config,
            base_url=OPENAI_COMPAT_BASE_URLS[provider],
            system=system,
            messages=messages,
            json_mode=json_mode,
            max_tokens=max_tokens,
        )
    if provider == "anthropic":
        return await _anthropic(
            config,
            system=system,
            messages=messages,
            json_mode=json_mode,
            max_tokens=max_tokens,
        )
    if provider == "gemini":
        return await _gemini(
            config,
            system=system,
            messages=messages,
            json_mode=json_mode,
            max_tokens=max_tokens,
        )
    raise ValueError(f"Unsupported provider '{provider}'")


async def _openai_compatible(
    config: RuntimeLlmConfig,
    *,
    base_url: str,
    system: str,
    messages: list[dict],
    json_mode: bool,
    max_tokens: int,
) -> str:
    payload: dict = {
        "model": config.model,
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": max_tokens,
        "temperature": 0.35,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    if config.provider == "openrouter":
        headers["HTTP-Referer"] = "https://nexxus-tech.com"
        headers["X-Title"] = "Nexxus Tech JPbot"

    async with httpx.AsyncClient(timeout=45) as client:
        resp = await client.post(
            f"{base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def _anthropic(
    config: RuntimeLlmConfig,
    *,
    system: str,
    messages: list[dict],
    json_mode: bool,
    max_tokens: int,
) -> str:
    system_prompt = system
    if json_mode:
        system_prompt = f"{system}\n\nRespond with valid JSON only."

    anthropic_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m.get("role") in ("user", "assistant")
    ]

    payload = {
        "model": config.model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": anthropic_messages,
        "temperature": 0.35,
    }

    async with httpx.AsyncClient(timeout=45) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        parts = data.get("content") or []
        return "".join(part.get("text", "") for part in parts if part.get("type") == "text")


async def _gemini(
    config: RuntimeLlmConfig,
    *,
    system: str,
    messages: list[dict],
    json_mode: bool,
    max_tokens: int,
) -> str:
    contents: list[dict] = []
    for message in messages:
        role = message.get("role")
        if role not in ("user", "assistant"):
            continue
        contents.append(
            {
                "role": "user" if role == "user" else "model",
                "parts": [{"text": str(message.get("content", ""))}],
            }
        )

    payload: dict = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.35,
            "maxOutputTokens": max_tokens,
        },
    }
    if json_mode:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    model = config.model
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )

    async with httpx.AsyncClient(timeout=45) as client:
        resp = await client.post(
            url,
            headers={
                "x-goog-api-key": config.api_key,
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get("candidates") or []
        if not candidates:
            raise ValueError("Gemini returned no candidates")
        parts = candidates[0].get("content", {}).get("parts") or []
        return "".join(part.get("text", "") for part in parts)


def default_model_for_provider(provider: str) -> str:
    return PROVIDER_DEFAULT_MODELS.get(provider, "")
