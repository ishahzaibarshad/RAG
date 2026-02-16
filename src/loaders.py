from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Iterable, List, Dict, Any

from pypdf import PdfReader


@dataclass
class Document:
    doc_id: str
    source: str
    text: str
    meta: Dict[str, Any]


def load_txt(path: str) -> Document:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        txt = f.read()
    name = os.path.basename(path)
    return Document(
        doc_id=name,
        source=path,
        text=txt,
        meta={"type": "txt", "path": path, "filename": name},
    )


def load_pdf(path: str) -> List[Document]:
    reader = PdfReader(path)
    name = os.path.basename(path)
    docs: List[Document] = []

    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        docs.append(
            Document(
                doc_id=f"{name}#page={i+1}",
                source=path,
                text=page_text,
                meta={
                    "type": "pdf",
                    "path": path,
                    "filename": name,
                    "page": i + 1,
                    "num_pages": len(reader.pages),
                },
            )
        )
    return docs


def load_documents_from_dir(raw_dir: str) -> List[Document]:
    out: List[Document] = []
    for root, _, files in os.walk(raw_dir):
        for fn in files:
            p = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext == ".txt":
                out.append(load_txt(p))
            elif ext == ".pdf":
                out.extend(load_pdf(p))
            else:
                # ignore unknown formats in MVP
                continue
    return out
