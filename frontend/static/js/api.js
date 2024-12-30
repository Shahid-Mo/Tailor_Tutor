// api.js
const API_URL = 'http://localhost:8000/api';

async function fetchSubjects() {
    try {
        const response = await fetch(`${API_URL}/subjects`);
        if (!response.ok) {
            throw new Error('Failed to fetch subjects');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching subjects:', error);
        return [];
    }
}

async function fetchChapters(subjectId) {
    try {
        const response = await fetch(`${API_URL}/chapters/${subjectId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch chapters');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching chapters:', error);
        return [];
    }
}

async function fetchTopicContent(topicId) {
    try {
        const response = await fetch(`${API_URL}/topic/${topicId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch topic content');
        }
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
            body: JSON.stringify({ 
                question: question,
                context: context 
            }),
        });
        if (!response.ok) {
            throw new Error('Failed to get answer');
        }
        return await response.json();
    } catch (error) {
        console.error('Error asking question:', error);
        return null;
    }
}