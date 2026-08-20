from src.symptom_analyzer.analyzer import extract_symptoms


def test_extract_common_symptoms():
    text = "I have fever, cough and headache."

    result = extract_symptoms(text)

    assert "fever" in result
    assert "cough" in result
    assert "headache" in result


def test_extract_synonyms():
    text = "My head hurts and I feel exhausted."

    result = extract_symptoms(text)

    assert "headache" in result
    assert "fatigue" in result


def test_extract_multiple_symptoms():
    text = "I have fever, chest pain and difficulty breathing."

    result = extract_symptoms(text)

    assert "fever" in result
    assert "chest pain" in result
    assert "shortness of breath" in result


def test_negation():
    text = "I don't have fever or headache."

    result = extract_symptoms(text)

    assert "fever" not in result
    assert "headache" not in result


def test_no_symptoms_detected():
    text = "I feel completely normal today."

    result = extract_symptoms(text)

    assert result == []


def test_empty_input():
    result = extract_symptoms("")

    assert result == []
    