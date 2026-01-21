from typing import Any
from gspread_asyncio import AsyncioGspreadWorksheet

from src.infrastructure.google_sheets import GoogleSheetsClient
from src.core.exceptions import GoogleSheetsRepositoryError
from src.core.logger import logger


class GoogleSheetsRepository:
    """Репозиторий для управления записями в CRM-таблице Google Sheets"""
    def __init__(self, client: GoogleSheetsClient) -> None:
        self._client: GoogleSheetsClient = client

    async def _get_worksheet(self) -> AsyncioGspreadWorksheet:
        return await self._client.get_worksheet()

    async def append_visit(self, row_data: list[Any]) -> None:
        """row_data: [ФИО, Геолокация, Анализ ИИ, Дата создания]"""
        worksheet = await self._get_worksheet()
        try:
            await worksheet.append_row(row_data)
            logger.info("Запись успешно добавлена в Google Sheet!")
        except Exception as error:
            logger.exception(f"Ошибка при добавлении записи в Google Sheets: {error}")
            raise GoogleSheetsRepositoryError(f"Ошибка при добавлении записи в Google Sheets:  {error}")
