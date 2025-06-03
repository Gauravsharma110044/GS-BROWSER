const API_URL = "http://localhost:8000";

document.getElementById('ask-btn').onclick = async () => {
    const subject = document.getElementById('subject').value;
    const question = document.getElementById('question').value;
    if (!question.trim()) return;
    document.getElementById('answer').innerText = "AI is thinking...";
    const res = await fetch(`${API_URL}/explain`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject, question})
    });
    const data = await res.json();
    document.getElementById('answer').innerText = data.answer;
};

document.getElementById('quiz-btn').onclick = async () => {
    const subject = document.getElementById('subject').value;
    document.getElementById('quiz').innerText = "Generating quiz...";
    const res = await fetch(`${API_URL}/quiz`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject, num_questions: 5})
    });
    const data = await res.json();
    let quiz = data.quiz;
    if (typeof quiz === "string") {
        try { quiz = JSON.parse(quiz); } catch {}
    }
    if (Array.isArray(quiz)) {
        let html = '';
        quiz.forEach((q, i) => {
            html += `<div class='quiz-q'><b>Q${i+1}: ${q.question}</b><ul>`;
            q.options.forEach(opt => {
                html += `<li>${opt}</li>`;
            });
            html += `</ul><i>Answer: ${q.answer}</i></div>`;
        });
        document.getElementById('quiz').innerHTML = html;
    } else {
        document.getElementById('quiz').innerText = typeof quiz === "string" ? quiz : JSON.stringify(quiz, null, 2);
    }
};

// Voice input/output hooks can be added here later
