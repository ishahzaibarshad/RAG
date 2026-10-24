from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .loaders import Document


@dataclass
class Chunk:
    chunk_id: str
    text: str
    meta: Dict[str, Any]


def chunk_text(text: str, size: int, overlap: int) -> List[str]:
    if size < 1:
        raise ValueError("size must be at least 1")
    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must be between 0 and size - 1")

    text = (text or "").strip()
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(n, start + size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = end - overlap

    return chunks


def chunk_documents(docs: List[Document], size: int, overlap: int) -> List[Chunk]:
    out: List[Chunk] = []
    for doc in docs:
        parts = chunk_text(doc.text, size=size, overlap=overlap)
        for idx, part in enumerate(parts):
            chunk_id = f"{doc.doc_id}::chunk={idx}"
            out.append(
                Chunk(
                    chunk_id=chunk_id,
                    text=part,
                    meta={
                        **(doc.meta or {}),
                        "doc_id": doc.doc_id,
                        "source": doc.source,
                        "chunk_index": idx,
                        "chunk_id": chunk_id,
                    },
                )
            )
    return out

