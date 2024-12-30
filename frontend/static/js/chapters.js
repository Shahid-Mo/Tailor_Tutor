// static/js/chapters.js
async function loadChapters() {
    try {
        const response = await fetch(`/api/chapters/${SUBJECT_ID}`);
        const chapters = await response.json();
        
        const chaptersList = document.getElementById('chapters-list');
        chapters.forEach(chapter => {
            const chapterItem = document.createElement('div');
            chapterItem.className = 'chapter-item';
            chapterItem.innerHTML = `
                <h3>${chapter.title}</h3>
                <p>${chapter.description || 'No description available'}</p>
            `;
            chapterItem.onclick = () => window.location.href = `/chapter/${chapter.id}`;
            chaptersList.appendChild(chapterItem);
        });
    } catch (error) {
        console.error('Error loading chapters:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadChapters);