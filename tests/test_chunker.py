from itertools import pairwise
from pathlib import Path

import pytest

from telecom_ai.rag.chunker import chunk_document


def _write(tmp_path: Path, rel_path: str, content: str) -> Path:
    path = tmp_path / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_tiny_doc_single_chunk(tmp_path: Path) -> None:
    path = _write(tmp_path, "sample.md", "Hello world.\nThis is a tiny doc.")

    chunks = chunk_document(path, tmp_path)

    assert len(chunks) == 1
    chunk = chunks[0]
    assert chunk.id == "sample.md#0"
    assert chunk.source == "sample.md"
    assert chunk.index == 0
    assert chunk.headings == []
    assert chunk.text == "Hello world.\nThis is a tiny doc."


def test_no_headings_doc(tmp_path: Path) -> None:
    content = "\n".join(f"paragraph {i}" for i in range(5))
    path = _write(tmp_path, "flat.md", content)

    chunks = chunk_document(path, tmp_path, max_tokens=3, overlap_tokens=0)

    assert len(chunks) > 1
    assert all(chunk.headings == [] for chunk in chunks)


def test_heading_hierarchy_tracked(tmp_path: Path) -> None:
    content = "\n".join(
        [
            "# Title",
            "",
            "Intro text here.",
            "",
            "## Section A",
            "",
            "Content A here.",
            "",
            "### Sub A1",
            "",
            "Detail A1 text.",
            "",
            "## Section B",
            "",
            "Content B here.",
        ]
    )
    path = _write(tmp_path, "doc.md", content)

    chunks = chunk_document(path, tmp_path, max_tokens=5, overlap_tokens=0)

    def headings_for(needle: str) -> list[str]:
        for chunk in chunks:
            if needle in chunk.text:
                return chunk.headings
        raise AssertionError(f"{needle!r} not found in any chunk")

    assert headings_for("Intro text") == ["Title"]
    assert headings_for("Content A here") == ["Title", "Section A"]
    assert headings_for("Detail A1 text") == ["Title", "Section A", "Sub A1"]
    # Section B is a sibling of Section A -> Sub A1 must be popped off the stack.
    assert headings_for("Content B here") == ["Title", "Section B"]


def test_deterministic_ids_and_overlap(tmp_path: Path) -> None:
    lines = [f"line{i}" for i in range(10)]
    path = _write(tmp_path, "seq.md", "\n".join(lines))

    chunks = chunk_document(path, tmp_path, max_tokens=2, overlap_tokens=1)

    assert len(chunks) == 9
    for i, chunk in enumerate(chunks):
        assert chunk.id == f"seq.md#{i}"
        assert chunk.index == i
        assert chunk.text == f"line{i}\nline{i + 1}"
    # Consecutive chunks overlap by the configured token budget.
    for prev, nxt in pairwise(chunks):
        assert prev.text.splitlines()[-1] == nxt.text.splitlines()[0]


def test_oversized_single_line_does_not_crash(tmp_path: Path) -> None:
    heading = "# " + " ".join(f"word{i}" for i in range(50))
    content = heading + "\n\nShort body text.\n\n## Next\n\nMore body text."
    path = _write(tmp_path, "long-heading.md", content)

    chunks = chunk_document(path, tmp_path, max_tokens=10, overlap_tokens=2)

    assert len(chunks) >= 2
    assert chunks[0].text.startswith("# word0 word1")
    # The oversized heading line alone forms the first chunk rather than crashing.
    assert chunks[0].headings[0].startswith("word0")


def test_empty_document_yields_no_chunks(tmp_path: Path) -> None:
    path = _write(tmp_path, "empty.md", "   \n\n  \n")

    assert chunk_document(path, tmp_path) == []


def test_invalid_token_budgets_raise(tmp_path: Path) -> None:
    path = _write(tmp_path, "doc.md", "content")

    with pytest.raises(ValueError):
        chunk_document(path, tmp_path, max_tokens=0)

    with pytest.raises(ValueError):
        chunk_document(path, tmp_path, max_tokens=10, overlap_tokens=10)

    with pytest.raises(ValueError):
        chunk_document(path, tmp_path, max_tokens=10, overlap_tokens=-1)
