from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class CareUnit(Base):
    __tablename__ = "care_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    cnes = Column(String(20), nullable=True, unique=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)

    consultations = relationship(
        "Consultation",
        back_populates="care_unit",
        cascade="all, delete-orphan",
    )
