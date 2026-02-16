#!/usr/bin/env python3
"""
Batch query example - demonstrating how to run multiple queries from a file.
"""

import json
from pathlib import Path
from src.config import settings
from src.vector_store import NumpyVectorStore
from src.embeddings import Embedder
from src.retriever import Retriever
from src.rag import RAGEngine


def batch_query(queries_file: str, output_file: str = "results.json"):
    """
    Run batch queries from a JSON file.
    
    Input file format:
    {
      "queries": [
        "What is AI?",
        "How does blockchain work?"
      ]
    }
    
    Output format:
    {
      "results": [
        {
          "query": "What is AI?",
          "answer": "...",
          "sources": [...]
        }
      ]
    }
    """
    
    # Load queries
    with open(queries_file, 'r') as f:
        data = json.load(f)
    queries = data.get("queries", [])
    
    if not queries:
        print("No queries found in file")
        return
    
    # Load RAG system
    store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
    embedder = Embedder()
    retriever = Retriever(store, embedder)
    rag = RAGEngine(retriever)
    
    # Process queries
    results = []
    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Processing: {query[:60]}...")
        
        result = rag.answer(query)
        results.append({
            "query": query,
            "answer": result.answer,
            "sources": [
                {
                    "chunk_id": s["chunk_id"],
                    "source": s["source"],
                    "score": s["score"],
                    "page": s.get("page")
                }
                for s in result.sources
            ]
        })
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump({"results": results}, f, indent=2)
    
    print(f"\n✅ Results saved to {output_file}")


if __name__ == "__main__":
    # Example: Create sample queries file
    sample_queries = {
        "queries": [
            "What is artificial intelligence?",
            "Explain the concept of machine learning",
            "What are the main causes of climate change?",
            "How does blockchain ensure security?",
            "What is the difference between supervised and unsupervised learning?"
        ]
    }
    
    # Save sample queries
    with open("sample_queries.json", "w") as f:
        json.dump(sample_queries, f, indent=2)
    
    print("📄 Created sample_queries.json")
    print("\nRunning batch query...")
    
    try:
        batch_query("sample_queries.json", "batch_results.json")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nFirst, run: python ingest_and_run.py")
