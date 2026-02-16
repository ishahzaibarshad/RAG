# RAG Project - Setup & Implementation Checklist

## ✅ Completed Components

### Core Modules (src/)
- [x] `__init__.py` - Package initialization
- [x] `config.py` - Configuration management with Settings dataclass
- [x] `loaders.py` - Document loading (TXT and PDF support)
- [x] `chunking.py` - Text chunking with overlap
- [x] `embeddings.py` - OpenAI embeddings integration
- [x] `vector_store.py` - NumPy-based vector store with cosine similarity
- [x] `retriever.py` - Semantic search with top-K retrieval
- [x] `rag.py` - RAG engine combining retrieval + LLM
- [x] `api.py` - FastAPI REST endpoint for queries
- [x] `chat_cli.py` - Interactive CLI chat interface
- [x] `ingest.py` - Pipeline to ingest documents and build index

### Data & Configuration
- [x] `data/raw/` - Sample documents included (3 text files)
  - `sample_ai.txt` - Artificial Intelligence overview
  - `sample_climate.txt` - Climate Change information
  - `sample_blockchain.txt` - Blockchain technology guide
- [x] `data/index/` - Directory for vector index (created on first ingest)
- [x] `.env` - Environment configuration file
- [x] `.env.example` - Template for environment variables
- [x] `requirements.txt` - Python dependencies

### Documentation & Examples
- [x] `README.md` - Comprehensive documentation
- [x] `.gitignore` - Git ignore rules
- [x] `SETUP.md` - This setup guide
- [x] `example.py` - Programmatic usage example
- [x] `batch_query.py` - Batch query processing example
- [x] `ingest_and_run.py` - Easy startup script

## 🚀 How to Get Started

### Step 1: Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Get free API key: https://platform.openai.com/api-keys
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Ingest Sample Data & Run
```bash
# Single command that does everything
python ingest_and_run.py
```

This will:
1. Load sample documents from `data/raw/`
2. Split into chunks
3. Generate embeddings (via OpenAI)
4. Save index to `data/index/`
5. Start interactive CLI

## 💬 Usage Modes

### 1. Interactive CLI Chat
```bash
python ingest_and_run.py
```
Then type your questions and get answers with sources.

### 2. REST API Server
```bash
python ingest_and_run.py api
```
Server runs on `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Endpoint: `POST /query`

### 3. Single Query
```bash
python ingest_and_run.py query "What is AI?"
```

### 4. Example Script
```bash
python example.py
```
Shows programmatic usage with multiple queries.

### 5. Batch Processing
```bash
python batch_query.py
```
Processes queries from `sample_queries.json` and saves results.

## 📚 Adding Your Own Documents

1. Add `.txt` or `.pdf` files to `data/raw/`
2. Run: `python ingest_and_run.py`
3. System automatically re-indexes

**Supported formats:**
- Text files (`.txt`) - Plain text, loaded as-is
- PDF files (`.pdf`) - Each page becomes a separate document

## ⚙️ Configuration Options

Edit `.env` to customize:

```env
# LLM & Embeddings
OPENAI_API_KEY=sk-...                 # Required - get from OpenAI
OPENAI_CHAT_MODEL=gpt-4o-mini         # Chat model
OPENAI_EMBED_MODEL=text-embedding-3-small  # Embedding model

# RAG Parameters
RAG_TOP_K=5                            # Number of chunks to retrieve
RAG_MAX_CONTEXT_CHARS=12000           # Max context length for LLM

# Chunking
CHUNK_SIZE_CHARS=1800                 # Chunk size in characters
CHUNK_OVERLAP_CHARS=250               # Overlap between chunks

# Paths
RAW_DATA_DIR=./data/raw               # Source documents
INDEX_DIR=./data/index                # Index location
INDEX_NAME=main                       # Index name
```

## 🔍 Project Architecture

```
Input Docs
     ↓
[Loader] - Reads TXT/PDF files
     ↓
Document Objects (doc_id, text, metadata)
     ↓
[Chunker] - Splits with overlap
     ↓
Chunk Objects (chunk_id, text, metadata)
     ↓
[Embedder] - OpenAI embeddings
     ↓
Vector Embeddings (NumPy arrays)
     ↓
[VectorStore] - Saves vectors + metadata
     ↓
Index Files (*.npy + *_meta.json)

---

Query Input
     ↓
[Embedder] - Embed query
     ↓
Query Vector
     ↓
[Retriever] - Cosine similarity search
     ↓
Top-K Chunks with scores
     ↓
[RAGEngine] - Format context
     ↓
[OpenAI] - Generate answer using context
     ↓
Answer + Sources
```

## 📊 Expected Performance

- **Embedding**: ~30 texts/sec (batch size 64)
- **Search**: <5ms per query (NumPy optimized)
- **LLM**: 1-5 seconds per answer (depends on OpenAI)

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not set"
**Solution**: Add key to `.env`
```bash
OPENAI_API_KEY=sk-your-key-here
```

### Error: "Index not found"
**Solution**: Run ingestion first
```bash
python ingest_and_run.py
```

### Error: "No chunks produced"
**Solution**: Add documents to `data/raw/`
- Must be `.txt` or `.pdf` files
- Must have proper extensions
- Re-run ingestion

### API Returns Empty Answer
**Solution**: Check that documents are indexed
- Increase `RAG_TOP_K` in `.env`
- Check documents in `data/raw/`
- Verify index was created

## 🔗 API Documentation

### Query Endpoint
```
POST /query
Content-Type: application/json
```

**Request:**
```json
{
  "question": "What is artificial intelligence?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Artificial Intelligence (AI) is the simulation...",
  "sources": [
    {
      "chunk_id": "sample_ai.txt::chunk=0",
      "score": 0.847,
      "source": "sample_ai.txt",
      "page": null
    }
  ]
}
```

## 📖 Code Examples

### Using as a Library
```python
from src.rag import RAGEngine
from src.retriever import Retriever
from src.embeddings import Embedder
from src.vector_store import NumpyVectorStore
from src.config import settings

store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
embedder = Embedder()
retriever = Retriever(store, embedder)
rag = RAGEngine(retriever)

result = rag.answer("Your question here")
print(result.answer)
print(result.sources)
```

### Direct Retrieval
```python
from src.retriever import Retriever
from src.embeddings import Embedder
from src.vector_store import NumpyVectorStore
from src.config import settings

store = NumpyVectorStore.load(settings.index_dir, settings.index_name)
embedder = Embedder()
retriever = Retriever(store, embedder)

chunks = retriever.retrieve("your query", top_k=5)
for chunk in chunks:
    print(f"Score: {chunk.score:.3f}")
    print(f"Text: {chunk.text[:100]}...")
```

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Add OpenAI API key
3. ✅ Run `python ingest_and_run.py`
4. ✅ Try queries
5. Optional: Add your own documents
6. Optional: Deploy as API service

## 📝 Sample Data Included

Three comprehensive documents are included:

1. **Artificial Intelligence** - Overview of AI, ML, NLP, Computer Vision, Robotics, etc.
2. **Climate Change** - Causes, impacts, solutions, and global cooperation
3. **Blockchain** - Technology fundamentals, applications, challenges, future directions

These cover different technical domains and provide good test cases for RAG queries.

## 🔐 Security Notes

- API key is stored in `.env` (don't commit to git)
- `.env` is in `.gitignore`
- Use environment variables in production
- Validate user inputs in production deployment

## 💡 Tips & Tricks

1. **Improve Results**:
   - Add more relevant documents
   - Adjust `CHUNK_SIZE_CHARS` (bigger = more context)
   - Adjust `RAG_TOP_K` (more chunks = more context)

2. **Speed Up**:
   - Reduce `CHUNK_SIZE_CHARS`
   - Reduce `RAG_TOP_K`
   - Use cheaper embedding model

3. **Better Quality**:
   - Use `gpt-4` instead of `gpt-4o-mini`
   - Increase `RAG_MAX_CONTEXT_CHARS`
   - Add more relevant documents

## 📞 Support

Check the [README.md](README.md) for more information.
