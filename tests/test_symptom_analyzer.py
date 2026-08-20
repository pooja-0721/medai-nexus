from src.symptom_analyzer.analyzer import extract_symptoms


def test_extract_common_symptoms():
    text = "I have fever, cough and headache."

    result = extract_symptoms(text)

    assert "fever" in result
    assert "cough" in result
    assert "headache" in result


def test_extract_multiple_symptoms():
    text = "I have fever, chest pain and shortness of breath."

    result = extract_symptoms(text)

    assert "fever" in result
    assert "chest pain" in result
    assert "shortness of breath" in result


def test_no_symptoms_detected():
    text = "I feel completely normal today."

    result = extract_symptoms(text)

    assert result == []