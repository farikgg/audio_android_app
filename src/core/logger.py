from __future__ import annotations

import logging, sys

from pathlib import Path

from src.app.config import get_settings
from src.core.constants import LOG_FORMAT, FILE_ENCODER

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def setup_logger() -> logging.Logger:
    """Настройка логгера для приложения."""
    settings = get_settings()

    logger = logging.getLogger("android_backend")
    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=LOG_FORMAT,
    )

    # Консольный handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый handler (только для прода)
    if settings.environment == "prod":
        log_file = BASE_DIR / "logs" / "app.log"
        log_file.parent.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding=FILE_ENCODER)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()
