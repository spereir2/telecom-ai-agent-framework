"""Markdown-aware token-counted chunker with heading metadata and deterministic IDs."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

# A source line paired with the heading stack (top-down) active at that point.
_Line = tuple[str, list[str]]


@dataclass
class Chunk:
    id: str  # "<rel_path>#<index>"
    text: str
    source: str  # relative path from corpus root
    headings: list[str] = field(default_factory=list)
    index: int = 0


def chunk_document(
    path: Path,
    corpus_root: Path,
    max_tokens: int = 512,
    overlap_tokens: int = 64,
) -> list[Chunk]:
    """Split a markdown file into overlapping token-bounded chunks.

    Chunk ids are deterministic: ``<rel_path>#<index>``.
    Heading hierarchy at the split point is preserved in ``headings``.
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if not 0 <= overlap_tokens < max_tokens:
        raise ValueError("overlap_tokens must be non-negative and less than max_tokens")

    source = path.resolve().relative_to(corpus_root.resolve()).as_posix()
    lines = _lines_with_headings(path.read_text(encoding="utf-8"))

    chunks: list[Chunk] = []
    buffer: list[_Line] = []
    buffer_tokens = 0

    for line, headings in lines:
        tokens = _token_count(line)
        if buffer and buffer_tokens + tokens > max_tokens:
            _append_chunk(chunks, buffer, source)
            buffer, buffer_tokens = _overlap_tail(buffer, overlap_tokens)
        buffer.append((line, headings))
        buffer_tokens += tokens

    _append_chunk(chunks, buffer, source)
    return chunks


def _lines_with_headings(text: str) -> list[_Line]:
    """Pair each line with the heading stack (top-down) active at that point.

    A heading line updates the stack (popping same-or-deeper levels) before
    being paired, so it is reported as part of its own section.
    """
    stack: list[tuple[int, str]] = []
    result: list[_Line] = []
    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        result.append((line, [title for _, title in stack]))
    return result


def _token_count(line: str) -> int:
    """Approximate token count via whitespace splitting."""
    return len(line.split())


def _overlap_tail(buffer: list[_Line], overlap_tokens: int) -> tuple[list[_Line], int]:
    """Return the trailing lines of ``buffer`` whose token count fits within overlap_tokens."""
    tail: list[_Line] = []
    count = 0
    for line, headings in reversed(buffer):
        tokens = _token_count(line)
        if count + tokens > overlap_tokens:
            break
        tail.insert(0, (line, headings))
        count += tokens
    return tail, count


def _append_chunk(chunks: list[Chunk], buffer: list[_Line], source: str) -> None:
    text = "\n".join(line for line, _ in buffer).strip("\n")
    if not text.strip():
        return
    chunks.append(
        Chunk(
            id=f"{source}#{len(chunks)}",
            text=text,
            source=source,
            headings=buffer[0][1] if buffer else [],
            index=len(chunks),
        )
    )
