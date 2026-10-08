from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

import os
import tempfile

from src.symptom_analyzer.analyzer import extract_symptoms
from src.blood_analyzer.pdf_extractor import extract_text_from_pdf
from src.blood_analyzer.parser import parse_blood_report
from src.blood_analyzer.analyzer import analyze_blood_report


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
@app.post("/analyze/blood-report")
async def analyze_blood_report_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported.",
            "filename": file.filename,
        }

    contents = await file.read()

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        extracted_text = extract_text_from_pdf(temp_path)

        extracted_values = parse_blood_report(extracted_text)

        results = analyze_blood_report(extracted_values)

        return {
            "filename": file.filename,
            "extracted_values": extracted_values,
            "analysis": results,
            "disclaimer": (
                "This is a research prototype and does not provide "
                "medical diagnosis or treatment advice."
            ),
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)