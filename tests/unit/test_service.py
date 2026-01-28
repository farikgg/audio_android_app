import pytest

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from src.visits.models import Visit, VisitStatus
from src.visits.service import VisitService

@pytest.mark.asyncio
async def test_create_visit():
    mock_session = AsyncMock()
    mock_storage = AsyncMock()
    mock_transcriber = MagicMock()
    mock_analyzer = MagicMock()
    mock_sheets_repo = MagicMock()
    mock_storage.save_file.return_value = "/tmp/fake.m4a"
    mock_session.add = MagicMock()

    service = VisitService(
        session=mock_session,
        storage=mock_storage,
        transcriber=mock_transcriber,
        analyzer=mock_analyzer,
        sheets_repo=mock_sheets_repo,
    )

    file_content_test: bytes = b"test"
    filename_test = "file_name_test"
    full_name_test = "full_name_test"
    location_test = "location_test"

    result = await service.create_visit(
        file_content=file_content_test,
        filename=filename_test,
        full_name=full_name_test,
        location=location_test,
    )

    assert result.filename == filename_test
    assert result.full_name == full_name_test
    assert result.location == location_test

    mock_storage.save_file.assert_called_once()
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_start_ai_analysis():
    mock_session = AsyncMock()
    mock_storage = AsyncMock()
    mock_transcriber = AsyncMock()
    mock_analyzer = AsyncMock()
    mock_sheets_repo = AsyncMock()

    mock_visit = Visit(
        id=1,
        full_name="full_name_test",
        filename="filename_test",
        filepath="filepath_test",
        location="location_test",
        status=VisitStatus.PENDING,
        ai_result=None,
        created_at=datetime.now()
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_visit
    mock_session.execute.return_value = mock_result

    mock_storage.read_file.return_value = b"fake_audio_bytes"
    mock_transcriber.transcribe.return_value = "Текст диалога"
    mock_analyzer.analyze.return_value = {"analyze": "Всё хорошо"}

    service = VisitService(
        session=mock_session,
        storage=mock_storage,
        transcriber=mock_transcriber,
        analyzer=mock_analyzer,
        sheets_repo=mock_sheets_repo,
    )

    await service.start_ai_analysis(1)

    assert mock_session.commit.call_count >= 1
    mock_sheets_repo.append_visit.assert_called_once()
    mock_transcriber.transcribe.assert_called_with(
        ("filename_test", b"fake_audio_bytes")
    )
