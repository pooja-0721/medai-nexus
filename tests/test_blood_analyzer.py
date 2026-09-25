from src.blood_analyzer.analyzer import analyze_blood_report


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