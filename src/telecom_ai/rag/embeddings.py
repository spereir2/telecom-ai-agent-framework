"""Batched sentence-transformers embedding wrapper (MiniLM by default)."""

from __future__ import annotations

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class Embedder:
    """Thin wrapper around a SentenceTransformer model with batched encode."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        raise NotImplementedError("Implemented in task 4")

    def encode(self, texts: list[str], batch_size: int = 64) -> list[list[float]]:
        """Return a list of embedding vectors, one per input text."""
        raise NotImplementedError("Implemented in task 4")
