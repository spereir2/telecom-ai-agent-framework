"""ChromaDB persistent collection wrapper."""

from __future__ import annotations

from pathlib import Path

from telecom_ai.rag.chunker import Chunk

DEFAULT_CHROMA_PATH = Path(".chroma")
COLLECTION_NAME = "telecom_kb"


class Store:
    """Manages a persistent ChromaDB collection for telecom knowledge base chunks."""

    def __init__(self, persist_path: Path = DEFAULT_CHROMA_PATH) -> None:
        raise NotImplementedError("Implemented in task 4")

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Upsert chunks with their pre-computed embeddings."""
        raise NotImplementedError("Implemented in task 4")

    def query_dense(self, embedding: list[float], k: int = 5) -> list[tuple[str, float]]:
        """Return (chunk_id, distance) pairs for the k nearest neighbours."""
        raise NotImplementedError("Implemented in task 4")

    def get(self, chunk_id: str) -> Chunk | None:
        """Retrieve a single chunk by its deterministic id."""
        raise NotImplementedError("Implemented in task 4")
