"""Sanitize blog markdown so it renders cleanly with the line-based frontend parser."""

from __future__ import annotations

import re

_FENCE_LINE = re.compile(r"^```([\w-]*)\s*$")
_PYTHON_TRIPLE_DOUBLE = re.compile(r'"""(.*?)"""', re.DOTALL)


def sanitize_blog_markdown(content: str, title: str | None = None) -> str:
    """Fix common markdown patterns that break or degrade blog rendering."""
    if not content:
        return content

    text = content.replace("\r\n", "\n").strip()
    text = _strip_duplicate_title_h1(text, title)
    text = _flatten_nested_fences(text)
    text = _fix_python_blocks(text)
    text = _ensure_fence_spacing(text)
    return text


def _strip_duplicate_title_h1(content: str, title: str | None) -> str:
    if not title:
        return content

    lines = content.split("\n")
    normalized_title = title.strip().lower()
    kept: list[str] = []
    skipped_first = False

    for line in lines:
        if not skipped_first and line.startswith("# ") and not line.startswith("## "):
            heading = line[2:].strip()
            if heading.lower() == normalized_title:
                skipped_first = True
                continue
        kept.append(line)

    return "\n".join(kept).strip()


def _flatten_nested_fences(content: str) -> str:
    """Remove inner ``` fences inside unlabeled or text blocks (session transcripts)."""
    lines = content.split("\n")
    output: list[str] = []
    index = 0

    while index < len(lines):
        match = _FENCE_LINE.match(lines[index])
        if not match:
            output.append(lines[index])
            index += 1
            continue

        lang = match.group(1) or ""
        block_lines, next_index = _read_fenced_block(lines, index)
        index = next_index

        if lang in ("", "text"):
            block_lines = _strip_inner_fence_markers(block_lines)
            lang = "text"

        output.append(f"```{lang}")
        output.extend(block_lines)
        output.append("```")

    return "\n".join(output)


def _read_fenced_block(lines: list[str], start: int) -> tuple[list[str], int]:
    open_match = _FENCE_LINE.match(lines[start])
    if not open_match:
        return [], start + 1

    collected: list[str] = []
    depth = 1
    index = start + 1

    while index < len(lines) and depth > 0:
        nested = _FENCE_LINE.match(lines[index])
        if nested:
            if nested.group(1):
                depth += 1
                collected.append(lines[index])
            else:
                depth -= 1
                if depth > 0:
                    collected.append(lines[index])
            index += 1
            continue
        if depth > 0:
            collected.append(lines[index])
        index += 1

    return collected, index


def _strip_inner_fence_markers(block_lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    inside_inner = False

    for line in block_lines:
        match = _FENCE_LINE.match(line)
        if match:
            if match.group(1):
                inside_inner = True
                continue
            inside_inner = False
            continue
        cleaned.append(line)

    return cleaned


def _fix_python_blocks(content: str) -> str:
    lines = content.split("\n")
    output: list[str] = []
    index = 0

    while index < len(lines):
        match = _FENCE_LINE.match(lines[index])
        if not match or match.group(1) != "python":
            output.append(lines[index])
            index += 1
            continue

        block_lines, next_index = _read_fenced_block(lines, index)
        index = next_index
        fixed = _convert_python_triple_double("\n".join(block_lines))
        output.append("```python")
        output.extend(fixed.split("\n"))
        output.append("```")

    return "\n".join(output)


def _convert_python_triple_double(code: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        inner = match.group(1)
        if "'''" in inner:
            escaped = inner.replace("\\", "\\\\").replace('"', '\\"')
            return f'("{escaped}")'
        return f"'''{inner}'''"

    return _PYTHON_TRIPLE_DOUBLE.sub(replacer, code)


def _ensure_fence_spacing(content: str) -> str:
    lines = content.split("\n")
    spaced: list[str] = []

    for index, line in enumerate(lines):
        is_fence = bool(_FENCE_LINE.match(line))
        prev = spaced[-1] if spaced else ""
        if is_fence and prev.strip() and not _FENCE_LINE.match(prev):
            spaced.append("")
        spaced.append(line)
        if is_fence and index + 1 < len(lines):
            nxt = lines[index + 1]
            if nxt.strip() and not _FENCE_LINE.match(nxt):
                spaced.append("")

    return re.sub(r"\n{3,}", "\n\n", "\n".join(spaced)).strip()
