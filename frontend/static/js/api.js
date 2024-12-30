const API_URL = 'http://localhost:8000/api';

async function fetchSubjects() {
    try {
        const response = await fetch(`${API_URL}/subjects`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching subjects:', error);
        return [];
    }
}

async function fetchChapters(subjectId) {
    try {
        const response = await fetch(`${API_URL}/chapters/${subjectId}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching chapters:', error);
        return [];
    }
}

async function fetchTopicContent(topicId) {
    try {
        const response = await fetch(`${API_URL}/topic/${topicId}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching topic:', error);
        return null;
    }
}

async function askQuestion(question, context = null) {
    try {
        const response = await fetch(`${API_URL}/tutor/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question, context }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error asking question:', error);
        return null;
    }
}