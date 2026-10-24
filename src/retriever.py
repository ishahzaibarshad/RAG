from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .config import settings
from .embeddings import Embedder
from .vector_store import NumpyVectorStore


@dataclass
class RetrievedChunk:
    score: float
    chunk_id: str
    text: str
    meta: Dict[str, Any]


class Retriever:
    def __init__(self, store: NumpyVectorStore, embedder: Embedder) -> None:
        self.store = store
        self.embedder = embedder

    def retrieve(self, question: str, top_k: int | None = None) -> List[RetrievedChunk]:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")
        k = settings.rag_top_k if top_k is None else top_k
        if k < 1:
            raise ValueError("top_k must be at least 1")
        qvec = self.embedder.embed_query(question)
        hits = self.store.cosine_search(qvec, top_k=k)
        return [
            RetrievedChunk(score=score, chunk_id=record.chunk_id, text=record.text, meta=record.meta)
            for score, record in hits
        ]

