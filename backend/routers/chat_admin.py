from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.auth import require_admin
from models.chat_settings import (
    PROVIDER_DEFAULT_MODELS,
    ChatSettingsResponse,
    ChatSettingsTestResponse,
    ChatSettingsWrite,
    ModelOption,
    ProviderModelsResponse,
    ProviderOption,
    VALID_PROVIDERS,
)
from services.chat_settings_store import get_admin_settings_view, get_runtime_config, save_admin_settings
from services.llm_models import get_models_for_provider
from services.llm_service import chat_completion

router = APIRouter(prefix="/admin/chat", tags=["chat-admin"])

PROVIDER_LABELS = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "gemini": "Google Gemini",
    "deepseek": "DeepSeek",
    "openrouter": "OpenRouter",
}


def _provider_options() -> list[ProviderOption]:
    return [
        ProviderOption(
            id=provider,
            label=PROVIDER_LABELS.get(provider, provider.title()),
            defaultModel=PROVIDER_DEFAULT_MODELS[provider],
        )
        for provider in sorted(VALID_PROVIDERS)
    ]


async def _settings_response(view: dict) -> ChatSettingsResponse:
    provider = str(view.get("provider") or "deepseek")
    model = str(view.get("model") or "")
    model_options = await get_models_for_provider(provider, current_model=model)
    return ChatSettingsResponse(
        **view,
        providers=_provider_options(),
        models=[ModelOption(id=item.id, label=item.label) for item in model_options],
    )


@router.get("/settings", response_model=ChatSettingsResponse)
async def get_chat_settings(_: dict = Depends(require_admin)) -> ChatSettingsResponse:
    view = await get_admin_settings_view()
    return await _settings_response(view)


@router.get("/models/{provider}", response_model=ProviderModelsResponse)
async def list_provider_models(
    provider: str,
    current: str = "",
    _: dict = Depends(require_admin),
) -> ProviderModelsResponse:
    cleaned = provider.strip().lower()
    if cleaned not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported provider '{provider}'",
        )
    model_options = await get_models_for_provider(cleaned, current_model=current)
    return ProviderModelsResponse(
        provider=cleaned,
        defaultModel=PROVIDER_DEFAULT_MODELS[cleaned],
        models=[ModelOption(id=item.id, label=item.label) for item in model_options],
    )


@router.put("/settings", response_model=ChatSettingsResponse)
async def update_chat_settings(
    payload: ChatSettingsWrite,
    admin: dict = Depends(require_admin),
) -> ChatSettingsResponse:
    provider = payload.provider.strip().lower()
    if provider not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported provider '{payload.provider}'",
        )

    api_key = payload.apiKey.strip() or None
    try:
        view = await save_admin_settings(
            provider=provider,
            model=payload.model.strip(),
            enabled=payload.enabled,
            api_key=api_key,
            updated_by=admin["username"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return await _settings_response(view)


@router.post("/settings/test", response_model=ChatSettingsTestResponse)
async def test_chat_settings(
    payload: ChatSettingsWrite,
    admin: dict = Depends(require_admin),
) -> ChatSettingsTestResponse:
    provider = payload.provider.strip().lower()
    if provider not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported provider '{payload.provider}'",
        )

    api_key = payload.apiKey.strip()
    if not api_key:
        runtime = await get_runtime_config()
        api_key = runtime.api_key

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API key is required to test the connection",
        )

    from services.llm_settings_store import RuntimeLlmConfig

    config = RuntimeLlmConfig(
        provider=provider,
        model=payload.model.strip() or PROVIDER_DEFAULT_MODELS.get(provider, ""),
        api_key=api_key,
        enabled=True,
    )

    try:
        reply = await chat_completion(
            config,
            system="You are a connectivity test assistant.",
            messages=[{"role": "user", "content": "Reply with exactly: OK"}],
            max_tokens=16,
        )
    except httpx.HTTPError as exc:
        detail = str(exc)
        if hasattr(exc, "response") and exc.response is not None:
            detail = exc.response.text[:300] or detail
        return ChatSettingsTestResponse(
            success=False,
            message=f"Connection failed: {detail}",
        )
    except Exception as exc:
        return ChatSettingsTestResponse(success=False, message=str(exc))

    preview = reply.strip()[:120]
    return ChatSettingsTestResponse(
        success=True,
        message="Connection successful.",
        replyPreview=preview,
    )
