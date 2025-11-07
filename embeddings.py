from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize embedding model
        
        all-MiniLM-L6-v2 is a good default:
        - Fast (only 80MB)
        - 384 dimensions
        - Good quality for semantic search
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully!")
    
    def embed(self, text):
        """Generate embedding for a single text"""
        if isinstance(text, str):
            text = [text]
        
        embeddings = self.model.encode(text, convert_to_numpy=True)
        
        # Return single embedding if single text was provided
        if len(embeddings) == 1:
            return embeddings[0]
        return embeddings
    
    def embed_batch(self, texts, batch_size=32):
        """Generate embeddings for multiple texts efficiently"""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True
        )
    
    def get_embedding_dimension(self):
        """Get the dimension of embeddings"""
        return self.model.get_sentence_embedding_dimension()
