from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
from openai import OpenAI

from .config import settings
from .retriever import Retriever, RetrievedChunk


SYSTEM_PROMPT = """You are a helpful assistant.
You must answer using ONLY the provided context.
If the answer is not in the context, say: "I don't know based on the provided documents."
Cite sources as [source:... page:... chunk_id:...] when possible.
Keep the answer clear and concise.
"""


def _format_context(chunks: List[RetrievedChunk], max_chars: int) -> str:
    parts: List[str] = []
    total = 0
    for c in chunks:
        source = c.meta.get("filename") or c.meta.get("source") or c.meta.get("path") or "unknown"
        page = c.meta.get("page")
        header = f"[chunk_id={c.chunk_id} | source={source}" + (f" | page={page}]" if page else "]")
        block = f"{header}\n{c.text}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)
    return "\n".join(parts)


@dataclass
class RAGResult:
    answer: str
    sources: List[Dict[str, Any]]


class RAGEngine:
    def __init__(self, retriever: Retriever) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment/.env")
        self.retriever = retriever
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.chat_model

    def answer(self, question: str, top_k: int | None = None) -> RAGResult:
        chunks = self.retriever.retrieve(question, top_k=top_k)
        context = _format_context(chunks, max_chars=settings.rag_max_context_chars)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"QUESTION:\n{question}\n\nCONTEXT:\n{context}",
            },
        ]

        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            max_tokens=400,
            messages=messages,
        )
        answer = (resp.choices[0].message.content or "").strip()

        sources = []
        for c in chunks:
            sources.append(
                {
                    "chunk_id": c.chunk_id,
                    "score": c.score,
                    "source": c.meta.get("filename") or c.meta.get("path") or c.meta.get("source"),
                    "page": c.meta.get("page"),
                }
            )

        return RAGResult(answer=answer, sources=sources)
