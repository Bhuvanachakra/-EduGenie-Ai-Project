from gemini_service import get_gemini_service


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""You are an AI tutor creating a personalized learning path for "{topic}".

Create a structured progression from beginner to advanced. Include:
1. Beginner level: key concepts and an estimated study time.
2. Intermediate level: topics to learn next and an estimated study time.
3. Advanced level: deeper topics and an estimated study time.
4. Recommended resources such as books, official documentation, tutorials, or practice ideas.
5. Adaptive learning tips: how to practice, how to know when to move forward, and common mistakes to avoid.

Keep recommendations practical and educational. Do not invent specific URLs.
"""
    return get_gemini_service().generate(prompt, temperature=0.5, max_output_tokens=2200)
