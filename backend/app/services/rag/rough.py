# backend/app/main.py
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from typing import Dict
from dotenv import load_dotenv

from .models.schemas import Question, Answer
from .core.config import settings
from .services.rag import RAGPipeline

# Load environment variables
load_dotenv()

# Initialize RAG pipeline configuration
rag_config = {
    "pinecone_api_key": os.getenv("PINECONE_API_KEY"),
    "pinecone_environment": os.getenv("PINECONE_ENVIRONMENT"),
    "pinecone_index_name": os.getenv("PINECONE_INDEX_NAME"),
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "groq_api_key": os.getenv("GROQ_API_KEY")
}

app = FastAPI(title="Tailor Tutor API")

# CORS middleware configuration remains the same...

# Frontend directory configuration remains the same...

# Initialize RAG pipeline
rag_pipeline = RAGPipeline(rag_config)

# Dependency to get RAG pipeline instance
async def get_rag_pipeline():
    return rag_pipeline

# Your existing routes remain the same...

# Modified /api/tutor/ask endpoint to use RAG pipeline
@app.post("/api/tutor/ask")
async def ask_question(
    question: Question,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
):
    try:
        # Process question through RAG pipeline
        result = await pipeline.answer_question(question.question)
        
        return Answer(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

# Optional: Add an endpoint to index new content
@app.post("/api/admin/index")
async def index_content(
    directory: str,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
):
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Directory {directory} does not exist"
            )
            
        await pipeline.index_directory(dir_path)
        return {"message": f"Successfully indexed content from {directory}"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error indexing content: {str(e)}"
        )

# Optionally update your schemas.py to include more detailed models
# backend/app/models/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    question: str
    context: Optional[str] = None
    
class Answer(BaseModel):
    answer: str
    sources: List[str]
    confidence: Optional[float] = None