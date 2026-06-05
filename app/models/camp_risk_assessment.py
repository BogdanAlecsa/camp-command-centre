from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CampRiskAssessment(Base):
    __tablename__ = "camp_risk_assessment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False, default="Camp Risk Assessment")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Not Started")

    prepared_by: Mapped[str | None] = mapped_column(String(200), nullable=True)
    review_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    submitted_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    approved_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    approval_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    site_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    overnight_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    supervision_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    communication_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
