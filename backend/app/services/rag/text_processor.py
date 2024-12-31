# app/services/rag/text_processor.py
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def process_document(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Process a document into chunks with metadata.
        
        Args:
            text: The document text to process
            metadata: Metadata about the document (e.g., chapter number, source)
            
        Returns:
            List of dictionaries containing chunks and their metadata
        """
        try:
            chunks = self.text_splitter.split_text(text)
            return [{"text": chunk, "chunk_id": i, **metadata} 
                   for i, chunk in enumerate(chunks)]
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise

    async def process_directory(self, directory: Path) -> List[Dict]:
        """
        Process all text files in a directory.
        
        Args:
            directory: Path to directory containing text files
            
        Returns:
            List of all chunks with metadata
        """
        all_chunks = []
        try:
            for file_path in directory.glob("*.txt"):
                chapter_num = int(file_path.stem.split("_")[1])
                text = file_path.read_text()
                
                metadata = {
                    "chapter": chapter_num,
                    "source": file_path.name
                }
                
                chunks = self.process_document(text, metadata)
                all_chunks.extend(chunks)
                
            return all_chunks
        except Exception as e:
            logger.error(f"Error processing directory {directory}: {e}")
            raise






