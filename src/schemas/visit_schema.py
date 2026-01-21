from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel, Field

from src.visits.models import VisitStatus
from src.schemas.ai_schema import AIResponseSchema


class VisitSchema(BaseModel):
    id: int = Field(..., description="Идентификатор визитов")
    status: VisitStatus
    filepath: str = Field(..., description="Путь файла с облачного хранилища")
    ai_result: Optional[AIResponseSchema] = Field(default=None)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) # из объекта SQLAlchemy в питоновский объект
