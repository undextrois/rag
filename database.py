import sqlite3
import numpy as np
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chunk_count INTEGER DEFAULT 0
            )
        ''')
        
        # Chunks table with embeddings stored as BLOB
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                embedding BLOB NOT NULL,
                FOREIGN KEY (doc_id) REFERENCES documents (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_document(self, name, content):
        """Add a new document"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO documents (name, content, chunk_count) VALUES (?, ?, ?)',
            (name, content, 0)
        )
        doc_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return doc_id
    
    def add_chunk(self, doc_id, text, embedding):
        """Add a chunk with its embedding"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Convert numpy array to bytes
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        cursor.execute(
            'INSERT INTO chunks (doc_id, text, embedding) VALUES (?, ?, ?)',
            (doc_id, text, embedding_bytes)
        )
        
        # Update chunk count
        cursor.execute(
            'UPDATE documents SET chunk_count = chunk_count + 1 WHERE id = ?',
            (doc_id,)
        )
        
        conn.commit()
        conn.close()
    
    def search_similar(self, query_embedding, top_k=5):
        """Search for similar chunks using cosine similarity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get all chunks with their embeddings
        cursor.execute('''
            SELECT c.text, d.name, c.embedding
            FROM chunks c
            JOIN documents d ON c.doc_id = d.id
        ''')
        
        results = []
        query_norm = np.linalg.norm(query_embedding)
        
        for row in cursor.fetchall():
            text = row[0]
            doc_name = row[1]
            embedding_bytes = row[2]
            
            # Convert bytes back to numpy array
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            
            # Calculate cosine similarity
            embedding_norm = np.linalg.norm(embedding)
            if embedding_norm > 0 and query_norm > 0:
                similarity = np.dot(query_embedding, embedding) / (query_norm * embedding_norm)
            else:
                similarity = 0
            
            results.append((text, doc_name, similarity))
        
        conn.close()
        
        # Sort by similarity and return top k
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:top_k]
    
    def get_all_documents(self):
        """Get all documents with metadata"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, chunk_count, uploaded_at,
                   length(content) as size
            FROM documents
            ORDER BY uploaded_at DESC
        ''')
        
        documents = []
        for row in cursor.fetchall():
            documents.append({
                'id': row[0],
                'name': row[1],
                'chunks': row[2],
                'uploadedAt': row[3],
                'size': f"{row[4] / 1024:.1f} KB"
            })
        
        conn.close()
        return documents
    
    def delete_document(self, doc_id):
        """Delete a document and all its chunks"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
        # Chunks will be deleted automatically due to CASCADE
        
        conn.commit()
        conn.close()
    
    def get_document(self, doc_id):
        """Get a specific document"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
