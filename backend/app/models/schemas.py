# backend/app/models/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict

class Question(BaseModel):
    question: str
    context: Optional[Dict] = None

class Answer(BaseModel):
    answer: str
    sources: List[str] = []

class Topic(BaseModel):
    id: str
    title: str
    content: str

class Chapter(BaseModel):
    id: str
    title: str
    description: str
    topics: List[Topic]

class Subject(BaseModel):
    id: str
    name: str
    grade: str
    chapters: List[Chapter]