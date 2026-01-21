from datetime import datetime
from pydantic import BaseModel, field_validator


class GoogleSheetsSchema(BaseModel):
    full_name: str
    location: str
    ai_analyze: str
    created_at: datetime

    @field_validator("ai_analyze", mode="before")
    def check_ai_analyze(self, ai_analyze) -> str:
        if ai_analyze is None:
            return "Идет обработка диалога"
        return ai_analyze.get("analyze", "Галлюцинация ИИ")

    def to_list(self) -> list:
        return [
            self.full_name,
            self.location,
            self.ai_analyze,
            self.created_at
        ]
