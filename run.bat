@echo off
setlocal
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3 -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if not exist ".env" (
    copy .env.example .env >nul
    echo.
    echo Created .env. Add your GEMINI_API_KEY, save the file, then run run.bat again.
    exit /b 0
)
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
