from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator,
)
from backend.config import get_settings
from backend.schemas import (
    DocumentRequest,
    DocumentResponse,
)


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate_document(
    request: DocumentRequest,
) -> DocumentResponse:

    settings = get_settings()

    generator = GeminiDocumentGenerator(
        settings
    )

    try:

        content, mock = (
            generator.generate_document(
                request
            )
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "Document generation failed: "
                f"{exc}"
            ),
        ) from exc

    return DocumentResponse(
        document_type=request.document_type,
        content=content,
        model=(
            "mock"
            if mock
            else settings.gemini_model
        ),
        mock=mock,
    )