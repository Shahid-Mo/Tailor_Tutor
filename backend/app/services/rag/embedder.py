# app/services/rag/embedder.py
from typing import List, Union
import numpy as np
from openai import AsyncOpenAI  # Note the AsyncOpenAI import
import logging

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    # app/services/rag/embedder.py
    async def embed_text(self, text: Union[str, List[str]], batch_size: int = 100) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for a single text or list of texts.
        Handles batching automatically for large lists.
        """
        try:
            # Convert single string to list
            if isinstance(text, str):
                text = [text]
                
            all_embeddings = []
            # Process in batches
            for i in range(0, len(text), batch_size):
                batch = text[i:i + batch_size]
                response = await self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)
                
            return all_embeddings[0] if len(all_embeddings) == 1 else all_embeddings
                
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
            
            
