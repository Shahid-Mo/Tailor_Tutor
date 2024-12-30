// static/js/subjects.js
async function loadSubjects() {
    try {
        const response = await fetch('/api/subjects');
        const subjects = await response.json();
        
        const subjectsGrid = document.getElementById('subjects-grid');
        subjects.forEach(subject => {
            const subjectCard = document.createElement('div');
            subjectCard.className = 'subject-card';
            subjectCard.innerHTML = `
                <h3>${subject.name}</h3>
                <p>${subject.grade}</p>
            `;
            subjectCard.onclick = () => window.location.href = `/chapters/${subject.id}`;
            subjectsGrid.appendChild(subjectCard);
        });
    } catch (error) {
        console.error('Error loading subjects:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadSubjects);





