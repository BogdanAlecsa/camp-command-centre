from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProgrammeSession(Base):
    __tablename__ = "programme_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    session_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    session_type: Mapped[str] = mapped_column(String(80), nullable=False, default="Activity")

    activity_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("activity.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    participant_team_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("team.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    lead_person_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("person.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    rotation_group: Mapped[str | None] = mapped_column(String(200), nullable=True)
    rotation_slot_number: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
