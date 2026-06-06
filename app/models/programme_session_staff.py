from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProgrammeSessionStaff(Base):
    __tablename__ = "programme_session_staff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    programme_session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("programme_session.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    person_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(String(80), nullable=False, default="Supporting Adult")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
