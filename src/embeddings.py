from __future__ import annotations

from typing import List

import numpy as np
from openai import OpenAI

from .config import settings


class Embedder:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment/.env")
        self.client = OpenAI(api_key=settings.openai_api_key, timeout=30.0, max_retries=2)
        self.model = settings.embed_model

    def embed_texts(self, texts: List[str], batch_size: int = 64) -> np.ndarray:
        """Return one float32 embedding per input text in input order."""
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if not texts:
            return np.empty((0, 0), dtype=np.float32)
        if any(not text.strip() for text in texts):
            raise ValueError("texts must not contain empty strings")

        vectors = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            response = self.client.embeddings.create(model=self.model, input=batch)
            if len(response.data) != len(batch):
                raise RuntimeError("Embedding service returned an unexpected number of vectors")
            vectors.extend(item.embedding for item in response.data)

        array = np.asarray(vectors, dtype=np.float32)
        if array.ndim != 2 or not np.isfinite(array).all():
            raise RuntimeError("Embedding service returned invalid vectors")
        return array

    def embed_query(self, text: str) -> np.ndarray:
        if not text.strip():
            raise ValueError("query text must not be empty")
        response = self.client.embeddings.create(model=self.model, input=[text])
        if len(response.data) != 1:
            raise RuntimeError("Embedding service returned an unexpected number of vectors")
        vector = np.asarray(response.data[0].embedding, dtype=np.float32)
        if vector.ndim != 1 or not np.isfinite(vector).all():
            raise RuntimeError("Embedding service returned an invalid query vector")
        return vector

