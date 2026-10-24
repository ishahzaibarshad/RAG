# RAG from Scratch

A small retrieval-augmented generation implementation built from focused Python modules rather than a high-level RAG framework. It loads TXT and PDF documents, chunks their text, embeds chunks with the OpenAI embeddings API, stores vectors in a NumPy-backed index, retrieves the closest chunks, and uses an OpenAI chat model to generate an answer with source information.

## Interfaces

- Streamlit interface
- Interactive CLI
- FastAPI query endpoint
- Python library API

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `OPENAI_API_KEY` locally. Then run an interface:

```bash
python run_streamlit.py
python ingest_and_run.py
python ingest_and_run.py api
```

The first run ingests documents from `data/raw/` and creates the local vector index. Supported inputs described by the implementation are `.txt` and `.pdf` files.

## Implementation

- Chunking and overlap are configurable
- Embeddings and generation use OpenAI APIs
- Vector storage and cosine-similarity retrieval use NumPy
- Answers include the retrieved source chunks and similarity scores
- The FastAPI, CLI, and Streamlit interfaces share the retrieval pipeline

## Notes

This repository is a prototype/learning project. Remove the current “production-ready” and unverified speed claims unless they are backed by measured evaluation. The repository does not appear to include a license file, so omit the MIT license claim until a `LICENSE` file is added.

