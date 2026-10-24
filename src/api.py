from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import settings
from .embeddings import Embedder
from .rag import RAGEngine
from .retriever import Retriever
from .vector_store import NumpyVectorStore


@asynccontextmanager
async def lifespan(_app: FastAPI):
    store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
    embedder = Embedder()
    _app.state.rag = RAGEngine(Retriever(store, embedder))
    yield


app = FastAPI(title="RAG From Scratch", lifespan=lifespan)


class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=20)

    @field_validator("question")
    @classmethod
    def reject_blank_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question must contain non-whitespace text")
        return value.strip()


class SourceReference(BaseModel):
    chunk_id: str
    score: float
    source: str | None = None
    page: int | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference]


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = app.state.rag.answer(req.question, top_k=req.top_k)
    return {"answer": result.answer, "sources": result.sources}

