# AI Writer Backend

- FastAPI server for AI text generation.
- Add your Gemini API key to a `.env` file in this directory:

GEMINI_API_KEY=your_api_key_here

## Run locally:
pip install -r requirements.txt
uvicorn app.main:app --reload
