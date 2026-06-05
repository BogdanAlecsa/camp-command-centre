from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CampRiskControl(Base):
    __tablename__ = "camp_risk_control"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    risk_assessment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp_risk_assessment.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    hazard: Mapped[str] = mapped_column(Text, nullable=False)
    who_might_be_harmed: Mapped[str | None] = mapped_column(Text, nullable=True)
    controls_in_place: Mapped[str | None] = mapped_column(Text, nullable=True)
    further_controls_needed: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsible_person: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
