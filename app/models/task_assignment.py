from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskAssignment(Base):
    __tablename__ = "task_assignment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    camp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("camp.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    assigned_person_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("person.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    assigned_team_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("team.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    assignment_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status_override: Mapped[str | None] = mapped_column(String(50), nullable=True)
