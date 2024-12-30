// UI State Management
let currentSubject = null;
let currentChapter = null;

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.remove('hidden');
    
    // Update navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

async function selectSubject(subjectId) {
    currentSubject = subjectId;
    const chapters = await fetchChapters(subjectId);
    displayChapters(chapters);
}

function displayChapters(chapters) {
    const chapterList = document.getElementById('chapter-list');
    chapterList.innerHTML = '';
    chapterList.classList.remove('hidden');

    chapters.forEach(chapter => {
        const chapterElement = document.createElement('div');
        chapterElement.className = 'chapter-item';
        chapterElement.innerHTML = `
            <h3>${chapter.title}</h3>
            <p>${chapter.description}</p>
        `;
        chapterElement.onclick = () => startChapter(chapter.id);
        chapterList.appendChild(chapterElement);
    });
}

function startChapter(chapterId) {
    window.location.href = `./chapter.html?id=${chapterId}`;
}

async function askQuestion() {
    const questionInput = document.getElementById('question');
    const answerContainer = document.getElementById('answer');
    
    const response = await askQuestion(questionInput.value);
    if (response) {
        answerContainer.innerHTML = `
            <h3>Answer:</h3>
            <p>${response.answer}</p>
            <div class="sources">
                <small>Sources: ${response.sources.join(', ')}</small>
            </div>
        `;
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Any initialization code
});