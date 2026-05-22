"""BM25 index over corpus chunks, serialised alongside ChromaDB."""

from __future__ import annotations

from pathlib import Path

from telecom_ai.rag.chunker import Chunk

DEFAULT_INDEX_PATH = Path(".chroma") / "bm25_index.pkl"


class BM25Index:
    """Build and query a rank-bm25 index over a list of Chunk objects."""

    def __init__(self) -> None:
        raise NotImplementedError("Implemented in task 5")

    @classmethod
    def build(cls, chunks: list[Chunk]) -> BM25Index:
        """Construct index from chunks using a simple whitespace+punctuation tokeniser."""
        raise NotImplementedError("Implemented in task 5")

    def query(self, text: str, k: int = 5) -> list[tuple[str, float]]:
        """Return (chunk_id, score) pairs for the top-k BM25 results."""
        raise NotImplementedError("Implemented in task 5")

    def save(self, path: Path = DEFAULT_INDEX_PATH) -> None:
        raise NotImplementedError("Implemented in task 5")

    @classmethod
    def load(cls, path: Path = DEFAULT_INDEX_PATH) -> BM25Index:
        raise NotImplementedError("Implemented in task 5")
