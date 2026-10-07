from gemini_service import get_gemini_service


def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following educational passage.
Preserve the important facts, definitions, relationships, and conclusions.
Remove repetition and unnecessary detail.
Return a clear summary suitable for a student revising for an exam.

PASSAGE:
{text}
"""
    return get_gemini_service().generate(prompt, temperature=0.3, max_output_tokens=1200)
