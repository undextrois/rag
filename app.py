from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from database import Database
from embeddings import EmbeddingModel
import PyPDF2
import io

app = Flask(__name__)
CORS(app)

# Initialize
db = Database('data/knowledge.db')
embedding_model = EmbeddingModel()

UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def extract_text_from_pdf(file_content):
    """Extract text from PDF bytes"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'
    return text

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and process a document"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Read file content
    file_content = file.read()
    filename = file.filename
    
    # Extract text based on file type
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_content)
    elif filename.endswith(('.txt', '.md')):
        text = file_content.decode('utf-8')
    else:
        return jsonify({'error': 'Unsupported file type'}), 400
    
    # Create document record
    doc_id = db.add_document(filename, text)
    
    # Chunk the text
    chunks = chunk_text(text)
    
    # Generate embeddings and store chunks
    for chunk in chunks:
        embedding = embedding_model.embed(chunk)
        db.add_chunk(doc_id, chunk, embedding)
    
    return jsonify({
        'id': doc_id,
        'name': filename,
        'chunks': len(chunks),
        'size': len(file_content)
    })

@app.route('/api/search', methods=['POST'])
def search():
    """Search for relevant chunks"""
    data = request.json
    query = data.get('query', '')
    top_k = data.get('top_k', 5)
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Generate query embedding
    query_embedding = embedding_model.embed(query)
    
    # Search for similar chunks
    results = db.search_similar(query_embedding, top_k)
    
    # Format results
    sources = []
    for chunk_text, doc_name, similarity in results:
        sources.append({
            'docName': doc_name,
            'excerpt': chunk_text[:300] + '...' if len(chunk_text) > 300 else chunk_text,
            'score': float(similarity)
        })
    
    # Simple answer generation (concatenate top results)
    context = '\n\n'.join([r[0] for r in results[:3]])
    answer = f"Based on the retrieved information: {context[:500]}..."
    
    return jsonify({
        'answer': answer,
        'sources': sources
    })

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get all documents"""
    documents = db.get_all_documents()
    return jsonify(documents)

@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document and its chunks"""
    db.delete_document(doc_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
