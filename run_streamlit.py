#!/usr/bin/env python3
"""
Run Streamlit UI for RAG System
"""

import subprocess
import sys
import os

def main():
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit not installed!")
        print("Run: pip install streamlit")
        print("Or: pip install -r requirements.txt")
        sys.exit(1)
    
    print("🚀 Starting Streamlit RAG UI...")
    print("📍 Local URL: http://localhost:8501")
    print("🌐 Network URL: http://your-ip:8501")
    print("\n💡 Press CTRL+C to stop\n")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        os.path.join(os.path.dirname(__file__), "streamlit_app.py"),
        "--logger.level=info"
    ])

if __name__ == "__main__":
    main()
