# EduGenie — Google Gemini Powered Learning Assistant

A complete FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied EduGenie project document.

Features:
- Question answering
- Simple concept explanations
- 3-question MCQ quiz generation
- Long-text summarization
- Beginner-to-advanced learning recommendations

The supplied document describes FastAPI endpoints `/qa`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`, plus an HTML/CSS frontend. This implementation keeps that architecture and uses Google's current `google-genai` SDK for Gemini.

## Run on Windows CMD

```bat
cd EduGenie
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Open `.env`, replace `your_gemini_api_key_here` with your Gemini API key, then:

```bat
python -m uvicorn main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Test

In another CMD window:

```bat
cd EduGenie
.venv\Scripts\activate
pytest -q
```

## API examples

```bat
curl "http://127.0.0.1:8000/qa?question=Which%20is%20the%20largest%20ocean%3F"

curl -X POST "http://127.0.0.1:8000/explain" -H "Content-Type: application/json" -d "{"topic":"Photosynthesis"}"

curl -X POST "http://127.0.0.1:8000/summarize" -H "Content-Type: application/json" -d "{"text":"The Industrial Revolution changed production through mechanization and factories."}"

curl -X POST "http://127.0.0.1:8000/quiz" -H "Content-Type: application/json" -d "{"text":"The Pythagorean theorem states that in a right triangle, a^2 + b^2 = c^2."}"

curl "http://127.0.0.1:8000/learn/recommendations?topic=SQL"
```

Never commit `.env` or expose your Gemini API key in frontend JavaScript.
