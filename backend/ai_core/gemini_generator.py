from __future__ import annotations

from backend.config import Settings
from backend.schemas import DocumentRequest


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI-assisted legal drafting engine.

Your task is to create professional legal-document DRAFTS
using only facts supplied by the user.

Rules:

1. Never invent names, dates, addresses, amounts, obligations,
   governing law, jurisdiction, or other material facts.

2. If a material fact is missing, use a clear placeholder such as:
   [GOVERNING LAW]
   [PARTY NAME]
   [EFFECTIVE DATE]

3. Preserve every material user-provided term.

4. Use professional and formal legal language.

5. Organize the document with clear headings and numbered sections.

6. Include signature blocks where appropriate.

7. Do not claim that the document is legally valid.

8. Do not claim that an attorney reviewed the document.

9. Do not claim compliance with a particular jurisdiction unless
   the user supplied the jurisdiction.

10. Begin with the document title.

11. Include parties and effective date.

12. Include relevant clauses based on the supplied terms.

13. End with appropriate signature blocks.

14. Return plain text only.

15. Do not return Markdown code fences.

16. This is an AI-assisted legal draft and should be reviewed
    by an appropriately qualified legal professional where appropriate.
""".strip()


def _mock_document(request: DocumentRequest) -> str:
    """
    Creates a deterministic document without using Gemini.

    This allows developers to test the complete application
    without an API key.
    """

    terms = [
        part.strip()
        for part in request.terms.split(";")
        if part.strip()
    ]

    term_lines = "\n".join(
        f"{index}. {term}"
        for index, term in enumerate(terms, start=1)
    )

    if not term_lines:
        term_lines = "1. [TERMS TO BE PROVIDED]"

    return f"""
{request.document_type.upper()}

PARTIES

{request.parties}

EFFECTIVE DATE

{request.effective_date}

PURPOSE

This AI-assisted draft records the principal terms supplied
by the user and is intended for review and editing before execution.

TERMS AND CONDITIONS

{term_lines}

GENERAL PROVISIONS

1. Any missing jurisdiction-specific or transaction-specific
   provision should be completed after appropriate review.

2. This draft does not constitute legal advice.

SIGNATURES

Party 1:

Name: ______________________________

Signature: _________________________

Date: ______________________________


Party 2:

Name: ______________________________

Signature: _________________________

Date: ______________________________
""".strip()


class GeminiDocumentGenerator:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None

        # Lazy import:
        # the Google SDK isn't needed in mock mode.
        if (
            settings.gemini_api_key
            and not settings.mock_ai
        ):
            from google import genai

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def generate_document(
        self,
        request: DocumentRequest,
    ) -> tuple[str, bool]:

        # Local testing mode.
        if (
            self.settings.mock_ai
            or not self.settings.gemini_api_key
        ):
            return _mock_document(request), True

        if self.client is None:
            raise RuntimeError(
                "Gemini client is not configured."
            )

        prompt = f"""
Create a complete {request.document_type}
legal-document draft.

DOCUMENT TYPE:
{request.document_type}

PARTIES:
{request.parties}

TERMS AND CONDITIONS:
{request.terms}

EFFECTIVE DATE:
{request.effective_date}

Requirements:

- Use the supplied information exactly.
- Do not invent missing facts.
- Use placeholders for missing material facts.
- Use professional legal-document structure.
- Include numbered sections.
- Include appropriate signature blocks.
- Return plain text.
- Do not use Markdown code fences.
- Do not provide legal advice.
""".strip()

        from google.genai import types

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )

        text = (
            response.text
            if response.text
            else ""
        ).strip()

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text, False