from fastapi import APIRouter, Depends, UploadFile, File

from src.api.dependencies import get_groq_analyzer, get_groq_transcriber
from src.infrastructure.groq import GroqAnalyzer, GroqTranscriber


router = APIRouter(tags=["Groq Analyzer"])

@router.post("/analyze_audio")
async def transcribe(
    file: UploadFile = File(...),
    service_transcribe: GroqTranscriber = Depends(get_groq_transcriber),
    service_analyze: GroqAnalyzer = Depends(get_groq_analyzer)
) -> dict:

    file_content: bytes = await file.read()
    audio_text: str = await service_transcribe.transcribe((file.filename, file_content))

    analyze_result = await service_analyze.analyze(audio_text)

    return analyze_result
