import json
import re

from gemini_service import get_gemini_service


def _clean_json(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _validate_quiz(data) -> list[dict]:
    if isinstance(data, dict) and "quiz" in data:
        data = data["quiz"]
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    result = []
    for item in data[:5]:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        if not question or not isinstance(options, list) or len(options) != 4 or not answer:
            continue
        options = [str(option).strip() for option in options]
        if answer not in options:
            letters = {"A": 0, "B": 1, "C": 2, "D": 3}
            if answer.upper() in letters:
                answer = options[letters[answer.upper()]]
            else:
                continue
        result.append({"question": question, "options": options, "answer": answer})

    if len(result) < 3:
        raise ValueError("Gemini returned fewer than three valid quiz questions.")
    return result[:3]


def generate_quiz(text: str) -> list[dict]:
    prompt = f"""You are an educational quiz generator.
Create exactly 3 multiple-choice questions from the passage below.

Rules:
- Each question must have exactly 4 distinct options.
- The answer must exactly match one option.
- Questions must test understanding of the supplied passage.
- Do not invent facts unrelated to the passage.
- Return ONLY valid JSON in this shape:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

PASSAGE:
{text}
"""
    raw = get_gemini_service().generate(
        prompt, temperature=0.2, max_output_tokens=1800, json_mode=True
    )
    try:
        return _validate_quiz(json.loads(_clean_json(raw)))
    except (json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"Could not parse Gemini quiz output: {exc}") from exc
