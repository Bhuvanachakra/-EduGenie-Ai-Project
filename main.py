from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from schemas import LearningResponse, QuizResponse, TextRequest, TopicRequest
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(request=request,name="index.html")


@app.get("/health")
async def health():
    from gemini_service import get_gemini_service

    service = get_gemini_service()
    return {
        "status": "ok",
        "gemini_configured": service.configured,
        "model": service.model,
    }


@app.get("/qa")
async def qa(question: str = Query(..., min_length=1, max_length=5000)):
    try:
        return {"answer": answer_question_with_gemini(question)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/explain")
async def explain(request: TopicRequest):
    try:
        return {"topic": request.topic, "explanation": explain_topic(request.topic)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        return {"summary": summarize_text(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):
    try:
        return {"quiz": generate_quiz(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/learn/recommendations", response_model=LearningResponse)
async def learning_recommendations(
    topic: str = Query(..., min_length=1, max_length=500)
):
    try:
        return {
            "topic": topic,
            "recommendations": get_learning_recommendations(topic),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.exception_handler(Exception)
async def unhandled_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Unexpected server error.", "error": str(exc)},
    )
