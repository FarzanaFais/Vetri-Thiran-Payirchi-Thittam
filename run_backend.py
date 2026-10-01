import uvicorn

from backend.config import get_settings


if __name__ == "__main__":

    settings = get_settings()

    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )