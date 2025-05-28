from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .ai import generate_text

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(request: PromptRequest):
    try:
        response = generate_text(request.prompt)
        return {"result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
