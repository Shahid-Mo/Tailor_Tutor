# scripts/test_rag.py
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
import os
from app.services.rag import RAGPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_rag_pipeline():
    """Test the RAG pipeline with a few sample questions."""
    try:
        # Load environment variables from .env
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)
        
        # Create config dict from environment variables
        config = {
            "pinecone_api_key": os.getenv("PINECONE_API_KEY"),
            "pinecone_environment": os.getenv("PINECONE_ENVIRONMENT"),
            "pinecone_index_name": os.getenv("PINECONE_INDEX_NAME"),
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "groq_api_key": os.getenv("GROQ_API_KEY")
        }
        
        # Validate environment variables
        missing_vars = [k for k, v in config.items() if not v]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Initialize RAG pipeline
        pipeline = RAGPipeline(config)
        
        # Test questions related to class 10 science
        test_questions = [
            "What happens in Reflex Actions?",
            "What happens when light enters from one transparent medium to another?",
            "What is the direction of magnetic field at a point directly below it",
            # Add more test questions relevant to your content
        ]
        
        logger.info("Starting RAG pipeline test...")
        
        for question in test_questions:
            logger.info(f"\nTesting question: {question}")
            
            # Get answer
            result = await pipeline.answer_question(question)
            
            # Log results
            logger.info("Answer received:")
            logger.info(f"Answer: {result['answer']}")
            logger.info("Sources used:")
            for source in result['sources']:
                logger.info(f"- {source}")
            
            logger.info("-" * 80)  # Separator line
            
            # Optional: add a small delay between questions
            await asyncio.sleep(1)
        
        logger.info("RAG pipeline test completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during RAG pipeline test: {e}")
        raise

def main():
    # Run test
    asyncio.run(test_rag_pipeline())

if __name__ == "__main__":
    main()