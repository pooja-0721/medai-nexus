from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["project"] == "MedAI-Nexus"
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_symptom_endpoint():
    response = client.post(
        "/analyze/symptoms",
        json={
            "text": "I have fever and headache"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "detected_symptoms" in data
    assert "symptom_count" in data


def test_blood_report_endpoint():
    with open(
        "data/sample_blood_report.pdf",
        "rb",
    ) as pdf_file:

        response = client.post(
            "/analyze/blood-report",
            files={
                "file": (
                    "sample_blood_report.pdf",
                    pdf_file,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "extracted_values" in data
    assert "analysis" in data

    assert data["extracted_values"]["hemoglobin"] == 13.5
    assert data["extracted_values"]["wbc"] == 8000
    assert data["extracted_values"]["platelets"] == 250000
    assert data["extracted_values"]["glucose"] == 110