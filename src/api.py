from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel

from .config import settings
from .vector_store import NumpyVectorStore
from .embeddings import Embedder
from .retriever import Retriever
from .rag import RAGEngine

app = FastAPI(title="RAG From Scratch")

# Load once at startup
store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
embedder = Embedder()
retriever = Retriever(store, embedder)
rag = RAGEngine(retriever)


class QueryRequest(BaseModel):
    question: str
    top_k: int | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    res = rag.answer(req.question, top_k=req.top_k)
    return {"answer": res.answer, "sources": res.sources}
