# LegalEase

LegalEase is an AI-assisted legal document drafting application.

It uses:

- FastAPI
- Streamlit
- Google Gemini
- Python
- python-docx
- FPDF2

The application can generate editable legal-document drafts and export
them to:

- TXT
- DOCX
- PDF

---

# Architecture

Streamlit Frontend
        |
        v
FastAPI Backend
        |
        v
Gemini AI
        |
        v
Generated Legal Draft
        |
        +----> Editable Preview
        |
        +----> TXT
        |
        +----> DOCX
        |
        +----> PDF

---

# Requirements

Python 3.10 or newer.

Python 3.12 is recommended.

---

# Installation

Create a virtual environment.

Windows:

    python -m venv .venv

Activate it:

    .venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

---

# Environment

Copy:

    .env.example

to:

    .env

For initial testing use:

    MOCK_AI=true

This allows LegalEase to work without a Gemini API key.

---

# Start Backend

Run:

    python run_backend.py

The backend will be available at:

    http://127.0.0.1:8000

Swagger API documentation:

    http://127.0.0.1:8000/docs

Health endpoint:

    http://127.0.0.1:8000/health

---

# Start Frontend

Open another terminal.

Activate the virtual environment.

Run:

    python run_frontend.py

Open:

    http://localhost:8501

---

# Gemini

After testing the application locally, add your Gemini API key
to .env:

    GEMINI_API_KEY=YOUR_API_KEY

Then set:

    MOCK_AI=false

The model can be configured with:

    GEMINI_MODEL=gemini-3.8-flash

---

# Testing

Run:

    python -m pytest -q

Tests cover:

- FastAPI root endpoint
- FastAPI health endpoint
- Document generation
- Mock AI mode
- TXT export
- DOCX export
- PDF export
- HTML preview

---

# Legal Disclaimer

LegalEase generates AI-assisted legal-document drafts.

It does not provide legal advice.

Users should verify:

- names
- dates
- amounts
- obligations
- jurisdiction
- governing law
- signatures
- applicable legal requirements

Consult a qualified legal professional where appropriate.

---

# Security

Never commit your .env file.

Do not expose Gemini API keys in Streamlit code.

Use HTTPS before production deployment.

Add authentication and rate limiting before exposing
the application publicly.