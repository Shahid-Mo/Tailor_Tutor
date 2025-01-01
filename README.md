# Tailor Tutor: Personalized Learning Platform

Tailor Tutor is an advanced educational platform that combines modern web technologies with AI-powered tutoring to deliver personalized learning experiences. The platform uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware responses to student questions across various subjects.

## Features

### Interactive Learning Interface
- Subject-based curriculum organization
- Chapter-wise content breakdown
- Topic-wise learning materials
- Intuitive navigation between different learning modules

### AI-Powered Tutoring
- Intelligent question-answering system using RAG pipeline
- Context-aware responses drawing from verified educational content
- Support for multiple subjects and topics
- Real-time response generation

### Flexible Architecture
- FastAPI backend for high-performance API endpoints
- Jinja2 templating for dynamic frontend rendering
- CORS support for cross-origin requests
- Modular design for easy expansion

## Technical Stack

### Backend
- FastAPI - Modern, fast web framework for building APIs
- Python 3.8+ 
- Pinecone - Vector database for efficient similarity search
- OpenAI/Groq - AI models for response generation
- Jinja2 - Template engine for frontend rendering

### Frontend
- HTML/CSS/JavaScript
- Static file serving
- Responsive templates
- Interactive UI components

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Environment Variables
Create a `.env` file in the root directory with the following variables:
```
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_index_name
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tailor-tutor.git
cd tailor-tutor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the application:
```bash
uvicorn backend.app.main:app --reload
```

The application will be available at `http://localhost:8000`

## Project Structure
```
tailor-tutor/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   └── tests/
├── frontend/
│   ├── static/
│   └── templates/
├── requirements.txt
└── README.md
```

## API Endpoints

### Frontend Routes
- `/` - Home page
- `/subjects` - Subject listing
- `/chapters/{subject_id}` - Chapter listing for a subject
- `/chapter/{chapter_id}` - Individual chapter view
- `/ask` - Question-asking interface
- `/quiz` - Quiz interface

### API Routes
- `GET /api/subjects` - Get all subjects
- `GET /api/chapters/{subject_id}` - Get chapters for a subject
- `GET /api/chapter/{chapter_id}` - Get chapter details
- `GET /api/topic/{topic_id}` - Get topic details
- `POST /api/tutor/ask` - Submit a question to the AI tutor

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI team for the excellent web framework
- OpenAI and Groq for AI capabilities
- Pinecone for vector search functionality
- All contributors who help improve this platform

## Support

For support, please open an issue in the GitHub repository or contact the maintenance team.