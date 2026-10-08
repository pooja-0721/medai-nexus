from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF blood report.

    This is a research prototype and does not provide
    medical diagnosis or clinical interpretation.
    """

    path = Path(pdf_path)

    if path.suffix.lower() != ".pdf":
        raise ValueError("The provided file must be a PDF.")

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages).strip()