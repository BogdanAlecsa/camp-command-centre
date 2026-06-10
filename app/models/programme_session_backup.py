from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.database import Base


class ProgrammeSessionBackup(Base):
    __tablename__ = "programme_session_backup"

    id = Column(Integer, primary_key=True, index=True)
    camp_id = Column(Integer, ForeignKey("camp.id", ondelete="CASCADE"), nullable=False, index=True)
    programme_session_id = Column(
        Integer,
        ForeignKey("programme_session.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    location = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
