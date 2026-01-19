from typing import Any
from gspread_asyncio import (
    AsyncioGspreadClient,
    AsyncioGspreadClientManager,
    AsyncioGspreadSpreadsheet,
    AsyncioGspreadWorksheet
)
from gspread.exceptions import WorksheetNotFound
from google.oauth2.service_account import Credentials

from src.app.config import get_settings
from src.core.constants import GOOGLE_SHEETS_URLS
from src.core.exceptions import GoogleSheetsError
from src.core.logger import logger


class GoogleSheetsClient:
    """Клиент для работы с Google Sheets API."""
    def __init__(self) -> None:
        settings = get_settings().google_sheets_settings
        self.credentials_path = settings.credentials_path
        self.spreadsheet_id = settings.spreadsheet_id
        self.worksheet_name = settings.worksheet_name

        self._client: AsyncioGspreadClient | None = None
        self._spreadsheet: AsyncioGspreadSpreadsheet | None = None
        self._worksheet: AsyncioGspreadWorksheet | None = None

    def get_credentials(self) -> Credentials | Any:
        """Получение credentials для подключения Google Sheets API"""
        credentials: Credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=GOOGLE_SHEETS_URLS
        )

        return credentials

    async def _get_client(self) -> AsyncioGspreadClient:
        if self._client is None:
            try:
                manager = AsyncioGspreadClientManager(self.get_credentials)
                self._client = await manager.authorize()
                logger.debug("Google Sheets клиент инициализирован")
            except Exception as error:
                logger.exception(f"Ошибка при инициализации Google Sheets: {error}")
                raise GoogleSheetsError(f"Ошибка клиента Google Sheets: {error}")

        return self._client

    async def _init_headers(self) -> None:
        """Инициализация заголовка таблицы"""
        if self._worksheet is None:
            return

        if (await self._worksheet.acell("A1")).value:
            return

        headers = [
            "Вердикт от ИИ",
            "Торговый представитель",
        ]

        await self._worksheet.append_row(headers)

    async def get_worksheet(self) -> AsyncioGspreadWorksheet:
        """Получение или создание таблицы Google Sheets"""
        if self._worksheet is None:
            try:
                client = await self._get_client()
                self._spreadsheet: AsyncioGspreadSpreadsheet = await client.open_by_key(self.spreadsheet_id)
                self._worksheet: AsyncioGspreadWorksheet = await self._spreadsheet.worksheet(self.worksheet_name)
            except WorksheetNotFound:
                logger.info(f"Таблица {self.worksheet_name} не найдена, создаем новый")
                self._worksheet: AsyncioGspreadWorksheet = await self._spreadsheet.add_worksheet(
                    title=self.worksheet_name,
                    rows=1000,
                    cols=10
                )
                await self._init_headers()
            except Exception as error:
                logger.exception(f"Ошибка при создании таблицы Google Sheets {error}")
                raise GoogleSheetsError(f"Ошибка при создании таблицы Google Sheets: {error}")

        await self._init_headers()
        return self._worksheet
