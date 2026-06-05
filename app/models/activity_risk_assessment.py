from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ActivityRiskAssessment(Base):
    __tablename__ = "activity_risk_assessment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    activity_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("activity.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_type: Mapped[str] = mapped_column(String(80), nullable=False, default="Created in app")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Not Started")

    leader_in_charge: Mapped[str | None] = mapped_column(String(200), nullable=True)
    prepared_by: Mapped[str | None] = mapped_column(String(200), nullable=True)
    review_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    provider_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    provider_contact: Mapped[str | None] = mapped_column(String(200), nullable=True)
    provider_reference: Mapped[str | None] = mapped_column(Text, nullable=True)

    provider_risk_assessment_received: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    provider_insurance_checked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    provider_qualification_checked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    scout_led_parts_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    overall_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
