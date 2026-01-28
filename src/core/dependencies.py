from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.infrastructure.storage import LocalStorage
from src.infrastructure.s3_storage import S3Storage
from src.infrastructure.google_sheets import GoogleSheetsClient
from src.infrastructure.groq import GroqAnalyzer, GroqTranscriber
from src.repository.sheets_repository import GoogleSheetsRepository
from src.visits.service import VisitService

@lru_cache
def get_groq_analyzer() -> GroqAnalyzer:
    return GroqAnalyzer()

@lru_cache
def get_groq_transcriber() -> GroqTranscriber:
    return GroqTranscriber()

@lru_cache
def get_google_sheets_client() -> GoogleSheetsClient:
    return GoogleSheetsClient()

def get_google_sheets_repository(
        client: GoogleSheetsClient = Depends(get_google_sheets_client)
) -> GoogleSheetsRepository:
    return GoogleSheetsRepository(client)

@lru_cache
def get_local_storage() -> LocalStorage:
    return LocalStorage()

@lru_cache
def get_s3_storage() -> S3Storage:
    return S3Storage()

def get_visit_service(
        session: AsyncSession = Depends(get_async_session),
        storage: S3Storage = Depends(get_s3_storage),
        transcriber: GroqTranscriber = Depends(get_groq_transcriber),
        analyzer: GroqAnalyzer = Depends(get_groq_analyzer),
        sheets_repo: GoogleSheetsRepository = Depends(get_google_sheets_repository)
) -> VisitService:

    return VisitService(
        session=session,
        storage=storage,
        transcriber=transcriber,
        analyzer=analyzer,
        sheets_repo=sheets_repo
    )
