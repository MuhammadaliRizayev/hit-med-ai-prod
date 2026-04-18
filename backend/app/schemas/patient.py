from pydantic import BaseModel


class PatientCreate(BaseModel):
    full_name: str
    diagnosis: str | None = None
    status: str | None = None
    sex: str | None = None
    age: int | None = None
    height_cm: str | None = None
    weight_kg: str | None = None

    medulloblastoma_histology: str | None = None
    medulloblastoma_molecular: str | None = None
    medulloblastoma_m_status: str | None = None
    medulloblastoma_r_status: str | None = None


class PatientResponse(BaseModel):
    id: int
    full_name: str
    diagnosis: str | None = None
    status: str | None = None
    sex: str | None = None
    age: int | None = None
    height_cm: str | None = None
    weight_kg: str | None = None

    medulloblastoma_histology: str | None = None
    medulloblastoma_molecular: str | None = None
    medulloblastoma_m_status: str | None = None
    medulloblastoma_r_status: str | None = None

    class Config:
        from_attributes = True