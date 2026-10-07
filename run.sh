#!/usr/bin/env bash
set -e
if [ ! -x ".venv/bin/python" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env. Add your GEMINI_API_KEY, then run ./run.sh again."
  exit 0
fi
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
