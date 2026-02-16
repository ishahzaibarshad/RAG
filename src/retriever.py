from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any

from .vector_store import NumpyVectorStore, VectorRecord
from .embeddings import Embedder
from .config import settings


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
        k = top_k or settings.rag_top_k
        qvec = self.embedder.embed_query(question)
        hits = self.store.cosine_search(qvec, top_k=k)
        return [
            RetrievedChunk(score=s, chunk_id=r.chunk_id, text=r.text, meta=r.meta)
            for s, r in hits
        ]
