"""CLI entry points: kb-ingest, kb-ask, kb-show."""

from __future__ import annotations

import typer

app = typer.Typer(name="kb", add_completion=False)


@app.command("ingest")
def _ingest_cmd(
    corpus: str = typer.Option("corpus", help="Path to corpus root directory"),
    chroma: str = typer.Option(".chroma", help="ChromaDB persist directory"),
) -> None:
    """Rebuild the knowledge-base index from corpus/."""
    raise NotImplementedError("Implemented in task 8")


@app.command("ask")
def _ask_cmd(
    question: str = typer.Argument(..., help="Question to answer"),
    k: int = typer.Option(5, help="Number of chunks to retrieve"),
    mode: str = typer.Option("hybrid", help="Retriever mode: bm25 | dense | hybrid"),
    chroma: str = typer.Option(".chroma", help="ChromaDB persist directory"),
) -> None:
    """Answer a question with inline citations."""
    raise NotImplementedError("Implemented in task 8")


@app.command("show")
def _show_cmd(
    chunk_id: str = typer.Argument(..., help="Chunk id (e.g. corpus/tmf/tmf641.md#3)"),
    chroma: str = typer.Option(".chroma", help="ChromaDB persist directory"),
) -> None:
    """Print a stored chunk's text and metadata."""
    raise NotImplementedError("Implemented in task 8")


# Zero-arg callables referenced by pyproject.toml [project.scripts].
def ingest() -> None:
    app(["ingest"], standalone_mode=True)


def ask() -> None:
    app(["ask"], standalone_mode=True)


def show() -> None:
    app(["show"], standalone_mode=True)
