from __future__ import annotations

import json
import re

import httpx

from models.blog import BlogAssistResponse
from services.blog_assistant_settings_store import get_runtime_config
from services.blog_store import BLOG_CATEGORIES, COVER_COLORS, estimate_read_time, slugify
from services.blog_markdown_sanitize import sanitize_blog_markdown
from services.llm_service import chat_completion

BLOG_ASSIST_SYSTEM_PROMPT = """You are a blog editor assistant for Nexxus Tech (cloud, security, AI consulting).
The user provides a draft article (plain text or markdown). Extract metadata and return polished markdown content.

METADATA RULES:
- category MUST be exactly one of: {categories}
- cover_color MUST be exactly one of: {cover_colors}
- slug: lowercase, hyphenated, no special characters, derived from title
- excerpt: 1-2 compelling sentences, max 220 characters, no markdown
- tags: 2-6 short topic tags relevant to the article
- read_time: integer minutes (estimate from content length, ~200 words/minute)

CONTENT RULES:
- content: clean markdown starting with # Title (match the title field), preserve the author's meaning
- Use clear section structure: ## for major sections, ### for subsections, blank lines between blocks
- Lists: use - for bullets; keep items concise
- The page hero already shows the title — include # Title once at the top only, never repeat it as a second H1

RENDERER CONSTRAINTS (critical — our blog uses a custom line-based markdown parser):
Before returning content, scan the draft for these issues and FIX them in your output:

1. Python triple-quoted strings (triple double-quotes)
   - NEVER use them in ```python blocks — they break older parsers and confuse readers
   - Replace with single-quoted multiline strings ('''...''') or parenthesized strings with \\n

2. Nested fenced code blocks
   - NEVER put ```bash (or any ```lang) inside another ``` fence
   - For terminal/session transcripts, use ONE ```text block and show commands as plain lines, e.g.:
     $ find /var -name "*.log" -mtime -1
   - Do not wrap inner commands in their own fences

3. Fence formatting
   - Opening and closing fences must be on their own line (only ``` or ```lang on that line)
   - Always tag code blocks with a language: python, bash, json, text, yaml, etc.
   - Leave a blank line before and after every fenced block

4. Prose vs code separation
   - Do not embed raw ``` markers inside paragraph text — use inline `backticks` for short snippets
   - Long commands, scripts, config, or transcripts belong in fenced blocks, not inline

5. Structure and readability
   - Break walls of text into short paragraphs (3-5 sentences max)
   - Add ## headings every few sections so the article is scannable
   - Keep list items parallel and concise

SELF-CHECK before outputting JSON:
- Every ``` opening fence has a matching closing ``` on its own line
- No triple double-quotes inside python code blocks
- No nested ``` fences
- No duplicate H1 title after the opening line

OUTPUT: ONLY valid JSON (no markdown fences):
{{
  "title": "string",
  "slug": "string",
  "excerpt": "string",
  "category": "string",
  "tags": ["tag1", "tag2"],
  "read_time": 5,
  "cover_color": "#007BA7",
  "content": "# Title\\n\\n..."
}}"""


def _build_system_prompt() -> str:
    return BLOG_ASSIST_SYSTEM_PROMPT.format(
        categories=", ".join(BLOG_CATEGORIES),
        cover_colors=", ".join(COVER_COLORS),
    )


def _parse_json_response(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Assistant returned invalid JSON")
    return data


def _pick_category(value: str) -> str:
    cleaned = value.strip()
    for category in BLOG_CATEGORIES:
        if category.lower() == cleaned.lower():
            return category
    for category in BLOG_CATEGORIES:
        if cleaned.lower() in category.lower() or category.lower() in cleaned.lower():
            return category
    return BLOG_CATEGORIES[0]


def _pick_cover_color(value: str) -> str:
    cleaned = value.strip().upper()
    for color in COVER_COLORS:
        if color.upper() == cleaned:
            return color
    return COVER_COLORS[0]


def _normalize_tags(tags: object) -> list[str]:
    if not isinstance(tags, list):
        return []
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
    return cleaned[:8]


def _build_response(data: dict, draft: str) -> BlogAssistResponse:
    title = str(data.get("title") or "").strip()
    if not title:
        raise ValueError("Assistant did not return a title")

    slug = slugify(str(data.get("slug") or title))
    if not slug:
        slug = slugify(title)

    content = str(data.get("content") or draft).strip()
    if content and not content.startswith("#"):
        content = f"# {title}\n\n{content}"

    content = sanitize_blog_markdown(content, title=title)

    read_time_raw = data.get("read_time")
    try:
        read_time = int(read_time_raw)
        read_time = max(1, min(120, read_time))
    except (TypeError, ValueError):
        read_time = estimate_read_time(content)

    excerpt = str(data.get("excerpt") or "").strip()
    if len(excerpt) > 500:
        excerpt = excerpt[:497] + "…"

    return BlogAssistResponse(
        title=title,
        slug=slug,
        excerpt=excerpt,
        category=_pick_category(str(data.get("category") or "")),
        tags=_normalize_tags(data.get("tags")),
        read_time=read_time,
        cover_color=_pick_cover_color(str(data.get("cover_color") or "")),
        content=content,
    )


async def generate_blog_metadata(draft: str) -> BlogAssistResponse:
    config = await get_runtime_config()
    if not config.configured:
        raise ValueError("Blog assistant is not configured. Ask an admin to set it up in Settings.")

    trimmed = draft.strip()
    if len(trimmed) < 50:
        raise ValueError("Please paste at least 50 characters of draft content.")

    try:
        raw = await chat_completion(
            config,
            system=_build_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Polish this draft for the Nexxus Tech blog. "
                        "Fix any markdown rendering issues (nested fences, Python triple-quoted strings, "
                        "missing language tags, walls of text) before returning JSON.\n\n"
                        f"{trimmed[:50000]}"
                    ),
                }
            ],
            json_mode=True,
            max_tokens=4096,
        )
        data = _parse_json_response(raw)
        return _build_response(data, trimmed)
    except httpx.HTTPError as exc:
        raise ValueError(f"AI service error: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError("Assistant returned invalid JSON. Try again.") from exc
