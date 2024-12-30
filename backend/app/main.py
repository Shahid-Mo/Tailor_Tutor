# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import json

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Topic(BaseModel):
    id: int
    title: str
    content: str
    key_points: List[str]

class Chapter(BaseModel):
    id: int
    title: str
    topics: List[Topic]

class StudentResponse(BaseModel):
    question_id: int
    answer: str

class QuizResult(BaseModel):
    score: int
    feedback: str
    next_topic_recommendation: Optional[str]

# API Endpoints
@app.get("/api/subjects")
async def get_subjects():
    return {
        "subjects": [
            {"id": "science", "name": "Science"},
            {"id": "social", "name": "Social"},
            {"id": "maths", "name": "maths"}
            # Add more subjects
        ]
    }

@app.get("/api/chapters/{subject}")
async def get_chapters(subject: str):
    # You'll load this from your database
    return {
        "chapters": [
            {
                "id": 1,
                "title": "Chemical Reactions",
                "description": "Learn about different types of chemical reactions..."
            }
            # Add more chapters
        ]
    }

@app.get("/api/chapter/{chapter_id}/topics")
async def get_chapter_topics(chapter_id: int):
    # Load topics for the chapter
    return {
        "topics": [
            {
                "id": 1,
                "title": "Introduction to Chemical Reactions",
                "estimated_time": "15 mins"
            }
            # Add more topics
        ]
    }

@app.get("/api/topic/{topic_id}")
async def get_topic_content(topic_id: int):
    # Load topic content with teaching material
    return {
        "content": "Content here...",
        "key_points": ["Point 1", "Point 2"],
        "examples": ["Example 1", "Example 2"]
    }

@app.post("/api/topic/{topic_id}/question")
async def ask_topic_question(topic_id: int, question: dict):
    # Process question within topic context
    return {
        "answer": "Answer based on topic context...",
        "related_concepts": ["concept1", "concept2"]
    }

@app.post("/api/quiz/generate/{chapter_id}")
async def generate_quiz(chapter_id: int):
    # Generate adaptive quiz based on covered topics
    return {
        "questions": [
            {
                "id": 1,
                "question": "What happens in a reduction reaction?",
                "type": "multiple_choice",
                "options": ["A", "B", "C", "D"]
            }
        ]
    }

@app.post("/api/quiz/evaluate")
async def evaluate_quiz(responses: List[StudentResponse]):
    # Evaluate quiz and provide feedback
    return {
        "score": 85,
        "feedback": "Good understanding of basic concepts...",
        "weak_areas": ["Advanced oxidation concepts"],
        "recommended_topics": ["Topic 3.2"]
    }

@app.post("/api/book/question")
async def ask_book_question(question: dict):
    # RAG-based full book Q&A
    return {
        "answer": "RAG generated answer...",
        "sources": ["Chapter 2", "Chapter 4"],
        "confidence": 0.95
    }
    
