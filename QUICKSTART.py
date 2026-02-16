#!/usr/bin/env python3
"""
QUICKSTART.md - RAG System in 60 Seconds

This is the fastest way to get your RAG system running.
"""

QUICKSTART = """
╔════════════════════════════════════════════════════════════════════════════╗
║                   RAG SYSTEM - QUICKSTART (60 SECONDS)                      ║
╚════════════════════════════════════════════════════════════════════════════╝

📥 STEP 1: Install Dependencies (30 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  $ pip install -r requirements.txt

🔑 STEP 2: Add API Key (10 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Get FREE API key: https://platform.openai.com/api-keys
  2. Edit .env file:
     OPENAI_API_KEY=sk-your-key-here

▶️ STEP 3: Run RAG (20 seconds to ingest + start interactive chat)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  $ python ingest_and_run.py
  
  Then type your questions:
    You: What is artificial intelligence?
    Assistant: AI is... [answer with sources]

💬 Questions to Try
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ "What is artificial intelligence?"
  ✓ "Explain machine learning"
  ✓ "What causes climate change?"
  ✓ "How does blockchain work?"
  ✓ "What are the future trends in AI?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ FEATURES INCLUDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Complete RAG pipeline (11 modules)
  ✅ 3 sample documents (27.8 KB) with diverse topics
  ✅ Multiple interfaces:
     • Interactive CLI chat
     • REST API endpoint
     • Python library
     • Batch processing
  ✅ Full documentation & examples
  ✅ Setup verification script

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️ OTHER USAGE MODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # API Server (uses port 8000)
  $ python ingest_and_run.py api
  
  # Single query
  $ python ingest_and_run.py query "What is AI?"
  
  # Programmatic example
  $ python example.py
  
  # Batch queries
  $ python batch_query.py
  
  # Verify setup
  $ python verify_setup.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ADD YOUR OWN DOCUMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Add .txt or .pdf files to: data/raw/
  2. Run: python ingest_and_run.py
  3. Ask questions about your documents!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 FULL DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • README.md     - Complete usage guide
  • SETUP.md      - Detailed setup & troubleshooting
  • COMPLETED.md  - What was added & how it works
  • example.py    - Code examples
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready? Let's go! 🚀

  $ pip install -r requirements.txt
  $ # Edit .env with your API key
  $ python ingest_and_run.py
"""

if __name__ == "__main__":
    print(QUICKSTART)
