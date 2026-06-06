from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    person_type: Mapped[str] = mapped_column(String(50), nullable=False)

    home_section_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("section.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    is_provisional: Mapped[bool] = mapped_column(Integer, nullable=False, default=False)
    attendance_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    information_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    section_unit: Mapped[str | None] = mapped_column(String(120), nullable=True)

    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)

    primary_contact_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    primary_contact_relationship: Mapped[str | None] = mapped_column(String(100), nullable=True)
    primary_contact_phone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    primary_contact_email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    emergency_contact_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    emergency_contact_relationship: Mapped[str | None] = mapped_column(String(100), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    emergency_contact_email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)
    allergy_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    medication: Mapped[str | None] = mapped_column(Text, nullable=True)
    medical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    dietary_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)

    role_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
