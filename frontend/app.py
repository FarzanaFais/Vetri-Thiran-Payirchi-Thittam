from __future__ import annotations

import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


# ==========================================
# Environment
# ==========================================

load_dotenv()


ROOT = Path(
    __file__
).resolve().parents[1]


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


LOGO = ROOT / "assets" / "logo.png"


# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# Custom CSS
# ==========================================

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 1.5rem;
}

.preview {
    background: #17191c;
    color: #f2f2f2;
    padding: 1.5rem;
    border-radius: 12px;
    max-height: 600px;
    overflow-y: auto;
    font-family: Georgia, serif;
    line-height: 1.65;
}

.preview h3 {
    color: #ffffff;
    margin-top: 1.2rem;
}

.preview p {
    margin: 0.35rem 0;
    white-space: pre-wrap;
}

.disclaimer {
    font-size: 0.82rem;
    color: #6b7280;
    line-height: 1.5;
}

.info-card {
    padding: 1rem;
    border-radius: 10px;
    background: #f3f4f6;
    margin-bottom: 1rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# Logo
# ==========================================

# Logo is optional.


# ==========================================
# Header
# ==========================================

st.markdown(
    '<div class="main-title">LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered legal document drafting '
    'and export'
    '</div>',
    unsafe_allow_html=True,
)


# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.header(
        "Document Inputs"
    )

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Custom Agreement",
        ],
    )

    if (
        document_type
        == "Custom Agreement"
    ):

        document_type = st.text_input(
            "Custom document type",
            placeholder=(
                "e.g. Partnership Agreement"
            ),
        )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=120,
    )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with "
            "15 days notice"
        ),
        height=200,
        help=(
            "Separate major terms with "
            "semicolons."
        ),
    )

    effective_date = st.text_input(
        "Effective Date",
        placeholder=(
            "April 15, 2026"
        ),
    )

    generate = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )

    st.markdown(
        """
        <div class="disclaimer">
        LegalEase creates AI-assisted drafts,
        not legal advice. Review the final
        document for factual and
        jurisdiction-specific requirements.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# Generate
# ==========================================

if generate:

    if not all(
        [
            document_type.strip(),
            parties.strip(),
            terms.strip(),
            effective_date.strip(),
        ]
    ):

        st.error(
            "Please complete all required fields."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
        }

        try:

            with st.spinner(
                "Generating your draft..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=180,
                )

            if response.ok:

                data = response.json()

                st.session_state[
                    "document"
                ] = data["content"]

                st.session_state[
                    "document_type"
                ] = document_type

                st.session_state[
                    "model"
                ] = data.get(
                    "model",
                    "unknown",
                )

                st.session_state[
                    "mock"
                ] = data.get(
                    "mock",
                    False,
                )

                st.success(
                    "Document generated successfully."
                )

            else:

                try:
                    detail = response.json().get(
                        "detail",
                        response.text,
                    )
                except Exception:
                    detail = response.text

                st.error(
                    f"Backend error: {detail}"
                )

        except requests.RequestException as exc:

            st.error(
                "Could not reach the FastAPI "
                f"backend at {BACKEND_URL}. "
                "Start the backend first.\n\n"
                f"Details: {exc}"
            )


# ==========================================
# Generated document
# ==========================================

if "document" in st.session_state:

    st.divider()

    st.subheader(
        "Editable Document"
    )

    edited = st.text_area(
        "Edit the generated draft",
        value=st.session_state[
            "document"
        ],
        height=520,
        label_visibility="collapsed",
    )

    st.session_state[
        "document"
    ] = edited

    model_name = st.session_state.get(
        "model",
        "unknown",
    )

    is_mock = st.session_state.get(
        "mock",
        False,
    )

    status_text = (
        f"Model: {model_name}"
    )

    if is_mock:
        status_text += (
            " • Local mock mode"
        )

    st.caption(
        status_text
    )


    # ======================================
    # Preview
    # ======================================

    st.subheader(
        "Document Preview"
    )

    from backend.services.document_formatter import (
        format_html_preview,
    )

    preview_html = (
        format_html_preview(
            edited
        )
    )

    st.markdown(
        f'<div class="preview">'
        f'{preview_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


    # ======================================
    # Exports
    # ======================================

    st.subheader(
        "Download"
    )

    from backend.services.document_formatter import (
        format_docx,
        format_pdf,
        format_txt,
    )

    doc_type = st.session_state.get(
        "document_type",
        "Legal Document",
    )

    footer = os.getenv(
        "DOCUMENT_FOOTER",
        (
            "Generated with LegalEase - "
            "AI-assisted drafting - "
            "review before use"
        ),
    )

    txt_bytes = format_txt(
        edited
    )

    docx_bytes = format_docx(
        edited,
        doc_type,
        LOGO,
        footer,
    )

    pdf_bytes = format_pdf(
        edited,
        doc_type,
        LOGO,
        footer,
    )

    col1, col2, col3 = st.columns(3)

    base_filename = (
        "legalease_document"
    )

    with col1:

        st.download_button(
            "Download TXT",
            data=txt_bytes,
            file_name=(
                f"{base_filename}.txt"
            ),
            mime="text/plain",
            use_container_width=True,
        )

    with col2:

        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=(
                f"{base_filename}.docx"
            ),
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

    with col3:

        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=(
                f"{base_filename}.pdf"
            ),
            mime="application/pdf",
            use_container_width=True,
        )

else:

    st.info(
        "Enter the document details in "
        "the sidebar and click "
        "**Generate Document**."
    )