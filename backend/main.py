from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class QueryRequest(BaseModel):
    subject: str
    question: str

class QuizRequest(BaseModel):
    subject: str
    num_questions: int = 5

@app.post("/explain")
def explain_topic(req: QueryRequest):
    prompt = f"Explain the following {req.subject} concept or question for IIT JEE in detail with examples and step-by-step reasoning: {req.question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message['content'].strip()
    return {"answer": answer}

@app.post("/quiz")
def quiz(req: QuizRequest):
    import json
    prompt = f"Generate {req.num_questions} multiple-choice questions with 4 options and answers for {req.subject} at IIT JEE level. Format as JSON."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message['content'].strip()
    # Try to parse JSON
    try:
        quiz_json = json.loads(answer)
        return {"quiz": quiz_json}
    except Exception:
        return {"quiz": answer}

# Voice endpoints can be added here later for Whisper and TTS integration
