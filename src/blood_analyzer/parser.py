import re

from .analyzer import TEST_ALIASES, REFERENCE_RANGES


def parse_blood_report(text: str) -> dict[str, float]:
    """
    Extract supported blood-test values from plain-text reports.

    This is a research prototype and is not a medical diagnostic tool.
    """

    extracted = {}

    for test_name in REFERENCE_RANGES:
        names = [test_name]

        for alias, canonical_name in TEST_ALIASES.items():
            if canonical_name == test_name:
                names.append(alias)

        for name in names:
            pattern = rf"\b{re.escape(name)}\b\s*[:\-]?\s*(\d+(?:\.\d+)?)"

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                extracted[test_name] = float(match.group(1))
                break

    return extracted