import logging

from dotenv import load_dotenv
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from functools import lru_cache

from src.core.constants import FILE_ENCODER

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    logging.error("Отсутствует файл .env в корне проекта.")


class _ProjectBaseSettings(BaseSettings):
    """Базовые настройки."""
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding=FILE_ENCODER,
        populate_by_name=True,
        extra="ignore",
    )


class GroqSettings(_ProjectBaseSettings):
    api_key: str = Field(default="", alias="GROQ_API_KEY")

    whisper_model: str = Field(default="whisper-large-v3", alias="WHISPER_MODEL")
    llm_model: str = Field(default="llama-3.1-8b-instant", alias="GROQ_LLM_MODEL")

    openai_base_url: str = Field(
        default="https://api.groq.com/openai/v1",
        alias="OPENAI_GROQ_BASE_URL"
    )


class AppSettings(_ProjectBaseSettings):
    environment: Literal["local", "dev", "prod"] = Field(default="local", validation_alias="APP_ENV")
    app_name: str = Field(default="Android App with AI analyzer")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    groq_settings: GroqSettings = Field(default_factory=GroqSettings)

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
