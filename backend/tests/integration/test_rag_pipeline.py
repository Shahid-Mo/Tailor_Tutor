# tests/integration/test_rag_pipeline.py
import pytest
from app.services.rag import RAGPipeline

@pytest.mark.asyncio
async def test_full_rag_pipeline(sample_text, vector_store):
    pipeline = RAGPipeline(vector_store)
    
    # Index some test content
    await pipeline.index_content(sample_text, {"chapter": 1})
    
    # Test question answering
    question = "What are chemical reactions?"
    response = await pipeline.answer_question(question)
    
    assert response.answer
    assert response.sources