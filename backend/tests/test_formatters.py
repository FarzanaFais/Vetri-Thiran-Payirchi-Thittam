from backend.services.document_formatter import (
    format_docx,
    format_html_preview,
    format_pdf,
    format_txt,
    sanitize_text,
)


TEXT = """
FREELANCE WORK CONTRACT

PARTIES

Jane Doe (Freelancer),
TechNova Inc. (Client)

TERMS AND CONDITIONS

Payment within 30 days.
Confidentiality applies.
"""


def test_sanitize_text():

    result = sanitize_text(
        "“Hello”—world…"
    )

    assert result == (
        '"Hello"-world...'
    )


def test_txt():

    data = format_txt(
        TEXT
    )

    assert (
        b"FREELANCE"
        in data
    )


def test_docx():

    data = format_docx(
        TEXT,
        "Freelance Work Contract",
        None,
        "LegalEase",
    )

    assert data[:2] == b"PK"


def test_pdf():

    data = format_pdf(
        TEXT,
        "Freelance Work Contract",
        None,
        "LegalEase",
    )

    assert data.startswith(
        b"%PDF"
    )


def test_html_preview():

    html = format_html_preview(
        TEXT
    )

    assert (
        "FREELANCE WORK CONTRACT"
        in html
    )