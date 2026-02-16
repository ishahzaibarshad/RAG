#!/usr/bin/env python3
"""
Example script showing how to use the RAG system programmatically.
"""

from src.config import settings
from src.vector_store import NumpyVectorStore
from src.embeddings import Embedder
from src.retriever import Retriever
from src.rag import RAGEngine

def example_usage():
    """Example: Query the RAG system programmatically"""
    
    print("=" * 70)
    print("RAG SYSTEM EXAMPLE")
    print("=" * 70)
    
    # Load the vector store (index must exist from running ingest)
    try:
        print("\n[1] Loading vector store...")
        store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
        print(f"    ✅ Loaded {len(store.records)} chunks")
    except FileNotFoundError as e:
        print(f"    ❌ Error: {e}")
        print("    Run: python ingest_and_run.py")
        return
    
    # Initialize embedder
    print("\n[2] Initializing embedder...")
    try:
        embedder = Embedder()
        print("    ✅ OpenAI embedder ready")
    except RuntimeError as e:
        print(f"    ❌ Error: {e}")
        print("    Add OPENAI_API_KEY to .env")
        return
    
    # Create retriever
    print("\n[3] Creating retriever...")
    retriever = Retriever(store, embedder)
    print("    ✅ Retriever ready")
    
    # Create RAG engine
    print("\n[4] Creating RAG engine...")
    rag = RAGEngine(retriever)
    print("    ✅ RAG engine ready")
    
    # Example queries
    queries = [
        "What is artificial intelligence?",
        "How does climate change affect ecosystems?",
        "What are the key features of blockchain technology?"
    ]
    
    print("\n" + "=" * 70)
    print("EXAMPLE QUERIES")
    print("=" * 70)
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 70)
        
        try:
            result = rag.answer(query)
            
            print(f"\n🤖 Answer:")
            print(result.answer)
            
            print(f"\n📚 Sources ({len(result.sources)}):")
            for src in result.sources:
                print(f"   • {src['source']} (score: {src['score']:.3f})")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    example_usage()
