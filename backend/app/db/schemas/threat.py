from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.threat_threat_type_mapping import threat_threat_type_mapping


class Threat(Base):
    __tablename__ = "threat"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    description = Column(String)

    types = relationship("ThreatType", secondary=threat_threat_type_mapping)

    value = Column(String, nullable=False, unique=True, index=True)