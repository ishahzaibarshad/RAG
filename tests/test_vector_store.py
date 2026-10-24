import numpy as np
import pytest

from src.vector_store import NumpyVectorStore, VectorRecord


def record(name):
    return VectorRecord(chunk_id=name, text=name, meta={"filename": f"{name}.txt"})


def test_cosine_search_ranks_nearest_record_and_limits_results():
    store = NumpyVectorStore(np.array([[1, 0], [0, 1], [-1, 0]], dtype=np.float32), [record("x"), record("y"), record("z")])
    hits = store.cosine_search(np.array([0.9, 0.1], dtype=np.float32), top_k=2)
    assert [hit[1].chunk_id for hit in hits] == ["x", "y"]
    assert hits[0][0] > hits[1][0]


def test_empty_index_returns_no_hits():
    store = NumpyVectorStore(np.empty((0, 2), dtype=np.float32), [])
    assert store.cosine_search(np.array([1, 0], dtype=np.float32)) == []


@pytest.mark.parametrize("query", [np.array([1], dtype=np.float32), np.array([0, 0], dtype=np.float32), np.array([np.nan, 1], dtype=np.float32)])
def test_search_rejects_invalid_query_vectors(query):
    store = NumpyVectorStore(np.array([[1, 0]], dtype=np.float32), [record("x")])
    with pytest.raises(ValueError):
        store.cosine_search(query)


def test_store_round_trip_and_rejects_unsafe_index_name(tmp_path):
    store = NumpyVectorStore(np.array([[1, 2]], dtype=np.float32), [record("x")])
    store.save(str(tmp_path), "sample")
    loaded = NumpyVectorStore.load(str(tmp_path), "sample")
    assert loaded.records[0].chunk_id == "x"
    assert np.array_equal(loaded.vectors, store.vectors)
    with pytest.raises(ValueError, match="simple file-name"):
        store.save(str(tmp_path), "../outside")

