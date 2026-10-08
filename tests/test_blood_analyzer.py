from src.blood_analyzer.analyzer import (
    analyze_blood_report,
    analyze_blood_report_text,
)
from src.blood_analyzer.parser import parse_blood_report
from src.blood_analyzer.pdf_extractor import extract_text_from_pdf


def test_standard_test_name():
    result = analyze_blood_report({
        "hemoglobin": 13.5
    })

    assert result["hemoglobin"]["status"] == "within_reference_range"


def test_hemoglobin_alias():
    result = analyze_blood_report({
        "Hb": 13.5
    })

    assert result["hemoglobin"]["status"] == "within_reference_range"


def test_wbc_alias():
    result = analyze_blood_report({
        "WBC Count": 8000
    })

    assert result["wbc"]["status"] == "within_reference_range"


def test_platelet_alias():
    result = analyze_blood_report({
        "PLT": 250000
    })

    assert result["platelets"]["status"] == "within_reference_range"


def test_glucose_alias():
    result = analyze_blood_report({
        "FBS": 90
    })

    assert result["glucose"]["status"] == "within_reference_range"


def test_abnormal_value():
    result = analyze_blood_report({
        "glucose": 110
    })

    assert result["glucose"]["status"] == "above_reference_range"


def test_unsupported_test():
    result = analyze_blood_report({
        "vitamin_d": 25
    })

    assert result["vitamin_d"]["status"] == "unsupported_test"
def test_parse_hemoglobin():
    text = "Hemoglobin: 13.5 g/dL"

    result = parse_blood_report(text)

    assert result["hemoglobin"] == 13.5


def test_parse_multiple_parameters():
    text = """
    Hemoglobin: 13.5 g/dL
    WBC Count: 8000 cells/µL
    Platelets: 250000 cells/µL
    Fasting Blood Sugar: 90 mg/dL
    """

    result = parse_blood_report(text)

    assert result["hemoglobin"] == 13.5
    assert result["wbc"] == 8000
    assert result["platelets"] == 250000
    assert result["glucose"] == 90


def test_parse_aliases():
    text = """
    Hb: 12.5 g/dL
    PLT: 300000 cells/µL
    FBS: 95 mg/dL
    """

    result = parse_blood_report(text)

    assert result["hemoglobin"] == 12.5
    assert result["platelets"] == 300000
    assert result["glucose"] == 95


def test_parse_empty_report():
    result = parse_blood_report("No blood test information available.")

    assert result == {}    
def test_analyze_blood_report_text():
    text = """
    Hemoglobin: 13.5 g/dL
    WBC Count: 8000 cells/µL
    Fasting Blood Sugar: 110 mg/dL
    """

    result = analyze_blood_report_text(text)

    assert result["hemoglobin"]["status"] == "within_reference_range"
    assert result["wbc"]["status"] == "within_reference_range"
    assert result["glucose"]["status"] == "above_reference_range" 
def test_pdf_file_not_found():
    import pytest

    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("nonexistent_report.pdf")


def test_pdf_invalid_extension():
    import pytest

    with pytest.raises(ValueError):
        extract_text_from_pdf("report.txt")   

def test_pdf_to_blood_analysis():
    from src.blood_analyzer.pdf_extractor import extract_text_from_pdf
    from src.blood_analyzer.parser import parse_blood_report
    from src.blood_analyzer.analyzer import analyze_blood_report

    text = extract_text_from_pdf("data/sample_blood_report.pdf")

    extracted = parse_blood_report(text)

    result = analyze_blood_report(extracted)

    assert result["hemoglobin"]["status"] == "within_reference_range"
    assert result["wbc"]["status"] == "within_reference_range"
    assert result["platelets"]["status"] == "within_reference_range"
    assert result["glucose"]["status"] == "above_reference_range"            