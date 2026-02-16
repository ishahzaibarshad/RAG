#!/usr/bin/env python3
"""
Ingest data and launch the RAG CLI.
Usage:
    python ingest_and_run.py       # Ingest and start CLI chat
    python ingest_and_run.py api   # Ingest and start API server
    python ingest_and_run.py ui    # Ingest and start Streamlit UI
    python ingest_and_run.py query "your question here"  # Ingest and ask a question
"""

import sys
import os
import subprocess

def main():
    # First, run the ingest pipeline
    print("=" * 60)
    print("INGESTING DATA...")
    print("=" * 60)
    
    result = subprocess.run([sys.executable, "-m", "src.ingest"], cwd=os.path.dirname(__file__) or ".")
    
    if result.returncode != 0:
        print("\n❌ Ingestion failed. Make sure you have:")
        print("   1. Added OPENAI_API_KEY to .env (use .env.example as template)")
        print("   2. Sample data in data/raw/ (already added)")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Ingestion complete! Starting RAG...")
    print("=" * 60 + "\n")
    
    # Now handle different modes
    if len(sys.argv) > 1:
        if sys.argv[1] == "api":
            print("Starting FastAPI server on http://localhost:8000")
            print("API endpoint: POST /query")
            print("Example: curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{\"question\": \"what is AI?\"}'")
            subprocess.run([sys.executable, "-m", "uvicorn", "src.api:app", "--reload"])
        elif sys.argv[1] == "ui":
            print("Starting Streamlit UI on http://localhost:8501")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
        elif sys.argv[1] == "query":
            if len(sys.argv) < 3:
                print("Usage: python ingest_and_run.py query 'your question'")
                sys.exit(1)
            question = " ".join(sys.argv[2:])
            # Run a single query
            from src.config import settings
            from src.vector_store import NumpyVectorStore
            from src.embeddings import Embedder
            from src.retriever import Retriever
            from src.rag import RAGEngine
            
            store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
            embedder = Embedder()
            retriever = Retriever(store, embedder)
            rag = RAGEngine(retriever)
            
            result = rag.answer(question)
            print("\n" + "=" * 60)
            print(f"🤖 Question: {question}\n")
            print(f"📝 Answer:\n{result.answer}\n")
            print("📚 Sources:")
            for s in result.sources:
                print(f"   - {s['source']} (chunk: {s['chunk_id']}, score: {s['score']:.3f})")
            print("=" * 60)
        else:
            print(f"Unknown command: {sys.argv[1]}")
            sys.exit(1)
    else:
        # Default: CLI mode
        subprocess.run([sys.executable, "-m", "src.chat_cli"])

if __name__ == "__main__":
    main()
