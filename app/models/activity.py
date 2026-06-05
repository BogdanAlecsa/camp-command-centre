from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    default_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    default_location: Mapped[str | None] = mapped_column(String(200), nullable=True)

    activity_lead_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("person.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    supporting_adults_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    equipment_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    wet_weather_alternative: Mapped[str | None] = mapped_column(Text, nullable=True)
    badge_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
