from __future__ import annotations

import re
from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status

from dependencies.auth import require_admin, require_blog_admin
from models.blog import BlogAssistRequest, BlogAssistResponse, BlogPost, BlogPostWrite
from models.chat_settings import ChatSettingsResponse, ChatSettingsWrite, ModelOption, ProviderModelsResponse, ProviderOption
from models.chat_settings import PROVIDER_DEFAULT_MODELS, VALID_PROVIDERS
from services.blog_assistant import generate_blog_metadata
from services import blog_assistant_settings_store
from services.blog_store import (
    estimate_read_time,
    find_post_index,
    load_posts_raw,
    next_post_id,
    save_posts_raw,
    slugify,
    validate_unique_slug,
)
from services.llm_models import get_models_for_provider

router = APIRouter(prefix="/admin/blog", tags=["blog-admin"])

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


async def _assistant_settings_response(view: dict) -> ChatSettingsResponse:
    provider = str(view.get("provider") or "openai")
    model = str(view.get("model") or "")
    model_options = await get_models_for_provider(provider, current_model=model)
    return ChatSettingsResponse(
        **view,
        providers=_provider_options(),
        models=[ModelOption(id=item.id, label=item.label) for item in model_options],
    )


def _normalize_tags(tags: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        value = str(tag).strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(value)
    return cleaned


def _build_excerpt(excerpt: str, content: str, title: str) -> str:
    cleaned = excerpt.strip()
    if cleaned:
        return cleaned
    plain = re.sub(r"[#*`\[\]()]", "", content)
    snippet = " ".join(plain.split())[:220]
    if len(snippet) >= 220:
        snippet = snippet.rsplit(" ", 1)[0] + "…"
    return snippet or title.strip()


def _prepare_post_payload(data: BlogPostWrite, *, post_id: str | None = None) -> dict[str, Any]:
    title = data.title.strip()
    slug = slugify(data.slug or title)
    if not slug:
        raise ValueError("Could not derive a valid slug")

    content = data.content.strip()
    if content and not content.startswith("#"):
        content = f"# {title}\n\n{content}"

    post_date = data.date.strip() or date.today().isoformat()
    read_time = data.read_time if data.read_time is not None else estimate_read_time(content)

    return {
        "id": post_id or "",
        "slug": slug,
        "title": title,
        "excerpt": _build_excerpt(data.excerpt, content, title),
        "content": content,
        "category": data.category.strip(),
        "tags": _normalize_tags(data.tags),
        "author": data.author.strip(),
        "author_role": data.author_role.strip(),
        "date": post_date,
        "read_time": read_time,
        "featured": bool(data.featured),
        "cover_color": data.cover_color.strip() or "#007BA7",
    }


@router.get("/assistant/settings", response_model=ChatSettingsResponse)
async def get_blog_assistant_settings(_: dict = Depends(require_admin)) -> ChatSettingsResponse:
    view = await blog_assistant_settings_store.get_admin_settings_view()
    return await _assistant_settings_response(view)


@router.put("/assistant/settings", response_model=ChatSettingsResponse)
async def update_blog_assistant_settings(
    payload: ChatSettingsWrite,
    admin: dict = Depends(require_admin),
) -> ChatSettingsResponse:
    provider = payload.provider.strip().lower()
    if provider not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported provider '{provider}'",
        )
    api_key = payload.apiKey.strip() or None
    try:
        view = await blog_assistant_settings_store.save_admin_settings(
            provider=provider,
            model=payload.model.strip(),
            enabled=payload.enabled,
            api_key=api_key,
            updated_by=admin["username"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return await _assistant_settings_response(view)


@router.get("/assistant/models/{provider}", response_model=ProviderModelsResponse)
async def list_blog_assistant_models(
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


@router.post("/assist", response_model=BlogAssistResponse)
async def assist_blog_post(
    payload: BlogAssistRequest,
    _: dict = Depends(require_blog_admin),
) -> BlogAssistResponse:
    try:
        return await generate_blog_metadata(payload.draft)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[BlogPost])
async def list_admin_posts(_: dict = Depends(require_blog_admin)) -> list[BlogPost]:
    posts = await load_posts_raw()
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return [BlogPost(**p) for p in posts]


@router.get("/{post_id}", response_model=BlogPost)
async def get_admin_post(post_id: str, _: dict = Depends(require_blog_admin)) -> BlogPost:
    posts = await load_posts_raw()
    index = find_post_index(posts, post_id)
    if index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return BlogPost(**posts[index])


@router.post("", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
async def create_admin_post(
    payload: BlogPostWrite,
    _: dict = Depends(require_blog_admin),
) -> BlogPost:
    posts = await load_posts_raw()
    try:
        doc = _prepare_post_payload(payload)
        validate_unique_slug(posts, doc["slug"])
        doc["id"] = next_post_id(posts)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    posts.insert(0, doc)
    await save_posts_raw(posts)
    return BlogPost(**doc)


@router.put("/{post_id}", response_model=BlogPost)
async def update_admin_post(
    post_id: str,
    payload: BlogPostWrite,
    _: dict = Depends(require_blog_admin),
) -> BlogPost:
    posts = await load_posts_raw()
    index = find_post_index(posts, post_id)
    if index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    try:
        doc = _prepare_post_payload(payload, post_id=post_id)
        validate_unique_slug(posts, doc["slug"], exclude_id=post_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    posts[index] = doc
    await save_posts_raw(posts)
    return BlogPost(**doc)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_admin_post(post_id: str, _: dict = Depends(require_blog_admin)) -> Response:
    posts = await load_posts_raw()
    index = find_post_index(posts, post_id)
    if index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    posts.pop(index)
    await save_posts_raw(posts)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
