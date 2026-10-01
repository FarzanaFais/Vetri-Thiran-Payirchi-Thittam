from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router


settings = get_settings()


app = FastAPI(
    title="LegalEase API",
    version="1.0.0",
    description=(
        "AI-assisted legal document"
        "drafting API" 
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
    ],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "ok",
        "service": "backend",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "mock_ai": settings.mock_ai,
    }