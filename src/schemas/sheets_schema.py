from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

from src.core.constants import DATA_FORMAT


class GoogleSheetsSchema(BaseModel):
    full_name: str
    location: str
    ai_analyze: str
    created_at: datetime

    def to_list(self) -> list:
        kz_timezone = timezone(timedelta(hours=5))
        local_time = self.created_at.astimezone(kz_timezone)

        return [
            self.full_name,
            self.location,
            self.ai_analyze,
            local_time.strftime(DATA_FORMAT),
        ]
