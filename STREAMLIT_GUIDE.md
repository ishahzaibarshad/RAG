# Streamlit UI - Complete Integration Guide

## 🎨 Overview

A professional, feature-rich Streamlit web interface for your RAG system with:
- ✅ Interactive query interface
- ✅ Real-time answer generation
- ✅ Source attribution and details
- ✅ Chat history tracking
- ✅ System statistics
- ✅ Configuration management
- ✅ Sample queries
- ✅ Export history

---

## 🚀 Quick Start

### 1. Install Streamlit (if not already done)
```bash
pip install -r requirements.txt
# or just: pip install streamlit
```

### 2. Ensure Index is Created
```bash
# First time only - creates vector index from sample data
python ingest_and_run.py
# (This opens CLI, type 'exit' to quit and use Streamlit instead)
```

### 3. Start Streamlit UI
```bash
# Option 1: Using helper script
python run_streamlit.py

# Option 2: Direct command
streamlit run streamlit_app.py
```

### 4. Open in Browser
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501

---

## 📋 Features

### Main Query Interface (Tab 1)
- **Query Input**: Multi-line text area for questions
- **Search Button**: Process and retrieve answers
- **Clear Button**: Reset query
- **Save Query**: Add to chat history
- **Instant Answers**: AI-generated responses with context
- **Source Details**: Expandable source citations with scores

### Statistics Dashboard (Tab 2)
- Total number of indexed chunks
- Number of documents
- Vector dimension information
- System status

### Settings Panel (Tab 3)
- Environment configuration status
- RAG parameters display
- Model information
- Data path configuration

### Chat History (Tab 4)
- View all previous queries and answers
- Download history as JSON
- Persistent during session
- Timestamps for each entry

### About Page (Tab 5)
- RAG technology explanation
- How the system works
- Features overview
- Project structure

### Sidebar Features
- **System Status**: Quick status indicator
- **Query Settings**: Adjust top-K retrieval count
- **Sample Queries**: Pre-built example questions
- **Documentation Links**: Access guides

---

## 🎯 Usage Examples

### Asking Questions
1. Type question in the query box
2. Click "🔍 Search"
3. View answer and sources
4. Expand sources for details

### Sample Queries
Click any sample in sidebar:
- "What is artificial intelligence?"
- "Explain machine learning"
- "What causes climate change?"
- "How does blockchain work?"
- "What are renewable energy solutions?"

### Tracking Queries
1. Ask questions (automatically saved)
2. Go to "💬 History" tab
3. View all previous queries
4. Download as JSON for records

---

## 🔧 Configuration

### In `.env` File
```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (already configured)
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small
RAG_TOP_K=5
RAG_MAX_CONTEXT_CHARS=12000
```

### In Streamlit UI
- Adjust top-K retrieval using slider in sidebar
- View all current settings in ⚙️ Settings tab
- Changes apply immediately to next query

---

## 📊 Interface Layout

```
┌─────────────────────────────────────────────────────┐
│  🤖 RAG Query System                      ✅ Ready  │
│  Retrieve relevant information...                   │
├──────────┬──────────────────────────────────────────┤
│ Sidebar  │  Main Content Area                       │
│          │                                          │
│ Settings │  [Tabs: Query | Stats | Settings | ...] │
│ Samples  │                                          │
│ Docs     │  Query Interface                         │
│          │  ┌──────────────────────────────────┐   │
│          │  │ Enter your question here...       │   │
│          │  └──────────────────────────────────┘   │
│          │  [Search] [Clear] [Save Query]          │
│          │                                          │
│          │  📝 Answer                               │
│          │  ┌──────────────────────────────────┐   │
│          │  │ Response here...                 │   │
│          │  └──────────────────────────────────┘   │
│          │                                          │
│          │  📚 Sources                              │
│          │  ▶ Source 1: doc.txt (Score: 0.85)     │
│          │  ▶ Source 2: doc.txt (Score: 0.82)     │
│          │                                          │
└──────────┴──────────────────────────────────────────┘
```

---

## 🎨 UI Sections

### Top Header
- App title with gradient text
- System status indicator
- Quick visual feedback

### Query Section
- Large text area for questions
- Three action buttons
- Real-time processing indicator

### Answer Display
- Styled response box
- Clear readable format
- Citation support

### Sources Panel
- Expandable source details
- Score information
- Chunk ID reference
- Page numbers (if applicable)

### Sidebar
- System status
- Top-K slider (1-20)
- Sample questions
- Documentation links

---

## 🔄 Workflow

```
User Enters Query
       ↓
Click "Search"
       ↓
Streamlit Calls RAG Engine
       ↓
Query gets embedded
       ↓
Retrieve top-K similar chunks
       ↓
Format context
       ↓
Send to OpenAI GPT
       ↓
Get answer + sources
       ↓
Display in UI
       ↓
Save to history
```

---

## 💡 Tips & Tricks

### Better Results
1. Ask specific, detailed questions
2. Include context in your query
3. Use multiple queries to explore topics
4. Check source scores (higher = more relevant)

### Performance
1. First run takes 20-30 seconds (index loading)
2. Subsequent queries take 1-5 seconds
3. Reduces latency with caching
4. Batch operations not available in UI

### Customization
1. Edit `streamlit_app.py` to modify UI
2. Change colors in custom CSS section
3. Add more sample questions to sidebar
4. Modify tab names and order

---

## 🐛 Troubleshooting

### "System not ready" Error
```bash
# Solution: Create index first
python ingest_and_run.py
# Then re-run Streamlit
python run_streamlit.py
```

### "Index not found" Error
```bash
# Solution: Run ingestion
python ingest_and_run.py
# Check: data/index/ should have files
```

### "API Key not set" Error
```bash
# Solution: Add to .env
OPENAI_API_KEY=sk-your-key-here
```

### Slow Performance
1. Close other applications
2. Check internet connection
3. API latency depends on OpenAI
4. Vector search is already optimized

### Streamlit Not Responding
```bash
# Restart:
# 1. Press CTRL+C to stop
# 2. Run: python run_streamlit.py again
# 3. Refresh browser
```

---

## 🚀 Advanced Usage

### Running on Server
```bash
# Make publicly accessible
streamlit run streamlit_app.py --server.address 0.0.0.0

# With authentication
streamlit run streamlit_app.py \
  --server.address your-server.com \
  --server.port 8501
```

### Environment Variables
```bash
# Set in terminal before running
set STREAMLIT_SERVER_PORT=8501
set STREAMLIT_SERVER_HEADLESS=true
python run_streamlit.py
```

### Docker Deployment
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## 📱 Responsive Design

- **Desktop**: Full width with all features
- **Tablet**: Two-column layout adapts
- **Mobile**: Stacked layout, sidebar collapses
- **Dark Mode**: Supported in Streamlit settings

---

## 🔐 Security Notes

- API key stored in `.env` (never commit)
- All processing happens locally or at OpenAI
- No data stored on browser
- History stored only in session memory

---

## 🎓 Learning

### Understanding RAG
1. Check "ℹ️ About" tab in UI
2. Read README.md
3. View SETUP.md for details
4. Check src/ code for implementation

### Modifying UI
1. Edit `streamlit_app.py`
2. Streamlit hot-reloads changes
3. Check Streamlit docs: streamlit.io/docs
4. Customize as needed

---

## 📊 Comparison: Interfaces

| Feature | CLI | API | Streamlit |
|---------|-----|-----|-----------|
| Ease of Use | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Visual | Text | JSON | Beautiful |
| Interactivity | Good | Good | Excellent |
| History | Manual | Manual | Automatic |
| History Export | Manual | Manual | Built-in |
| Sources | Listed | Included | Expandable |
| Configuration | Env | Headers | UI Sliders |
| Learning Curve | Low | Medium | Very Low |

---

## 🎉 Ready to Use!

Your RAG system is now fully integrated with Streamlit!

```bash
# Make sure index exists:
python ingest_and_run.py

# Then start Streamlit:
python run_streamlit.py

# Open: http://localhost:8501
```

Enjoy the interactive experience! 🚀
