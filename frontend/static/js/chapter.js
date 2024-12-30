// static/js/chapter.js
let currentTopicIndex = 0;
let topics = [];

async function initChapter() {
    try {
        const response = await fetch(`/api/chapter/${CHAPTER_ID}`);
        const chapterData = await response.json();
        
        document.getElementById('chapter-title').textContent = chapterData.title;
        topics = chapterData.topics;
        
        if (topics.length > 0) {
            displayTopic(0);
        } else {
            showError('No topics available in this chapter');
        }
        
        updateNavigation();
    } catch (error) {
        console.error('Error initializing chapter:', error);
        showError('Failed to load chapter content');
    }
}

async function displayTopic(index) {
    if (index < 0 || index >= topics.length) {
        return;
    }

    try {
        const response = await fetch(`/api/topic/${topics[index].id}`);
        const topicContent = await response.json();
        const contentArea = document.getElementById('content-area');
        
        contentArea.innerHTML = `
            <h2>${topicContent.title}</h2>
            <div class="topic-content">
                ${topicContent.content}
            </div>
        `;

        updateProgress(index);
        currentTopicIndex = index;
        updateNavigation();
    } catch (error) {
        console.error('Error displaying topic:', error);
        showError('Failed to load topic content');
    }
}

function nextTopic() {
    if (currentTopicIndex < topics.length - 1) {
        displayTopic(currentTopicIndex + 1);
    }
}

function previousTopic() {
    if (currentTopicIndex > 0) {
        displayTopic(currentTopicIndex - 1);
    }
}

function updateProgress(index) {
    const progress = ((index + 1) / topics.length) * 100;
    document.getElementById('progress').style.width = `${progress}%`;
}

function updateNavigation() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    prevBtn.disabled = currentTopicIndex === 0;
    nextBtn.disabled = currentTopicIndex === topics.length - 1;
}

function showError(message) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="error-message">${message}</div>`;
}

async function askTopicQuestion() {
    const questionContainer = document.getElementById('questions-container');
    const textarea = questionContainer.querySelector('textarea');
    const question = textarea.value.trim();
    
    if (!question) {
        return;
    }

    try {
        const response = await fetch('/api/tutor/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                context: {
                    chapterId: CHAPTER_ID,
                    topicId: topics[currentTopicIndex].id
                }
            }),
        });
        
        const result = await response.json();
        
        const answerElement = document.createElement('div');
        answerElement.className = 'answer';
        answerElement.innerHTML = `
            <p><strong>Q: </strong>${question}</p>
            <p><strong>A: </strong>${result.answer}</p>
        `;
        
        questionContainer.appendChild(answerElement);
        textarea.value = '';
    } catch (error) {
        console.error('Error asking question:', error);
        showError('Failed to get answer');
    }
}

document.addEventListener('DOMContentLoaded', initChapter);