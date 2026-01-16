from fastapi import APIRouter, Depends, UploadFile, File

from src.app.config import get_settings
from src.api.dependencies import get_groq_analyzer, get_groq_transcriber
from src.infrastructure.groq import GroqAnalyzer, GroqTranscriber

router = APIRouter(tags=["Groq Analyzer"])
settings = get_settings()

@router.post("/analyze")
async def analyze(
    system: str,
    prompt: str,
    service: GroqAnalyzer = Depends(get_groq_analyzer)
):
    result = await service.analyze(system, prompt)
    return result

@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    service: GroqTranscriber = Depends(get_groq_transcriber)
):
    file_content = await file.read()
    result = (file.filename, file_content)
    return await service.transcribe(result)
