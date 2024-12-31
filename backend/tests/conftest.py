# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_text():
    return """
    This is a sample chapter about chemical reactions.
    Chemical reactions involve the transformation of substances.
    """ * 10

@pytest.fixture
def vector_store():
    # Create test index in Pinecone
    from app.services.rag.vector_store import VectorStore
    store = VectorStore(index_name="test-index")
    yield store
    # Cleanup test index after tests
    store.cleanup()