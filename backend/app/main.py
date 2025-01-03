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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the frontend directory
FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"

# Initialize RAG pipeline
rag_pipeline = RAGPipeline(rag_config)

# Dependency to get RAG pipeline instance
async def get_rag_pipeline():
    return rag_pipeline

# Mount static files
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# Sample data - This should eventually move to a database or separate data file
subjects_data = {
    "science": {
        "id": "science",
        "name": "Science",
        "grade": "Class 10",
        "chapters": [
            {
                "id": "ch1",
                "title": "Chemical Reactions",
                "description": "Learn about different types of chemical reactions",
                "topics": [
                    {
                        "id": "topic1",
                        "title": "Introduction to Chemical Reactions",
                        "content": "A chemical reaction is a process that leads to the chemical transformation of one set of chemical substances to another."
                    },
                    {
                        "id": "topic2",
                        "title": "Types of Chemical Reactions",
                        "content": "Chemical reactions can be classified into several types including combination, decomposition, displacement, and double displacement."
                    }
                ]
            }
        ]
    },
    "social": {
        "id": "social",
        "name": "Social Science",
        "grade": "Class 10",
        "chapters": [
            {
                "id": "ch2",
                "title": "Indian National Movement",
                "description": "Study the history of Indian independence movement",
                "topics": [
                    {
                        "id": "topic3",
                        "title": "Early Nationalist Movements",
                        "content": "The early nationalist movements in India laid the foundation for the independence struggle."
                    }
                ]
            }
        ]
    }
}

# Frontend routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/subjects", response_class=HTMLResponse)
async def read_subjects(request: Request):
    return templates.TemplateResponse("subjects.html", {"request": request})

@app.get("/chapters/{subject_id}", response_class=HTMLResponse)
async def read_chapters(request: Request, subject_id: str):
    if subject_id not in subjects_data:
        raise HTTPException(status_code=404, detail="Subject not found")
    return templates.TemplateResponse("chapters.html", {
        "request": request,
        "subject_id": subject_id,
        "subject_name": subjects_data[subject_id]["name"]
    })

@app.get("/chapter/{chapter_id}", response_class=HTMLResponse)
async def read_chapter(request: Request, chapter_id: str):
    return templates.TemplateResponse("chapter.html", {"request": request, "chapter_id": chapter_id})

@app.get("/ask", response_class=HTMLResponse)
async def read_ask(request: Request):
    return templates.TemplateResponse("ask.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def read_quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

# API routes
@app.get("/api/subjects")
async def get_subjects():
    return [
        {"id": subject_id, "name": data["name"], "grade": data["grade"]}
        for subject_id, data in subjects_data.items()
    ]

@app.get("/api/chapters/{subject_id}")
async def get_chapters(subject_id: str):
    if subject_id not in subjects_data:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subjects_data[subject_id]["chapters"]

@app.get("/api/chapter/{chapter_id}")
async def get_chapter(chapter_id: str):
    for subject in subjects_data.values():
        for chapter in subject["chapters"]:
            if chapter["id"] == chapter_id:
                return chapter
    raise HTTPException(status_code=404, detail="Chapter not found")

@app.get("/api/topic/{topic_id}")
async def get_topic(topic_id: str):
    for subject in subjects_data.values():
        for chapter in subject["chapters"]:
            for topic in chapter["topics"]:
                if topic["id"] == topic_id:
                    return topic
    raise HTTPException(status_code=404, detail="Topic not found")


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

