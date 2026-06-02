#!/usr/bin/env python3
"""Create a new blog post entry in backend/data/blog_posts.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_FILE = ROOT / "backend" / "data" / "blog_posts.json"
TEMPLATE_FILE = ROOT / "backend" / "data" / "blog_post.template.json"

CATEGORIES = [
    "WAF & Security",
    "Zero-Trust",
    "AI & Automation",
    "Cloud Security",
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


def load_posts() -> list[dict]:
    with open(POSTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts: list[dict]) -> None:
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
        f.write("\n")


def next_id(posts: list[dict]) -> str:
    ids = [int(p["id"]) for p in posts if str(p.get("id", "")).isdigit()]
    return str(max(ids, default=0) + 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a new Nexxus Tech blog post")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--slug", help="URL slug (auto from title if omitted)")
    parser.add_argument("--category", default="WAF & Security", choices=CATEGORIES)
    parser.add_argument("--content-file", help="Markdown file for article body")
    parser.add_argument("--excerpt", help="Listing excerpt (auto from content if omitted)")
    parser.add_argument("--featured", action="store_true")
    parser.add_argument("--cover-color", default="#007BA7", choices=COVER_COLORS)
    parser.add_argument("--tags", help="Comma-separated tags")
    args = parser.parse_args()

    slug = args.slug or slugify(args.title)
    if not slug:
        print("Error: could not derive slug from title", file=sys.stderr)
        return 1

    posts = load_posts()
    if any(p.get("slug") == slug for p in posts):
        print(f"Error: slug already exists: {slug}", file=sys.stderr)
        return 1

    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        post = json.load(f)

    if args.content_file:
        content_path = Path(args.content_file)
        if not content_path.is_file():
            print(f"Error: content file not found: {content_path}", file=sys.stderr)
            return 1
        content = content_path.read_text(encoding="utf-8").strip()
    else:
        content = post["content"].replace("Your Article Title", args.title)

    if not content.startswith("#"):
        content = f"# {args.title}\n\n{content}"

    excerpt = args.excerpt
    if not excerpt:
        plain = re.sub(r"[#*`\[\]()]", "", content)
        excerpt = " ".join(plain.split())[:220].rsplit(" ", 1)[0] + "…"

    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()] or post["tags"]

    post.update(
        {
            "id": next_id(posts),
            "slug": slug,
            "title": args.title,
            "excerpt": excerpt,
            "content": content,
            "category": args.category,
            "tags": tags,
            "date": date.today().isoformat(),
            "read_time": estimate_read_time(content),
            "featured": args.featured,
            "cover_color": args.cover_color,
        }
    )

    posts.insert(0, post)
    save_posts(posts)

    print("Added blog post:")
    print(f"  id:       {post['id']}")
    print(f"  slug:     {post['slug']}")
    print(f"  url:      /blog/{post['slug']}")
    print(f"  category: {post['category']}")
    print(f"  read:     {post['read_time']} min")
    print(f"\nEdit: {POSTS_FILE}")
    print("Deploy: docker compose restart backend")
    return 0


if __name__ == "__main__":
    sys.exit(main())
