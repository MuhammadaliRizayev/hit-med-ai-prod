from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    diagnosis = Column(String, nullable=True)
    status = Column(String, nullable=True)

    sex = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    height_cm = Column(String, nullable=True)
    weight_kg = Column(String, nullable=True)

    medulloblastoma_histology = Column(String, nullable=True)
    medulloblastoma_molecular = Column(String, nullable=True)
    medulloblastoma_m_status = Column(String, nullable=True)
    medulloblastoma_r_status = Column(String, nullable=True)

    ependymoma_histology = Column(String, nullable=True)
    ependymoma_molecular = Column(String, nullable=True)
    ependymoma_location = Column(String, nullable=True)
    ependymoma_m_status = Column(String, nullable=True)
    ependymoma_r_status = Column(String, nullable=True)

    pineoblastoma_histology = Column(String, nullable=True)
    pineoblastoma_molecular = Column(String, nullable=True)
    pineoblastoma_m_status = Column(String, nullable=True)
    pineoblastoma_r_status = Column(String, nullable=True)

    protocol_table_id = Column(String, nullable=True)
    protocol_risk_group = Column(String, nullable=True)
    protocol_phase = Column(String, nullable=True)
    protocol_review_required = Column(String, nullable=True)

    histories = relationship("PatientHistory", back_populates="patient", cascade="all, delete-orphan")
    labs = relationship("PatientLab", back_populates="patient", cascade="all, delete-orphan")
    treatments = relationship("PatientTreatment", back_populates="patient", cascade="all, delete-orphan")


class PatientHistory(Base):
    __tablename__ = "patient_histories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    event_date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="histories")


class PatientLab(Base):
    __tablename__ = "patient_labs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    test = Column(String, nullable=False)
    value = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    note = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="labs")


class PatientTreatment(Base):
    __tablename__ = "patient_treatments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    treatment_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=True)
    note = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="treatments")