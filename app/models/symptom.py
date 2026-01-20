from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base


class Symptom(Base):
    __tablename__ = "symptom"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
