from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.config import get_settings
from src.api.v1 import ai_endpoints
from src.core.database import async_engine, get_async_session
from src.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")
    logger.info("Приложение запущено!")
    yield

    logger.info("Остановка приложения...")
    await async_engine.dispose()
    logger.info("✅ Приложение остановлено")

def create_application() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.debug
    )
    application.include_router(ai_endpoints.router, prefix="/api/v1")

    return application

app = create_application()
