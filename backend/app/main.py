from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routers.patients import router as patients_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HIT_MED_AI_PROD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients_router)


@app.get("/")
def root():
    return {"message": "HIT_MED_AI_PROD backend ishlayapti"}


@app.get("/health")
def health():
    return {"ok": True}
