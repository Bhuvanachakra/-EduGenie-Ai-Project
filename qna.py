from gemini_service import get_gemini_service


def answer_question_with_gemini(question: str) -> str:
    prompt = f"""You are EduGenie, a friendly educational tutor.
Answer the student's question accurately and concisely.
Use simple language, give enough context to understand the answer, and avoid unnecessary jargon.
If the question is ambiguous, briefly state the assumption you are making.

Student question:
{question}
"""
    return get_gemini_service().generate(prompt, temperature=0.3, max_output_tokens=800)
