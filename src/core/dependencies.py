from fastapi import Depends
from functools import lru_cache

from src.infrastructure.google_sheets import GoogleSheetsClient
from src.infrastructure.groq import GroqAnalyzer, GroqTranscriber
from src.repository.sheets_repository import GoogleSheetsRepository


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
