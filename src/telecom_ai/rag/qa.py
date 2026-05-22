"""QA chain: assemble prompt with retrieved chunks and emit a cited answer."""

from __future__ import annotations

from pydantic import BaseModel

from telecom_ai.rag.retriever import HybridRetriever, RetrieverMode


class Answer(BaseModel):
    text: str
    citations: list[str]  # chunk ids that support the answer


def answer_with_citations(
    question: str,
    retriever: HybridRetriever,
    k: int = 5,
    mode: RetrieverMode = RetrieverMode.hybrid,
) -> Answer:
    """Retrieve relevant chunks, call the LLM, validate citations, return Answer."""
    raise NotImplementedError("Implemented in task 7")
