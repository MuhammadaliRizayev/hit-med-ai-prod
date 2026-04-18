from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.patients import router as patients_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HIT_MED_AI_PROD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://frontend-pi-green-49.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients_router)


@app.get("/")
def root():
    return {"ok": True, "service": "HIT_MED_AI_PROD backend"}


@app.get("/health")
def health():
    return {"ok": True}