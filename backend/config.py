from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(
        default="LegalEase",
        alias="APP_NAME",
    )

    company_name: str = Field(
        default="LegalEase",
        alias="COMPANY_NAME",
    )

    gemini_api_key: str = Field(
        default="",
        alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-3.8-flash",
        alias="GEMINI_MODEL",
    )

    mock_ai: bool = Field(
        default=True,
        alias="MOCK_AI",
    )

    backend_host: str = Field(
        default="127.0.0.1",
        alias="BACKEND_HOST",
    )

    backend_port: int = Field(
        default=8000,
        alias="BACKEND_PORT",
    )

    cors_origins: str = Field(
        default=(
            "http://localhost:8501,"
            "http://127.0.0.1:8501"
        ),
        alias="CORS_ORIGINS",
    )

    logo_path: str = Field(
        default="assets/logo.png",
        alias="LOGO_PATH",
    )

    document_font: str = Field(
        default="Times New Roman",
        alias="DOCUMENT_FONT",
    )

    document_footer: str = Field(
        default=(
            "Generated with LegalEase - "
            "AI-assisted drafting - review before use"
        ),
        alias="DOCUMENT_FOOTER",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            item.strip()
            for item in self.cors_origins.split(",")
            if item.strip()
        ]

    @property
    def logo_file(self) -> Path:
        return BASE_DIR / self.logo_path


@lru_cache
def get_settings() -> Settings:
    return Settings()