from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.visits.models import Visit, VisitStatus
from src.infrastructure.storage import LocalStorage
from src.infrastructure.groq import GroqTranscriber, GroqAnalyzer
from src.repository.sheets_repository import GoogleSheetsRepository
from src.schemas.sheets_schema import GoogleSheetsSchema


class VisitService:
    def __init__(
            self,
            session: AsyncSession,
            storage: LocalStorage,
            transcriber: GroqTranscriber,
            analyzer: GroqAnalyzer,
            sheets_repo: GoogleSheetsRepository
    ) -> None:
        self.session = session
        self.storage = storage
        self.transcriber = transcriber
        self.analyzer = analyzer
        self.sheets_repo = sheets_repo

    async def process_visit(
            self,
            file_content: bytes,
            filename: str,
            full_name: str,
            location: str
    ) -> Visit:

        saved_path = await self.storage.save_file(filename, file_content)

        visit = Visit(
            filename=filename,
            full_name=full_name,
            location=location,
            filepath=saved_path,
            status=VisitStatus.PENDING,
        )

        self.session.add(visit)
        await self.session.commit()
        await self.session.refresh(visit)

        try:
            ai_text = "Нет данных"
            text = await self.transcriber.transcribe((filename, file_content))
            ai_data = await self.analyzer.analyze(text)

            visit.ai_result = ai_data
            visit.status = VisitStatus.COMPLETED
            await self.session.commit()

            if visit.ai_result:
                ai_text = visit.ai_result.get("analyze", "Ошибка структуры JSON")

            logger.info("Подготовка к записи в Google Sheets")
            google_sheets_schema = GoogleSheetsSchema(
                full_name=visit.full_name,
                location=visit.location,
                ai_analyze=ai_text,  # Валидатор схемы достанет текст
                created_at=visit.created_at
            )

            await self.sheets_repo.append_visit(google_sheets_schema.to_list())
            logger.info("Успешное добавление записи в Google Sheets")

        except Exception as error:
            logger.exception(f"Ошибка при обработке визита: {error}")

            visit.status = VisitStatus.FAILED
            await self.session.commit()

            raise error

        return visit
