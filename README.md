# Personal Knowledge Base - RAG System

A clean, minimalist Retrieval-Augmented Generation (RAG) system built with vanilla JavaScript, Python, and SQLite. No external dependencies like Hugging Face API, no complex vector databases—just pure local processing with an Apple-inspired UI.

![Tech Stack](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20JS-yellow.svg)
![Database](https://img.shields.io/badge/Database-SQLite-green.svg)

##  Project Goal

Learn RAG fundamentals by building a practical, real-world application where you can:
- Upload documents (PDF, TXT, Markdown)
- Ask questions in natural language
- Get AI-powered answers with source citations
- Keep everything local and private

##  Features

- **Document Upload**: Supports PDF, TXT, and Markdown files
- **Semantic Search**: Uses sentence transformers for accurate retrieval
- **Local Storage**: Everything stored in SQLite—no cloud dependencies
- **Apple-Style UI**: Clean, modern interface inspired by iCloud.com
- ** Fast & Lightweight**: Runs entirely on your machine
- **Privacy First**: No data leaves your computer

## Architecture

### How RAG Works

```
┌─────────────────────────────────────────────────────────────┐
│                    1. INDEXING PHASE                         │
├─────────────────────────────────────────────────────────────┤
│  Document → Text Extraction → Chunking → Embeddings → SQLite│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    2. RETRIEVAL PHASE                        │
├─────────────────────────────────────────────────────────────┤
│  Question → Embedding → Similarity Search → Top K Chunks    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    3. GENERATION PHASE                       │
├─────────────────────────────────────────────────────────────┤
│  Question + Retrieved Chunks → LLM → Answer with Citations  │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Backend:**
- **Flask**: Lightweight API server
- **SQLite**: Database for documents and embeddings
- **sentence-transformers**: Local embedding generation (all-MiniLM-L6-v2)
- **NumPy**: Vector similarity calculations
- **PyPDF2**: PDF text extraction

**Frontend:**
- **Vanilla JavaScript**: No frameworks, no build tools
- **CSS3**: Modern glassmorphism effects
- **HTML5**: Semantic markup

## Project Structure

```
rag-system/
├── backend/
│   ├── app.py              # Flask API endpoints
│   ├── database.py         # SQLite operations
│   ├── embeddings.py       # Embedding model handler
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   └── index.html          # Single-page vanilla JS app
│
└── data/                   # Created automatically
    ├── uploads/            # Uploaded files
    └── knowledge.db        # SQLite database
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- ~500MB free disk space (for embedding model)

### Step 1: Clone or Download

```bash
mkdir rag-system
cd rag-system
```

### Step 2: Set Up Backend

```bash
# Create backend directory and files
mkdir -p backend data

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation

The first time you run the backend, it will download the embedding model (~80MB):

```bash
python app.py
```

You should see:
```
Loading embedding model: all-MiniLM-L6-v2
Model loaded successfully!
 * Running on http://127.0.0.1:5000
```

## Usage

### Starting the Application

1. **Start the backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

2. **Open the frontend:**
   - Simply open `frontend/index.html` in your browser
   - Or use a local server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

### Using the Knowledge Base

#### 1. Upload Documents

Click the "Upload" button and select your documents:
- Supported formats: `.pdf`, `.txt`, `.md`
- Multiple files can be uploaded at once
- Documents are automatically processed and chunked

#### 2. Search Your Knowledge

Type a question in the search bar and hit Enter or click "Search":
- Example: "What are the main findings about climate change?"
- The system will find relevant chunks and display them with source citations
- Similarity scores show how relevant each source is

#### 3. Manage Documents

- View all uploaded documents in the grid
- Hover over a document card to see the delete button
- Click delete to remove a document and all its chunks

## Configuration

### Chunking Strategy

Edit `app.py` to customize chunking:

```python
def chunk_text(text, chunk_size=500, overlap=50):
    # chunk_size: words per chunk
    # overlap: overlapping words between chunks
```

**Recommendations:**
- Small documents: `chunk_size=300, overlap=30`
- Large documents: `chunk_size=700, overlap=100`
- Technical docs: `chunk_size=400, overlap=80`

### Embedding Model

Change the model in `embeddings.py`:

```python
class EmbeddingModel:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
```

**Alternative models:**
- `all-mpnet-base-v2`: Higher quality, slower (420MB)
- `paraphrase-MiniLM-L3-v2`: Faster, lighter (61MB)
- `multi-qa-MiniLM-L6-cos-v1`: Optimized for Q&A

### Search Results

Adjust the number of retrieved chunks in `app.py`:

```python
@app.route('/api/search', methods=['POST'])
def search():
    top_k = data.get('top_k', 5)  # Change this number
```

## Database Schema

### Documents Table
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    chunk_count INTEGER DEFAULT 0
);
```

### Chunks Table
```sql
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding BLOB NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES documents (id) ON DELETE CASCADE
);
```

Embeddings are stored as binary blobs (float32 arrays) for efficiency.

## Learning Path

This project is designed for progressive learning:

### Phase 1: Basic Retrieval (Current)
✅ Document upload and processing  
✅ Text chunking  
✅ Embedding generation  
✅ Similarity search  
✅ Source citation  

### Phase 2: Enhanced Generation (Next Steps)
- [ ] Integrate local LLM (Ollama, LlamaCPP)
- [ ] Add prompt engineering for better answers
- [ ] Implement streaming responses
- [ ] Add conversation history

### Phase 3: Advanced Features
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking with cross-encoders
- [ ] Metadata filtering (date, author, tags)
- [ ] Query expansion and reformulation
- [ ] Multi-document summarization

### Phase 4: Production Ready
- [ ] User authentication
- [ ] Multiple knowledge bases
- [ ] Caching layer
- [ ] Monitoring and analytics
- [ ] Upgrade to vector database (pgvector, Qdrant)

## Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError`**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: `Port 5000 already in use`**
```python
# Change port in app.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use different port
```

### Frontend can't connect to backend

**CORS Error:**
- Make sure `flask-cors` is installed
- Backend must be running before opening frontend
- Check browser console for specific error messages

**API URL mismatch:**
```javascript
// In index.html, update the API URL if needed
const API_URL = 'http://localhost:5000/api';
```

### Upload fails

**PDF extraction error:**
```bash
# Install updated PyPDF2
pip install --upgrade PyPDF2
```

**File size issues:**
- Default Flask limit is 16MB
- Increase in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

### Search returns no results

**No documents uploaded:**
- Upload at least one document first

**Embedding dimension mismatch:**
- Delete `data/knowledge.db`
- Restart backend to rebuild database

**Query too vague:**
- Try more specific questions
- Include keywords from your documents

## Performance Tips

### Faster Uploads
- Use `.txt` files instead of PDFs when possible
- Pre-process documents to remove unnecessary content
- Batch upload multiple files at once

### Better Search Results
- Use complete sentences as queries
- Include domain-specific terms
- Ask one question at a time

### Optimize Database
```sql
-- Run periodically to optimize
sqlite3 data/knowledge.db "VACUUM;"
```

## Privacy & Security

- **All data stays local**: No external API calls
- **No tracking**: No analytics or telemetry
- **Secure by default**: No authentication required (single-user)
- **Data portability**: SQLite database is easily backed up

##  API Reference

### POST `/api/upload`
Upload and process a document.

**Request:**
```
Content-Type: multipart/form-data
file: [binary file data]
```

**Response:**
```json
{
  "id": 1,
  "name": "document.pdf",
  "chunks": 42,
  "size": 245760
}
```

### POST `/api/search`
Search for relevant information.

**Request:**
```json
{
  "query": "What is machine learning?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Based on the retrieved information...",
  "sources": [
    {
      "docName": "ml-guide.pdf",
      "excerpt": "Machine learning is...",
      "score": 0.89
    }
  ]
}
```

### GET `/api/documents`
List all documents.

**Response:**
```json
[
  {
    "id": 1,
    "name": "document.pdf",
    "chunks": 42,
    "uploadedAt": "2025-01-15T10:30:00",
    "size": "240.0 KB"
  }
]
```

### DELETE `/api/documents/:id`
Delete a document and its chunks.

**Response:**
```json
{
  "success": true
}
```

## Contributing

This is a learning project! Feel free to:
- Experiment with different chunking strategies
- Try different embedding models
- Add new features (tagging, filtering, etc.)
- Improve the UI/UX

## Resources

### Learn More About RAG
- [Anthropic's RAG Guide](https://docs.anthropic.com/claude/docs/retrieval-augmented-generation)
- [LangChain Documentation](https://python.langchain.com/docs/use_cases/question_answering/)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)

### Embedding Models
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Hugging Face Model Hub](https://huggingface.co/models?pipeline_tag=sentence-similarity)

### Vector Search
- [Understanding Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Vector Database Comparison](https://github.com/erikbern/ann-benchmarks)

## License

This project is open source and available for educational purposes. Use it to learn, modify it, and build something awesome!

## Acknowledgments

- Built as a clean, minimal RAG learning project
- UI inspired by Apple's iCloud design language
- Uses open-source models from Hugging Face
- No bloat, no over-engineering—just the essentials

---

**Happy Learning! **

Questions? Issues? This is a learning project—break things, fix things, and learn!
