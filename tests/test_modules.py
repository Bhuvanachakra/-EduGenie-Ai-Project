from quiz_module import _clean_json, _validate_quiz


def test_clean_json_code_fence():
    raw = '```json\n[{"question":"x","options":["a","b","c","d"],"answer":"a"}]\n```'
    assert _clean_json(raw).startswith("[")


def test_validate_quiz_accepts_valid_data():
    data = [
        {"question": "2+2?", "options": ["1", "2", "3", "4"], "answer": "4"},
        {"question": "Capital of France?", "options": ["Paris", "Rome", "Berlin", "Madrid"], "answer": "Paris"},
        {"question": "Water formula?", "options": ["CO2", "H2O", "O2", "NaCl"], "answer": "H2O"},
    ]
    assert len(_validate_quiz(data)) == 3


def test_validate_quiz_rejects_too_few():
    import pytest
    with pytest.raises(ValueError):
        _validate_quiz([])
