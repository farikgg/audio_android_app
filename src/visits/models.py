import enum

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Enum, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class VisitStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    # TODO: описание ТП для дополнения визита
    filepath: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[VisitStatus] = mapped_column(Enum(VisitStatus), default=VisitStatus.PENDING)
    ai_result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
