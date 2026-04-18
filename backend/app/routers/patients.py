from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Patient, PatientHistory, PatientLab, PatientTreatment
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_model=list[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.id.desc()).all()


@router.post("/", response_model=PatientResponse)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(
        full_name=payload.full_name,
        diagnosis=payload.diagnosis,
        status=payload.status or "active",
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    starter_history = PatientHistory(
        patient_id=patient.id,
        event_date="2026-04-19",
        title="Bemor ro'yxatga olindi",
        description=f"{patient.full_name} tizimga qo'shildi.",
    )
    starter_lab = PatientLab(
        patient_id=patient.id,
        test="WBC",
        value="-",
        unit="x10^9/L",
        note="starter placeholder",
    )
    starter_treatment = PatientTreatment(
        patient_id=patient.id,
        treatment_type="Chemotherapy",
        title="Initial treatment planning",
        status="planned",
        note="Starter treatment record",
    )

    db.add(starter_history)
    db.add(starter_lab)
    db.add(starter_treatment)
    db.commit()

    return patient


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
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