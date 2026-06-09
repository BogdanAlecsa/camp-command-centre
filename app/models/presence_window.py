from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PresenceWindow(Base):
    __tablename__ = "presence_window"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # camp / participating_group / section / person
    scope_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)

    # null for camp scope, otherwise the id of the group/section/person
    scope_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)

    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Expected / Not Attending / Unknown
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="Expected")

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
