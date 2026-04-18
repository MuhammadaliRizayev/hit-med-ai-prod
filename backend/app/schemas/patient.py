from pydantic import BaseModel


class PatientCreate(BaseModel):
    full_name: str
    diagnosis: str | None = None
    status: str | None = "active"


class PatientResponse(BaseModel):
    id: int
    full_name: str
    diagnosis: str | None = None
    status: str | None = None

    class Config:
        from_attributes = True
