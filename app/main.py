from fastapi import FastAPI

from app.database import Base, engine
from app.models.patient import Patient
from app.routers.patient import router as patients_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(patients_router)


@app.get("/")
def health():
    return {"status": "ok"}

