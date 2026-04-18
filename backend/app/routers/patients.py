from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Patient, PatientHistory, PatientLab, PatientTreatment
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])


class HistoryCreate(BaseModel):
    event_date: str
    title: str
    description: str | None = None


class LabCreate(BaseModel):
    test: str
    value: str | None = None
    unit: str | None = None
    note: str | None = None


class TreatmentCreate(BaseModel):
    treatment_type: str
    title: str
    status: str | None = None
    note: str | None = None


@router.get("/", response_model=list[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.id.desc()).all()


@router.post("/", response_model=PatientResponse)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(
        full_name=payload.full_name,
        diagnosis=payload.diagnosis,
        status=payload.status or "active",
        sex=payload.sex,
        age=payload.age,
        height_cm=payload.height_cm,
        weight_kg=payload.weight_kg,
        medulloblastoma_histology=payload.medulloblastoma_histology,
        medulloblastoma_molecular=payload.medulloblastoma_molecular,
        medulloblastoma_m_status=payload.medulloblastoma_m_status,
        medulloblastoma_r_status=payload.medulloblastoma_r_status,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    db.add(PatientHistory(
        patient_id=patient.id,
        event_date="2026-04-19",
        title="Bemor ro'yxatga olindi",
        description=f"{patient.full_name} tizimga qo'shildi.",
    ))
    db.add(PatientLab(
        patient_id=patient.id,
        test="WBC",
        value="-",
        unit="x10^9/L",
        note="starter placeholder",
    ))
    db.add(PatientTreatment(
        patient_id=patient.id,
        treatment_type="Chemotherapy",
        title="Initial treatment planning",
        status="planned",
        note="Starter treatment record",
    ))
    db.commit()

    return patient


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, payload: PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.full_name = payload.full_name
    patient.diagnosis = payload.diagnosis
    patient.status = payload.status or patient.status
    patient.sex = payload.sex
    patient.age = payload.age
    patient.height_cm = payload.height_cm
    patient.weight_kg = payload.weight_kg
    patient.medulloblastoma_histology = payload.medulloblastoma_histology
    patient.medulloblastoma_molecular = payload.medulloblastoma_molecular
    patient.medulloblastoma_m_status = payload.medulloblastoma_m_status
    patient.medulloblastoma_r_status = payload.medulloblastoma_r_status

    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}/history")
def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    items = (
        db.query(PatientHistory)
        .filter(PatientHistory.patient_id == patient_id)
        .order_by(PatientHistory.id.desc())
        .all()
    )

    return {
        "ok": True,
        "patient_id": patient_id,
        "items": [
            {
                "date": item.event_date,
                "title": item.title,
                "description": item.description or "",
            }
            for item in items
        ],
    }


@router.post("/{patient_id}/history")
def create_patient_history(patient_id: int, payload: HistoryCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    item = PatientHistory(
        patient_id=patient_id,
        event_date=payload.event_date,
        title=payload.title,
        description=payload.description,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "ok": True,
        "item": {
            "id": item.id,
            "date": item.event_date,
            "title": item.title,
            "description": item.description or "",
        },
    }


@router.get("/{patient_id}/labs")
def get_patient_labs(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    items = (
        db.query(PatientLab)
        .filter(PatientLab.patient_id == patient_id)
        .order_by(PatientLab.id.desc())
        .all()
    )

    return {
        "ok": True,
        "patient_id": patient_id,
        "items": [
            {
                "test": item.test,
                "value": item.value or "",
                "unit": item.unit or "",
                "note": item.note or "",
            }
            for item in items
        ],
    }


@router.post("/{patient_id}/labs")
def create_patient_lab(patient_id: int, payload: LabCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    item = PatientLab(
        patient_id=patient_id,
        test=payload.test,
        value=payload.value,
        unit=payload.unit,
        note=payload.note,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "ok": True,
        "item": {
            "id": item.id,
            "test": item.test,
            "value": item.value or "",
            "unit": item.unit or "",
            "note": item.note or "",
        },
    }


@router.get("/{patient_id}/treatment")
def get_patient_treatment(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    items = (
        db.query(PatientTreatment)
        .filter(PatientTreatment.patient_id == patient_id)
        .order_by(PatientTreatment.id.desc())
        .all()
    )

    return {
        "ok": True,
        "patient_id": patient_id,
        "items": [
            {
                "type": item.treatment_type,
                "title": item.title,
                "status": item.status or "",
                "note": item.note or "",
            }
            for item in items
        ],
    }


@router.post("/{patient_id}/treatment")
def create_patient_treatment(patient_id: int, payload: TreatmentCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    item = PatientTreatment(
        patient_id=patient_id,
        treatment_type=payload.treatment_type,
        title=payload.title,
        status=payload.status,
        note=payload.note,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "ok": True,
        "item": {
            "id": item.id,
            "type": item.treatment_type,
            "title": item.title,
            "status": item.status or "",
            "note": item.note or "",
        },
    }