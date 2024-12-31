# app/services/rag/vector_store.py
from typing import List, Dict
from pinecone import Pinecone, Index
from .embedder import Embedder
import logging
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, api_key: str, openai_api_key: str, environment: str = "us-east-1", ):
        """Initialize connection to Pinecone vector store"""
        self.pc = Pinecone(api_key=api_key)
        self.index_name = "tailor-tutor"  # Your existing index name
        self.index = self.pc.Index(self.index_name)
        self.embedder = Embedder(openai_api_key)
        
    async def index_chunks(self, chunks: List[Dict], batch_size: int = 100) -> None:
        """
        Index a list of chunks with their embeddings.
        
        Args:
            chunks: List of dictionaries containing text and metadata
            batch_size: Number of vectors to upsert in each batch
        """
        try:
            # Extract texts for embedding
            texts = [chunk["text"] for chunk in chunks]
            
            # Generate embeddings in batches
            embeddings = await self.embedder.embed_text(texts, batch_size)
            
            # Prepare vectors for upsert
            vectors = []
            for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
                vector = {
                    'id': f'chunk_{i}',
                    'values': embedding,
                    'metadata': {
                        'text': chunk['text'],
                        'chapter': chunk.get('chapter'),
                        'source': chunk.get('source'),
                        'chunk_id': chunk.get('chunk_id', i)
                    }
                }
                vectors.append(vector)
            
            # Upsert vectors in batches
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
                logger.info(f"Indexed batch {i//batch_size + 1} of {len(vectors)//batch_size + 1}")
                
        except Exception as e:
            logger.error(f"Error indexing chunks: {e}")
            raise
    
    async def query(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Query the vector store for similar chunks.
        
        Args:
            query: The question or query text
            top_k: Number of most similar chunks to return
            
        Returns:
            List of dictionaries containing text and metadata of most similar chunks
        """
        try:
            # Generate embedding for query
            query_embedding = await self.embedder.embed_text(query)
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extract and return relevant chunks
            matched_chunks = []
            for match in results.matches:
                matched_chunks.append({
                    'text': match.metadata['text'],
                    'source': match.metadata.get('source', 'Unknown'),
                    'score': match.score,
                    'chapter': match.metadata.get('chapter')
                })
            
            return matched_chunks
            
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            raise

    async def delete_all(self) -> None:
        """Delete all vectors from the index"""
        try:
            self.index.delete(delete_all=True)
            logger.info("Deleted all vectors from index")
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            raise