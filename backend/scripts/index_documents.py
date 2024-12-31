# scripts/index_documents.py
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
import os
from app.services.rag import RAGPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def index_documents(data_dir: Path, clear_existing: bool = True):
    """Index all documents in the specified directory using RAG pipeline."""
    try:
        # Load environment variables from .env
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)
        
        
        
        
        # Create config dict from environment variables
        config = {
            "pinecone_api_key": os.getenv("PINECONE_API_KEY"),
            "pinecone_environment": os.getenv("PINECONE_ENVIRONMENT"),
            "pinecone_index_name": os.getenv("PINECONE_INDEX_NAME"),
            "openai_api_key": os.getenv("OPENAI_API_KEY")
        }
        
        
        
        # Validate environment variables
        missing_vars = [k for k, v in config.items() if not v]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Initialize RAG pipeline
        pipeline = RAGPipeline(config)
        
        if clear_existing:
            # First clear existing vectors (optional)
            logger.info("Clearing existing vectors...")
            await pipeline.vector_store.delete_all()
        
        # Index all documents
        logger.info(f"Starting indexing of documents in {data_dir}...")
        await pipeline.index_directory(data_dir)
        
        logger.info("Indexing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during indexing: {e}")
        raise

def main():
    # Define data directory path
    data_dir = Path(__file__).parent.parent / "data/raw/class_10_science"
    
    # Ensure path exists
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found at {data_dir}")
    
    # Run indexing
    asyncio.run(index_documents(data_dir))

if __name__ == "__main__":
    main()