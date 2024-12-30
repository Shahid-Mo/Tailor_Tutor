// static/js/ask.js
async function askQuestion() {
    const questionInput = document.getElementById('question');
    const answerContainer = document.getElementById('answer');
    const question = questionInput.value.trim();
    
    if (!question) {
        answerContainer.innerHTML = '<p class="error">Please enter a question.</p>';
        return;
    }

    answerContainer.innerHTML = '<p>Getting answer...</p>';
    
    try {
        const response = await fetch('/api/tutor/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        });
        
        const result = await response.json();
        
        answerContainer.innerHTML = `
            <h3>Answer:</h3>
            <p>${result.answer}</p>
            ${result.sources ? `
                <div class="sources">
                    <small>Sources: ${result.sources.join(', ')}</small>
                </div>
            ` : ''}
        `;
    } catch (error) {
        answerContainer.innerHTML = '<p class="error">Failed to get answer. Please try again.</p>';
    }
}