"""Hybrid retriever combining BM25 + dense embeddings via Reciprocal Rank Fusion."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from telecom_ai.rag.bm25_index import BM25Index
from telecom_ai.rag.embeddings import Embedder
from telecom_ai.rag.store import Store


class RetrieverMode(StrEnum):
    bm25 = "bm25"
    dense = "dense"
    hybrid = "hybrid"


@dataclass
class RetrievedChunk:
    id: str
    text: str
    score: float
    source: str
    headings: list[str] = field(default_factory=list)


class HybridRetriever:
    """Retrieve chunks using BM25, dense, or hybrid (RRF) mode."""

    def __init__(
        self,
        store: Store,
        bm25: BM25Index,
        embedder: Embedder,
        rrf_k: int = 60,
    ) -> None:
        raise NotImplementedError("Implemented in task 6")

    def retrieve(
        self,
        query: str,
        k: int = 5,
        mode: RetrieverMode = RetrieverMode.hybrid,
    ) -> list[RetrievedChunk]:
        """Return the top-k chunks ranked by the selected mode."""
        raise NotImplementedError("Implemented in task 6")

    @classmethod
    def from_disk(
        cls,
        chroma_path: Path,
        bm25_path: Path,
        model_name: str | None = None,
    ) -> HybridRetriever:
        """Convenience constructor that loads persisted indices from disk."""
        raise NotImplementedError("Implemented in task 6")
