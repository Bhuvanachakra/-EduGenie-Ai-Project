import os

from gemini_service import get_gemini_service


def _explain_with_gemini(topic: str) -> str:
    prompt = f"""Explain the concept "{topic}" to a school or college student.
Start with a one-sentence definition, then explain it in simple language.
Use a small example or analogy when useful. Keep the response structured and concise.
Do not assume advanced prior knowledge.
"""
    return get_gemini_service().generate(prompt, temperature=0.4, max_output_tokens=1000)


def explain_topic(topic: str) -> str:
    # The supplied documentation describes LaMini-Flan-T5 as the local explanation
    # model. It is optional because installing its ML stack can be very large.
    # Set USE_LOCAL_EXPLANATION=true and install the optional dependencies to use it.
    if os.getenv("USE_LOCAL_EXPLANATION", "false").lower() != "true":
        return _explain_with_gemini(topic)

    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        import torch

        model_name = os.getenv(
            "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        inputs = tokenizer(
            f"Explain the concept of '{topic}' in simple language for a student.",
            return_tensors="pt",
            truncation=True,
        )
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=180)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires transformers and torch. "
            "Set USE_LOCAL_EXPLANATION=false to use Gemini instead."
        ) from exc
