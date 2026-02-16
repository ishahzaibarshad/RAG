from __future__ import annotations
from typing import List
import numpy as np
from openai import OpenAI

from .config import settings


class Embedder:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment/.env")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embed_model

    def embed_texts(self, texts: List[str], batch_size: int = 64) -> np.ndarray:
        """
        Returns: (N, D) float32 numpy array
        """
        vectors: List[List[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = self.client.embeddings.create(model=self.model, input=batch)
            # keep the response order
            batch_vecs = [item.embedding for item in resp.data]
            vectors.extend(batch_vecs)

        arr = np.array(vectors, dtype=np.float32)
        return arr

    def embed_query(self, text: str) -> np.ndarray:
        resp = self.client.embeddings.create(model=self.model, input=[text])
        vec = np.array(resp.data[0].embedding, dtype=np.float32)
        return vec
