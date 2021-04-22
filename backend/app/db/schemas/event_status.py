from sqlalchemy import Column, Integer, String

from db.database import Base


class EventStatus(Base):
    __tablename__ = "event_status"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)