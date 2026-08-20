import re


SYMPTOM_PATTERNS = {
    "fever": [
        "fever",
        "high temperature",
        "running a temperature",
    ],
    "cough": [
        "cough",
        "coughing",
    ],
    "headache": [
        "headache",
        "head pain",
        "my head hurts",
        "head is hurting",
    ],
    "fatigue": [
        "fatigue",
        "extremely tired",
        "very tired",
        "feeling tired",
        "exhausted",
    ],
    "weakness": [
        "weakness",
        "feeling weak",
        "very weak",
    ],
    "nausea": [
        "nausea",
        "feeling nauseous",
        "feel nauseous",
    ],
    "vomiting": [
        "vomiting",
        "throwing up",
        "threw up",
    ],
    "diarrhea": [
        "diarrhea",
        "loose motion",
        "loose motions",
    ],
    "dizziness": [
        "dizziness",
        "dizzy",
        "feeling dizzy",
    ],
    "chest pain": [
        "chest pain",
        "pain in my chest",
    ],
    "shortness of breath": [
        "shortness of breath",
        "difficulty breathing",
        "trouble breathing",
        "breathing difficulty",
    ],
    "sore throat": [
        "sore throat",
        "throat pain",
        "painful throat",
    ],
    "runny nose": [
        "runny nose",
        "nose is running",
    ],
    "body pain": [
        "body pain",
        "body aches",
        "body ache",
    ],
    "abdominal pain": [
        "abdominal pain",
        "stomach pain",
        "pain in my stomach",
    ],
}


NEGATION_PATTERNS = [
    "no",
    "not",
    "don't",
    "do not",
    "doesn't",
    "does not",
    "without",
    "never",
]


def normalize_text(text: str) -> str:
    """Normalize user-provided symptom text."""

    text = text.lower()
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_negated(text: str, symptom_phrase: str) -> bool:
    """
    Perform basic local negation detection.

    This is a simple baseline and is not a clinical NLP system.
    """

    symptom_position = text.find(symptom_phrase)

    if symptom_position == -1:
        return False

    preceding_text = text[max(0, symptom_position - 30):symptom_position]

    return any(
        re.search(
            rf"\b{re.escape(negation)}\b",
            preceding_text,
        )
        for negation in NEGATION_PATTERNS
    )


def extract_symptoms(text: str) -> list[str]:
    """
    Extract symptoms from a natural-language description.

    This is a rule-based NLP baseline for research purposes.
    It does not provide medical diagnosis or treatment advice.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    normalized_text = normalize_text(text)

    detected_symptoms = []

    for symptom, patterns in SYMPTOM_PATTERNS.items():

        for pattern in patterns:

            normalized_pattern = normalize_text(pattern)

            if normalized_pattern in normalized_text:

                if not is_negated(
                    normalized_text,
                    normalized_pattern,
                ):
                    detected_symptoms.append(symptom)

                break

    return detected_symptoms