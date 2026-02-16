from __future__ import annotations
import os
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import numpy as np


@dataclass
class VectorRecord:
    chunk_id: str
    text: str
    meta: Dict[str, Any]


class NumpyVectorStore:
    """
    Minimal vector store:
    - vectors: numpy float32 array (N, D)
    - records: list of VectorRecord aligned with vectors rows
    """

    def __init__(self, vectors: np.ndarray, records: List[VectorRecord]) -> None:
        if len(vectors) != len(records):
            raise ValueError("vectors and records length mismatch")
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        self.vectors = vectors
        self.records = records

        # Precompute norms for cosine similarity
        self._norms = np.linalg.norm(self.vectors, axis=1) + 1e-12

    @staticmethod
    def _paths(index_dir: str, index_name: str) -> Tuple[str, str]:
        vec_path = os.path.join(index_dir, f"{index_name}_vectors.npy")
        meta_path = os.path.join(index_dir, f"{index_name}_meta.json")
        return vec_path, meta_path

    def save(self, index_dir: str, index_name: str) -> None:
        os.makedirs(index_dir, exist_ok=True)
        vec_path, meta_path = self._paths(index_dir, index_name)
        np.save(vec_path, self.vectors)

        payload = [
            {"chunk_id": r.chunk_id, "text": r.text, "meta": r.meta}
            for r in self.records
        ]
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, index_dir: str, index_name: str) -> "NumpyVectorStore":
        vec_path, meta_path = cls._paths(index_dir, index_name)
        if not os.path.exists(vec_path) or not os.path.exists(meta_path):
            raise FileNotFoundError(
                f"Index not found. Expected {vec_path} and {meta_path}. Run ingest first."
            )

        vectors = np.load(vec_path).astype(np.float32)
        with open(meta_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        records = [
            VectorRecord(chunk_id=item["chunk_id"], text=item["text"], meta=item.get("meta", {}))
            for item in payload
        ]
        return cls(vectors=vectors, records=records)

    def cosine_search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Tuple[float, VectorRecord]]:
        """
        Returns list of (score, record) sorted desc. Score is cosine similarity.
        """
        if query_vec.dtype != np.float32:
            query_vec = query_vec.astype(np.float32)

        qn = (np.linalg.norm(query_vec) + 1e-12)
        sims = (self.vectors @ query_vec) / (self._norms * qn)

        if top_k >= len(sims):
            idxs = np.argsort(-sims)
        else:
            idxs = np.argpartition(-sims, top_k)[:top_k]
            idxs = idxs[np.argsort(-sims[idxs])]

        results: List[Tuple[float, VectorRecord]] = []
        for i in idxs:
            results.append((float(sims[i]), self.records[int(i)]))
        return results
