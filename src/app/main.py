from fastapi import FastAPI

from src.app.config import get_settings
from src.api.v1 import ai_endpoints

settings = get_settings()

app = FastAPI(
    title=settings.app_name
)

app.include_router(ai_endpoints.router, prefix="/api/v1")
