from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

import aiofiles

from models.blog import BlogPost

DATA_FILE = Path(__file__).parent.parent / "data" / "blog_posts.json"

BLOG_CATEGORIES = [
    "WAF & Security",
    "Zero-Trust",
    "AI & Automation",
    "Cloud Security",
    "Security",
]

COVER_COLORS = ["#007BA7", "#00A8E0", "#005F7F", "#38383D", "#4DB8E0"]


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def estimate_read_time(content: str) -> int:
    words = len(re.findall(r"\w+", content))
    return max(1, round(words / 200))


async def load_posts_raw() -> list[dict[str, Any]]:
    async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = await f.read()
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("blog_posts.json must contain a JSON array")
    return data


async def save_posts_raw(posts: list[dict[str, Any]]) -> None:
    async with aiofiles.open(DATA_FILE, "w", encoding="utf-8") as f:
        await f.write(json.dumps(posts, indent=2, ensure_ascii=False))
        await f.write("\n")


async def load_posts() -> list[BlogPost]:
    return [BlogPost(**p) for p in await load_posts_raw()]


def next_post_id(posts: list[dict[str, Any]]) -> str:
    ids = [int(p["id"]) for p in posts if str(p.get("id", "")).isdigit()]
    return str(max(ids, default=0) + 1)


def find_post_index(posts: list[dict[str, Any]], post_id: str) -> int:
    for index, post in enumerate(posts):
        if str(post.get("id")) == str(post_id):
            return index
    return -1


def validate_unique_slug(posts: list[dict[str, Any]], slug: str, *, exclude_id: str | None = None) -> None:
    cleaned = slug.strip().lower()
    for post in posts:
        if exclude_id is not None and str(post.get("id")) == str(exclude_id):
            continue
        if str(post.get("slug", "")).strip().lower() == cleaned:
            raise ValueError(f"Slug already exists: {slug}")
