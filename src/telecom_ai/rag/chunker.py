"""Markdown-aware token-counted chunker with heading metadata and deterministic IDs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


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
    raise NotImplementedError("Implemented in task 3")
