#!/usr/bin/env python3
"""
Verification script to check if the RAG project is properly set up.
"""

import os
import sys
from pathlib import Path

def check_file(path: str, description: str) -> bool:
    """Check if a file exists."""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def check_directory(path: str, description: str) -> bool:
    """Check if a directory exists."""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def verify_setup():
    """Verify all project components are in place."""
    
    print("\n" + "=" * 70)
    print("RAG PROJECT VERIFICATION")
    print("=" * 70)
    
    all_ok = True
    
    # Check Python environment
    print("\n[1] Python Environment")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.8+)")
        all_ok = False
    
    # Check directories
    print("\n[2] Directory Structure")
    all_ok &= check_directory("src", "   src/ directory")
    all_ok &= check_directory("data", "   data/ directory")
    all_ok &= check_directory("data/raw", "   data/raw/ directory")
    all_ok &= check_directory("data/index", "   data/index/ directory")
    
    # Check source files
    print("\n[3] Core Modules")
    src_files = [
        ("src/__init__.py", "   __init__.py"),
        ("src/config.py", "   config.py"),
        ("src/loaders.py", "   loaders.py"),
        ("src/chunking.py", "   chunking.py"),
        ("src/embeddings.py", "   embeddings.py"),
        ("src/vector_store.py", "   vector_store.py"),
        ("src/retriever.py", "   retriever.py"),
        ("src/rag.py", "   rag.py"),
        ("src/api.py", "   api.py"),
        ("src/chat_cli.py", "   chat_cli.py"),
        ("src/ingest.py", "   ingest.py"),
    ]
    for path, desc in src_files:
        all_ok &= check_file(path, desc)
    
    # Check configuration files
    print("\n[4] Configuration Files")
    all_ok &= check_file(".env", "   .env (exists)")
    all_ok &= check_file(".env.example", "   .env.example (template)")
    all_ok &= check_file("requirements.txt", "   requirements.txt")
    
    # Check documentation
    print("\n[5] Documentation")
    all_ok &= check_file("README.md", "   README.md")
    all_ok &= check_file("SETUP.md", "   SETUP.md")
    
    # Check utility scripts
    print("\n[6] Utility Scripts")
    all_ok &= check_file("ingest_and_run.py", "   ingest_and_run.py")
    all_ok &= check_file("example.py", "   example.py")
    all_ok &= check_file("batch_query.py", "   batch_query.py")
    
    # Check sample data
    print("\n[7] Sample Data")
    data_files = [
        ("data/raw/sample_ai.txt", "   sample_ai.txt"),
        ("data/raw/sample_climate.txt", "   sample_climate.txt"),
        ("data/raw/sample_blockchain.txt", "   sample_blockchain.txt"),
    ]
    for path, desc in data_files:
        all_ok &= check_file(path, desc)
    
    # Check .env configuration
    print("\n[8] Environment Configuration")
    try:
        from dotenv import load_dotenv
        load_dotenv(".env")
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        
        if api_key and api_key != "your_key_here" and api_key.startswith("sk-"):
            print("✅ OPENAI_API_KEY is set")
        else:
            print("❌ OPENAI_API_KEY not configured (required)")
            print("   → Copy .env.example to .env")
            print("   → Add your API key from https://platform.openai.com/api-keys")
            all_ok = False
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        all_ok = False
    
    # Check dependencies
    print("\n[9] Python Dependencies")
    dependencies = {
        "openai": "OpenAI API client",
        "dotenv": "Environment variables",
        "numpy": "NumPy arrays",
        "fastapi": "FastAPI web framework",
        "uvicorn": "ASGI server",
        "pydantic": "Data validation",
        "pypdf": "PDF reading",
        "tqdm": "Progress bar",
    }
    
    missing_deps = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module:15} - {description}")
        except ImportError:
            print(f"❌ {module:15} - {description}")
            missing_deps.append(module)
            all_ok = False
    
    # Check index
    print("\n[10] Vector Index")
    index_vec = "data/index/main_vectors.npy"
    index_meta = "data/index/main_meta.json"
    
    if os.path.exists(index_vec) and os.path.exists(index_meta):
        try:
            import numpy as np
            vec_size = os.path.getsize(index_vec) / (1024 * 1024)  # MB
            print(f"✅ Index exists ({vec_size:.1f} MB)")
        except Exception as e:
            print(f"⚠️  Index exists but error reading: {e}")
    else:
        print(f"⚠️  Index not created yet")
        print(f"   → Run: python ingest_and_run.py")
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok and not missing_deps:
        print("✅ PROJECT READY!")
        print("\nNext steps:")
        print("  1. python ingest_and_run.py    # Ingest data and start CLI")
        print("  2. Type your questions")
        print("  3. Get answers with sources")
    else:
        print("❌ MISSING COMPONENTS")
        if missing_deps:
            print(f"\nInstall missing dependencies:")
            print(f"  pip install {' '.join(missing_deps)}")
        print("\nOr install all at once:")
        print("  pip install -r requirements.txt")
    
    print("=" * 70 + "\n")
    
    return all_ok and not missing_deps

if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)
