import re

_TAG_RE = re.compile(r"<[^>]+>")


def sanitize_text(value: str) -> str:
    """Strip HTML tags and normalize whitespace for user-provided text fields."""
    if not value:
        return ""
    cleaned = _TAG_RE.sub("", value)
    return cleaned.strip()
