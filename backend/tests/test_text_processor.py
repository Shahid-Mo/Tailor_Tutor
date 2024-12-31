# tests/test_text_processor.py
import pytest
from app.services.rag.text_processor import TextProcessor

def test_process_document():
    processor = TextProcessor(chunk_size=100, chunk_overlap=20)
    text = "This is a test document " * 10
    metadata = {"chapter": 1, "section": "intro"}
    
    chunks = processor.process_document(text, metadata)
    
    assert len(chunks) > 0
    assert all("text" in chunk for chunk in chunks)
    assert all(chunk["chapter"] == 1 for chunk in chunks)