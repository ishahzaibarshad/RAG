from __future__ import annotations
from .config import settings
from .vector_store import NumpyVectorStore
from .embeddings import Embedder
from .retriever import Retriever
from .rag import RAGEngine


def main() -> None:
    store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
    embedder = Embedder()
    retriever = Retriever(store, embedder)
    rag = RAGEngine(retriever)

    print("RAG CLI. Type 'exit' to quit.")
    while True:
        q = input("\nYou: ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break

        result = rag.answer(q)
        print("\nAssistant:\n", result.answer)
        print("\nSources:")
        for s in result.sources:
            print(f" - score={s['score']:.3f} chunk={s['chunk_id']} source={s.get('source')} page={s.get('page')}")


if __name__ == "__main__":
    main()
