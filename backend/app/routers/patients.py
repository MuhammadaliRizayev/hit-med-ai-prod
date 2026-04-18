from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Patient
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

    return {
        "ok": True,
        "patient_id": patient_id,
        "items": [
            {
                "date": "2026-04-19",
                "title": "Bemor ro'yxatga olindi",
                "description": f"{patient.full_name} tizimga qo'shildi.",
            },
            {
                "date": "2026-04-19",
                "title": "Boshlang'ich tashxis kiritildi",
                "description": patient.diagnosis or "Tashxis kiritilmagan",
            },
        ],
    }


@router.get("/{patient_id}/labs")
def get_patient_labs(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "ok": True,
        "patient_id": patient_id,
        "items": [
            {"test": "WBC", "value": "-", "unit": "x10^9/L", "note": "placeholder"},
            {"test": "HGB", "value": "-", "unit": "g/L", "note": "placeholder"},
            {"test": "PLT", "value": "-", "unit": "x10^9/L", "note": "placeholder"},
        ],
    }


@router.get("/{patient_id}/treatment")
def get_patient_treatment(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "ok": True,
        "patient_id": patient_id,
        "items": [
            {
                "type": "Chemotherapy",
                "title": "Induction block",
                "status": "planned",
                "note": "Treatment module placeholder",
            },
            {
                "type": "Supportive care",
                "title": "Hydration and monitoring",
                "status": "planned",
                "note": "Supportive block placeholder",
            },
        ],
    }