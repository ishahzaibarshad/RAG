from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np


@dataclass
class VectorRecord:
    chunk_id: str
    text: str
    meta: Dict[str, Any]


class NumpyVectorStore:
    """Minimal local vector index with row-aligned metadata records."""

    def __init__(self, vectors: np.ndarray, records: List[VectorRecord]) -> None:
        vectors = np.asarray(vectors, dtype=np.float32)
        if vectors.ndim != 2:
            raise ValueError("vectors must be a two-dimensional array")
        if len(vectors) != len(records):
            raise ValueError("vectors and records length mismatch")
        if vectors.shape[1] == 0:
            raise ValueError("vectors must have at least one dimension")
        if not np.isfinite(vectors).all():
            raise ValueError("vectors must contain only finite values")
        self.vectors = vectors
        self.records = records
        self._norms = np.linalg.norm(self.vectors, axis=1) + 1e-12

    @staticmethod
    def _paths(index_dir: str, index_name: str) -> Tuple[str, str]:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", index_name):
            raise ValueError("index_name must be a simple file-name component")
        return (
            os.path.join(index_dir, f"{index_name}_vectors.npy"),
            os.path.join(index_dir, f"{index_name}_meta.json"),
        )

    def save(self, index_dir: str, index_name: str) -> None:
        os.makedirs(index_dir, exist_ok=True)
        vec_path, meta_path = self._paths(index_dir, index_name)
        payload = [
            {"chunk_id": record.chunk_id, "text": record.text, "meta": record.meta}
            for record in self.records
        ]
        np.save(vec_path, self.vectors, allow_pickle=False)
        with open(meta_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, index_dir: str, index_name: str) -> "NumpyVectorStore":
        vec_path, meta_path = cls._paths(index_dir, index_name)
        if not os.path.exists(vec_path) or not os.path.exists(meta_path):
            raise FileNotFoundError(
                f"Index not found. Expected {vec_path} and {meta_path}. Run ingest first."
            )
        vectors = np.load(vec_path, allow_pickle=False)
        with open(meta_path, "r", encoding="utf-8") as file:
            payload = json.load(file)
        records = [
            VectorRecord(chunk_id=item["chunk_id"], text=item["text"], meta=item.get("meta", {}))
            for item in payload
        ]
        return cls(vectors=vectors, records=records)

    def cosine_search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Tuple[float, VectorRecord]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        query_vec = np.asarray(query_vec, dtype=np.float32)
        if query_vec.ndim != 1 or query_vec.shape[0] != self.vectors.shape[1]:
            raise ValueError("query vector dimension must match indexed vectors")
        if not np.isfinite(query_vec).all():
            raise ValueError("query vector must contain only finite values")
        query_norm = float(np.linalg.norm(query_vec))
        if query_norm == 0:
            raise ValueError("query vector must not be zero")
        if not self.records:
            return []

        similarities = (self.vectors @ query_vec) / (self._norms * query_norm)
        count = min(top_k, len(similarities))
        indexes = np.argpartition(-similarities, count - 1)[:count]
        indexes = indexes[np.argsort(-similarities[indexes])]
        return [(float(similarities[i]), self.records[int(i)]) for i in indexes]

