from pydantic import BaseModel, Field


class AIResponseSchema(BaseModel):
    analyze: str = Field(..., description="Основной анализ ИИ")
    # result: str = Field(..., description="Итог от ИИ")
