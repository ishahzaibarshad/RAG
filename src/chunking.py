from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any

from .loaders import Document


@dataclass
class Chunk:
    chunk_id: str
    text: str
    meta: Dict[str, Any]


def chunk_text(text: str, size: int, overlap: int) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []

    if overlap >= size:
        overlap = max(0, size // 4)

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
        start = max(0, end - overlap)

    return chunks


def chunk_documents(docs: List[Document], size: int, overlap: int) -> List[Chunk]:
    out: List[Chunk] = []
    for d in docs:
        parts = chunk_text(d.text, size=size, overlap=overlap)
        for idx, part in enumerate(parts):
            out.append(
                Chunk(
                    chunk_id=f"{d.doc_id}::chunk={idx}",
                    text=part,
                    meta={
                        **(d.meta or {}),
                        "doc_id": d.doc_id,
                        "source": d.source,
                        "chunk_index": idx,
                        "chunk_id": f"{d.doc_id}::chunk={idx}",
                    },
                )
            )
    return out
