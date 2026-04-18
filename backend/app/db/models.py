from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    diagnosis = Column(String, nullable=True)
    status = Column(String, default="active")
