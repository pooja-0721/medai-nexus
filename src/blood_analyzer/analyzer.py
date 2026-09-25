from typing import Any


REFERENCE_RANGES = {
    "hemoglobin": {
        "unit": "g/dL",
        "min": 12.0,
        "max": 16.0,
    },
    "wbc": {
        "unit": "cells/µL",
        "min": 4000,
        "max": 11000,
    },
    "platelets": {
        "unit": "cells/µL",
        "min": 150000,
        "max": 450000,
    },
    "glucose": {
        "unit": "mg/dL",
        "min": 70,
        "max": 99,
    },
}


def analyze_blood_report(
    report: dict[str, float],
) -> dict[str, Any]:
    """
    Compare blood-report values against configured reference ranges.

    This is a research prototype and does not provide a medical diagnosis.
    Reference ranges are configurable and may vary by laboratory,
    patient characteristics, and clinical context.
    """

    results = {}

    for test_name, value in report.items():

        test_key = test_name.lower().strip()

        if test_key not in REFERENCE_RANGES:
            results[test_key] = {
                "value": value,
                "status": "unsupported_test",
                "message": "Reference range not configured.",
            }
            continue

        reference = REFERENCE_RANGES[test_key]

        if value < reference["min"]:
            status = "below_reference_range"
        elif value > reference["max"]:
            status = "above_reference_range"
        else:
            status = "within_reference_range"

        results[test_key] = {
            "value": value,
            "unit": reference["unit"],
            "reference_range": [
                reference["min"],
                reference["max"],
            ],
            "status": status,
        }

    return results