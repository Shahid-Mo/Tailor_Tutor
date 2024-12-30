// main.js
let currentSubject = null;
let currentChapter = null;

// Show/hide sections
function showSection(sectionId) {
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('hidden');
    });
    
    document.getElementById(sectionId).classList.remove('hidden');
    
    // Update navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    const activeButton = document.querySelector(`button[onclick="showSection('${sectionId}')"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

// Handle subject selection
async function selectSubject(subjectId) {
    currentSubject = subjectId;
    try {
        const chapters = await fetchChapters(subjectId);
        displayChapters(chapters);
    } catch (error) {
        console.error('Error selecting subject:', error);
        // Show error message to user
        const chapterList = document.getElementById('chapter-list');
        chapterList.innerHTML = '<p class="error">Failed to load chapters. Please try again.</p>';
    }
}

// Display chapters
function displayChapters(chapters) {
    const chapterList = document.getElementById('chapter-list');
    chapterList.innerHTML = '';
    chapterList.classList.remove('hidden');

    if (chapters.length === 0) {
        chapterList.innerHTML = '<p>No chapters available for this subject.</p>';
        return;
    }

    chapters.forEach(chapter => {
        const chapterElement = document.createElement('div');
        chapterElement.className = 'chapter-item';
        chapterElement.innerHTML = `
            <h3>${chapter.title}</h3>
            <p>${chapter.description || 'No description available'}</p>
        `;
        chapterElement.onclick = () => startChapter(chapter.id);
        chapterList.appendChild(chapterElement);
    });
}

// Start chapter learning
function startChapter(chapterId) {
    window.location.href = `./chapter.html?id=${chapterId}`;
}

// Handle questions in open book section
async function askQuestion() {
    const questionInput = document.getElementById('question');
    const answerContainer = document.getElementById('answer');
    const question = questionInput.value.trim();
    
    if (!question) {
        answerContainer.innerHTML = '<p class="error">Please enter a question.</p>';
        return;
    }

    // Show loading state
    answerContainer.innerHTML = '<p>Getting answer...</p>';
    
    try {
        const response = await askQuestion(question);
        if (response) {
            answerContainer.innerHTML = `
                <h3>Answer:</h3>
                <p>${response.answer}</p>
                ${response.sources ? `
                    <div class="sources">
                        <small>Sources: ${response.sources.join(', ')}</small>
                    </div>
                ` : ''}
            `;
        } else {
            throw new Error('No response received');
        }
    } catch (error) {
        answerContainer.innerHTML = '<p class="error">Failed to get answer. Please try again.</p>';
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch initial subjects
        const subjects = await fetchSubjects();
        // You can use this to populate dynamic subject cards if needed
        
        // Add error handling for nav buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (!e.target.getAttribute('onclick')) {
                    console.error('Navigation button missing onclick attribute');
                }
            });
        });
    } catch (error) {
        console.error('Error initializing page:', error);
    }
});