// chapter.js
let currentTopicIndex = 0;
let topics = [];
let chapterId = null;

// Initialize chapter page
async function initChapterPage() {
    // Get chapter ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    chapterId = urlParams.get('id');
    
    if (!chapterId) {
        showError('No chapter specified');
        return;
    }

    try {
        // Fetch chapter content
        const response = await fetch(`${API_URL}/chapter/${chapterId}`);
        const chapterData = await response.json();
        
        // Set chapter title
        document.getElementById('chapter-title').textContent = chapterData.title;
        
        // Store topics
        topics = chapterData.topics;
        
        // Display first topic
        if (topics.length > 0) {
            displayTopic(0);
        } else {
            showError('No topics available in this chapter');
        }
        
        // Update navigation buttons
        updateNavigation();
    } catch (error) {
        console.error('Error initializing chapter:', error);
        showError('Failed to load chapter content');
    }
}

// Display topic content
async function displayTopic(index) {
    if (index < 0 || index >= topics.length) {
        return;
    }

    try {
        const topicContent = await fetchTopicContent(topics[index].id);
        const contentArea = document.getElementById('content-area');
        
        contentArea.innerHTML = `
            <h2>${topicContent.title}</h2>
            <div class="topic-content">
                ${topicContent.content}
            </div>
        `;

        // Update progress bar
        updateProgress(index);
        
        currentTopicIndex = index;
    } catch (error) {
        console.error('Error displaying topic:', error);
        showError('Failed to load topic content');
    }
}

// Navigation functions
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

// Update progress bar
function updateProgress(index) {
    const progress = ((index + 1) / topics.length) * 100;
    document.getElementById('progress').style.width = `${progress}%`;
}

// Update navigation buttons
function updateNavigation() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    prevBtn.disabled = currentTopicIndex === 0;
    nextBtn.disabled = currentTopicIndex === topics.length - 1;
}

// Show error message
function showError(message) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `<div class="error-message">${message}</div>`;
}

// Ask topic-specific question
async function askTopicQuestion() {
    const questionContainer = document.getElementById('questions-container');
    const textarea = questionContainer.querySelector('textarea');
    const question = textarea.value.trim();
    
    if (!question) {
        return;
    }

    try {
        const response = await askQuestion(question, {
            chapterId: chapterId,
            topicId: topics[currentTopicIndex].id
        });
        
        // Display answer
        const answerElement = document.createElement('div');
        answerElement.className = 'answer';
        answerElement.innerHTML = `
            <p><strong>Q: </strong>${question}</p>
            <p><strong>A: </strong>${response.answer}</p>
        `;
        
        questionContainer.appendChild(answerElement);
        textarea.value = '';
    } catch (error) {
        console.error('Error asking question:', error);
        showError('Failed to get answer');
    }
}

// Initialize page when loaded
document.addEventListener('DOMContentLoaded', initChapterPage);