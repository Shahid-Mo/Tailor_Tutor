# app/services/rag/__init__.py
from .text_processor import TextProcessor
from .embedder import Embedder
from .vector_store import VectorStore
from .answer_generator import AnswerGenerator
from typing import Dict
from pathlib import Path

class RAGPipeline:
    def __init__(self, config: Dict):
        self.text_processor = TextProcessor()
        self.vector_store = VectorStore(
            api_key=config["pinecone_api_key"],
            environment=config["pinecone_environment"],
            openai_api_key= config['openai_api_key'],  
        )
        self.answer_generator = AnswerGenerator(openai_api_key=config["openai_api_key"], groq_api_key = config["groq_api_key"])
    
    async def index_directory(self, directory: Path) -> None:
        """Index all documents in a directory."""
        chunks = await self.text_processor.process_directory(directory)
        await self.vector_store.index_chunks(chunks)
    
    async def answer_question(self, question: str) -> Dict:
        """Process a question and return an answer with sources."""
        contexts = await self.vector_store.query(question)
        print(contexts)## Just for debug 
        return await self.answer_generator.generate_answer(question, contexts)