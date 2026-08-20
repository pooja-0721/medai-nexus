from fastapi import FastAPI
from pydantic import BaseModel

from src.symptom_analyzer.analyzer import extract_symptoms


app = FastAPI(
    title="MedAI-Nexus",
    description="Multimodal AI research platform for medical data analysis.",
    version="0.1.0",
)


class SymptomRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "project": "MedAI-Nexus",
        "status": "running",
        "version": "0.1.0",
        "message": "MedAI-Nexus API is running successfully.",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze/symptoms")
def analyze_symptoms(request: SymptomRequest):
    symptoms = extract_symptoms(request.text)

    return {
        "input": request.text,
        "detected_symptoms": symptoms,
        "symptom_count": len(symptoms),
        "disclaimer": (
            "This is a research prototype and does not provide "
            "medical diagnosis or treatment advice."
        ),
    }