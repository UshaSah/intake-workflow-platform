from fastapi import FastAPI
from app.models.trial import Trial
from app.models.trial import Trial
from app.models.eligibility_rule import EligibilityRule
from app.database import Base, engine
from app.models.patient import Patient
from app.models.idempotency_key import IdempotencyKey
from app.routers.patient import router as patients_router


app = FastAPI()

app.include_router(patients_router)

@app.get("/")
def health():
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)