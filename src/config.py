
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(".env")


def _get_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        return default
    try:
        return int(v)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    embed_model: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

    rag_top_k: int = _get_int("RAG_TOP_K", 5)
    rag_max_context_chars: int = _get_int("RAG_MAX_CONTEXT_CHARS", 12000)

    chunk_size_chars: int = _get_int("CHUNK_SIZE_CHARS", 1800)
    chunk_overlap_chars: int = _get_int("CHUNK_OVERLAP_CHARS", 250)

    raw_data_dir: str = os.getenv("RAW_DATA_DIR", "./data/raw")
    index_dir: str = os.getenv("INDEX_DIR", "./data/index")
    index_name: str = os.getenv("INDEX_NAME", "main")


settings = Settings()
