#!/usr/bin/env python3
"""
Streamlit UI for RAG System
A user-friendly web interface for querying documents with RAG
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime
import json

# Import RAG components
from src.config import settings
from src.vector_store import NumpyVectorStore
from src.embeddings import Embedder
from src.retriever import Retriever
from src.rag import RAGEngine
from src.loaders import load_documents_from_dir
from src.chunking import chunk_documents
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Configure page
st.set_page_config(
    page_title="RAG Query System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .response-box {
        background-color: #f0f2f6;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .source-box {
        background-color: #e8f4f8;
        border-left: 4px solid #00b4d8;
        padding: 12px;
        border-radius: 5px;
        margin: 8px 0;
    }
    .stats-box {
        background-color: #f8f9ff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None
if "embedder" not in st.session_state:
    st.session_state.embedder = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "system_ready" not in st.session_state:
    st.session_state.system_ready = False


@st.cache_resource
def load_rag_system():
    """Load RAG system components with caching"""
    try:
        # Check if index exists
        index_dir = settings.index_dir
        index_name = settings.index_name
        vec_path = os.path.join(index_dir, f"{index_name}_vectors.npy")
        meta_path = os.path.join(index_dir, f"{index_name}_meta.json")
        
        if not os.path.exists(vec_path) or not os.path.exists(meta_path):
            return None, None, "Index not found"
        
        # Load components
        store = NumpyVectorStore.load(index_dir, index_name)
        embedder = Embedder()
        retriever = Retriever(store, embedder)
        rag = RAGEngine(retriever)
        
        return rag, embedder, "System initialized successfully"
    
    except Exception as e:
        return None, None, f"Error loading system: {str(e)}"


def display_header():
    """Display main header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<p class="main-header">🤖 RAG Query System</p>', unsafe_allow_html=True)
        st.markdown("*Retrieve relevant information from documents and get AI-powered answers*")
    
    with col2:
        if st.session_state.system_ready:
            st.success("✅ System Ready")
        else:
            st.error("❌ System Not Ready")


def setup_sidebar():
    """Setup sidebar with configuration"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # System status
        st.subheader("System Status")
        if st.session_state.system_ready:
            st.markdown("**Status**: ✅ Ready to use")
            st.markdown(f"**Top-K**: {settings.rag_top_k}")
            st.markdown(f"**Max Context**: {settings.rag_max_context_chars:,} chars")
        else:
            st.markdown("**Status**: ❌ Not initialized")
        
        # Settings
        st.divider()
        st.subheader("Query Settings")
        
        top_k = st.slider(
            "Number of sources to retrieve",
            min_value=1,
            max_value=20,
            value=settings.rag_top_k,
            help="How many document chunks to use for context"
        )
        st.session_state.top_k = top_k
        
        # Sample queries
        st.divider()
        st.subheader("📚 Sample Queries")
        sample_questions = [
            "What is artificial intelligence?",
            "Explain machine learning",
            "What causes climate change?",
            "How does blockchain work?",
            "What are renewable energy solutions?",
        ]
        
        for question in sample_questions:
            if st.button(f"❓ {question}", key=f"sample_{question}", use_container_width=True):
                st.session_state.query_input = question
        
        # Documentation
        st.divider()
        st.subheader("📖 Documentation")
        if st.button("📋 README", use_container_width=True):
            st.session_state.show_docs = "README"
        if st.button("⚙️ Setup Guide", use_container_width=True):
            st.session_state.show_docs = "SETUP"
        if st.button("📊 Project Info", use_container_width=True):
            st.session_state.show_docs = "INFO"


def display_query_interface():
    """Display main query interface"""
    st.subheader("💬 Ask a Question")
    
    # Query input
    query = st.text_area(
        "Enter your question:",
        key="query_input",
        height=100,
        placeholder="Ask anything about the documents...",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        submit_button = st.button("🔍 Search", use_container_width=True, type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    with col3:
        if st.button("📌 Save Query", use_container_width=True):
            if query:
                st.session_state.chat_history.append({
                    "query": query,
                    "timestamp": datetime.now().isoformat()
                })
                st.success("Query saved!")
    
    if clear_button:
        st.session_state.query_input = ""
        st.rerun()
    
    # Process query
    if submit_button and query:
        if not st.session_state.system_ready:
            st.error("❌ System not ready. Please initialize first.")
            return
        
        with st.spinner("🔄 Processing your query..."):
            try:
                result = st.session_state.rag_engine.answer(
                    query, 
                    top_k=st.session_state.get("top_k", settings.rag_top_k)
                )
                
                # Display answer
                st.markdown("### 📝 Answer")
                st.markdown(f'<div class="response-box">{result.answer}</div>', 
                          unsafe_allow_html=True)
                
                # Display sources
                st.markdown("### 📚 Sources")
                if result.sources:
                    cols = st.columns(1)
                    for i, source in enumerate(result.sources):
                        with st.expander(
                            f"Source {i+1}: {source.get('source', 'Unknown')} (Score: {source['score']:.3f})",
                            expanded=(i == 0)
                        ):
                            st.markdown(f'<div class="source-box">', unsafe_allow_html=True)
                            st.markdown(f"**Chunk ID**: `{source['chunk_id']}`")
                            st.markdown(f"**Score**: {source['score']:.4f}")
                            st.markdown(f"**Source**: {source.get('source', 'Unknown')}")
                            if source.get('page'):
                                st.markdown(f"**Page**: {source['page']}")
                            st.markdown(f'</div>', unsafe_allow_html=True)
                
                # Save to history
                st.session_state.chat_history.append({
                    "query": query,
                    "answer": result.answer,
                    "sources": result.sources,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")


def display_stats():
    """Display system statistics"""
    st.markdown("### 📊 System Statistics")
    
    try:
        # Count documents and chunks
        if st.session_state.rag_engine:
            store = st.session_state.rag_engine.retriever.store
            num_chunks = len(store.records)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📦 Total Chunks", num_chunks)
            
            with col2:
                st.metric("📄 Documents", "3 (AI, Climate, Blockchain)")
            
            with col3:
                st.metric("📊 Vector Dimension", "1536")
            
            with col4:
                st.metric("✅ Status", "Ready")
    
    except Exception as e:
        st.warning(f"Could not load statistics: {str(e)}")


def display_settings_tab():
    """Display settings and configuration tab"""
    st.subheader("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Environment Configuration")
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key and api_key.startswith("sk-"):
            st.success("✅ OpenAI API Key configured")
        else:
            st.error("❌ OpenAI API Key not configured")
            st.info("Add OPENAI_API_KEY to .env file")
        
        st.markdown("### RAG Parameters")
        st.markdown(f"- **Top-K Retrieval**: {settings.rag_top_k}")
        st.markdown(f"- **Max Context**: {settings.rag_max_context_chars:,} chars")
        st.markdown(f"- **Chunk Size**: {settings.chunk_size_chars:,} chars")
        st.markdown(f"- **Chunk Overlap**: {settings.chunk_overlap_chars:,} chars")
    
    with col2:
        st.markdown("### Model Configuration")
        st.markdown(f"- **Chat Model**: {settings.chat_model}")
        st.markdown(f"- **Embed Model**: {settings.embed_model}")
        
        st.markdown("### Data Paths")
        st.markdown(f"- **Raw Data**: {settings.raw_data_dir}")
        st.markdown(f"- **Index Dir**: {settings.index_dir}")
        st.markdown(f"- **Index Name**: {settings.index_name}")


def display_chat_history_tab():
    """Display chat history"""
    st.subheader("💬 Chat History")
    
    if not st.session_state.chat_history:
        st.info("No queries yet. Ask a question to get started!")
        return
    
    # Download history
    if st.button("📥 Download History", use_container_width=True):
        history_json = json.dumps(st.session_state.chat_history, indent=2, default=str)
        st.download_button(
            label="Download JSON",
            data=history_json,
            file_name=f"rag_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Display history
    for i, entry in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(
            f"Query {len(st.session_state.chat_history) - i}: {entry.get('query', '')[:50]}...",
            expanded=False
        ):
            st.markdown(f"**Time**: {entry.get('timestamp', 'Unknown')}")
            st.markdown(f"**Query**: {entry.get('query', '')}")
            if "answer" in entry:
                st.markdown(f"**Answer**: {entry['answer']}")
                if "sources" in entry:
                    st.markdown(f"**Sources**: {len(entry['sources'])} documents")


def display_about_tab():
    """Display about information"""
    st.subheader("ℹ️ About RAG System")
    
    st.markdown("""
    ### What is RAG?
    
    **RAG (Retrieval Augmented Generation)** combines document retrieval with AI language models to:
    - Answer questions based on your documents
    - Cite sources for transparency
    - Reduce hallucinations through grounding in real data
    
    ### How it Works
    
    1. **Document Loading**: Load TXT and PDF files
    2. **Chunking**: Split documents into manageable pieces
    3. **Embeddings**: Convert text to vector embeddings
    4. **Indexing**: Store vectors in efficient index
    5. **Retrieval**: Find relevant chunks for query
    6. **Generation**: Use LLM to generate answers with context
    
    ### Features
    
    ✅ Multiple document formats (TXT, PDF)
    ✅ Semantic search with top-K retrieval
    ✅ Source attribution and transparency
    ✅ Configurable parameters
    ✅ Chat history tracking
    ✅ Batch processing support
    ✅ REST API integration
    
    ### Project Components
    
    - **src/**: Core RAG modules
    - **data/raw/**: Input documents
    - **data/index/**: Vector index storage
    - **streamlit_app.py**: This UI
    - **api.py**: REST API server
    - **chat_cli.py**: CLI interface
    
    ### Documentation
    
    - README.md - Setup and usage
    - SETUP.md - Configuration guide
    - COMPLETED.md - Implementation details
    """)


def main():
    """Main Streamlit app"""
    display_header()
    setup_sidebar()
    
    # Initialize RAG system
    if not st.session_state.system_ready:
        st.info("Initializing RAG system...")
        rag, embedder, message = load_rag_system()
        
        if rag and embedder:
            st.session_state.rag_engine = rag
            st.session_state.embedder = embedder
            st.session_state.system_ready = True
            st.success("✅ " + message)
        else:
            st.error(message)
            st.error("The vector index was not found. Please run: `python ingest_and_run.py`")
            st.stop()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Query", 
        "📊 Statistics", 
        "⚙️ Settings", 
        "💬 History",
        "ℹ️ About"
    ])
    
    with tab1:
        display_query_interface()
    
    with tab2:
        display_stats()
    
    with tab3:
        display_settings_tab()
    
    with tab4:
        display_chat_history_tab()
    
    with tab5:
        display_about_tab()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.85rem;'>
        RAG System | Built with Streamlit | Powered by OpenAI
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
