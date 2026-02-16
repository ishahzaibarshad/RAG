from __future__ import annotations
import os
from tqdm import tqdm

from .config import settings
from .loaders import load_documents_from_dir
from .chunking import chunk_documents
from .embeddings import Embedder
from .vector_store import NumpyVectorStore, VectorRecord


def main() -> None:
    raw_dir = settings.raw_data_dir
    index_dir = settings.index_dir
    index_name = settings.index_name

    print(f"Loading documents from: {raw_dir}")
    docs = load_documents_from_dir(raw_dir)
    print(f"Loaded {len(docs)} document units (PDF pages count as units).")

    print("Chunking...")
    chunks = chunk_documents(docs, size=settings.chunk_size_chars, overlap=settings.chunk_overlap_chars)
    print(f"Created {len(chunks)} chunks.")

    if not chunks:
        print("No chunks produced. Add documents to data/raw and try again.")
        return

    embedder = Embedder()
    texts = [c.text for c in chunks]

    print("Embedding chunks...")
    vectors = embedder.embed_texts(texts, batch_size=64)

    records = [
        VectorRecord(chunk_id=c.chunk_id, text=c.text, meta=c.meta)
        for c in chunks
    ]

    store = NumpyVectorStore(vectors=vectors, records=records)
    store.save(index_dir=index_dir, index_name=index_name)

    print(f"Saved index to {os.path.join(index_dir, index_name)}_*")


if __name__ == "__main__":
    main()
