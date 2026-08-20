import re


COMMON_SYMPTOMS = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "weakness",
    "nausea",
    "vomiting",
    "diarrhea",
    "dizziness",
    "chest pain",
    "shortness of breath",
    "sore throat",
    "runny nose",
    "body pain",
    "abdominal pain",
]


def extract_symptoms(text: str) -> list[str]:
    """
    Extract recognized symptoms from a text description.

    This is an initial rule-based research prototype.
    It does not provide a medical diagnosis.
    """

    normalized_text = text.lower()
    normalized_text = re.sub(r"\s+", " ", normalized_text).strip()

    detected_symptoms = []

    for symptom in COMMON_SYMPTOMS:
        if symptom in normalized_text:
            detected_symptoms.append(symptom)

    return detected_symptoms