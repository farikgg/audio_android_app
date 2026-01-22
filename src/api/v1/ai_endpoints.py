from fastapi import APIRouter, Depends, UploadFile, File, Form

from src.core.dependencies import get_visit_service
from src.schemas.visit_schema import VisitSchema
from src.visits.models import Visit
from src.visits.service import VisitService

router = APIRouter(tags=["Groq Analyzer"])

@router.post("/analyze_audio", response_model=VisitSchema)
async def transcribe(
    file: UploadFile = File(...),
    full_name: str = Form(...),
    location: str = Form(...),
    service: VisitService = Depends(get_visit_service),
) -> Visit:

    file_content = await file.read()
    filename = file.filename or "unknown_name.m4a"
    result = await service.process_visit(
        filename=filename,
        file_content=file_content,
        full_name=full_name,
        location=location,
    )

    return result
