from fastapi import FastAPI

from app.database import Base, engine
from app.models.patient import Patient

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

