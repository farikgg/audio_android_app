from asyncio import run as async_run

from src.core.celery import celery_app
from src.core.database import async_session_maker
from src.infrastructure.groq import GroqAnalyzer, GroqTranscriber
from src.infrastructure.google_sheets import GoogleSheetsClient
from src.infrastructure.s3_storage import S3Storage
from src.repository.sheets_repository import GoogleSheetsRepository
from src.visits.service import VisitService

async def run_process_visit(visit_id: int):
    async with async_session_maker() as session:
        analyzer: GroqAnalyzer = GroqAnalyzer()
        transcriber: GroqTranscriber = GroqTranscriber()
        google_client: GoogleSheetsClient = GoogleSheetsClient()
        storage: S3Storage = S3Storage()
        google_repository: GoogleSheetsRepository = GoogleSheetsRepository(google_client)

        service: VisitService = VisitService(
            session=session,
            storage=storage,
            transcriber=transcriber,
            analyzer=analyzer,
            sheets_repo=google_repository
        )

        await service.start_ai_analysis(visit_id)

@celery_app.task(name="process_visits")
def process_visits(visit_id: int):
    async_run(run_process_visit(visit_id))
