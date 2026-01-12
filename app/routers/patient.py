from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.models.idempotency_key import IdempotencyKey
from app.schemas.patient import PatientCreate, PatientOut
from app.utils.idempotency import stable_request_hash

router = APIRouter(prefix="/patients", tags=['patients'])

@router.post("", response_model=PatientOut, status_code=201)
def create_patient(
    payload: PatientCreate, 
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    
    payload_dict = payload.model_dump()
    req_hash = stable_request_hash(payload_dict)
    
    # if idempotency-Key is provided, enforce idempotency
    if idempotency_key:
        existing = (
            db.query(IdempotencyKey)
            .filter(IdempotencyKey.key == idempotency_key)
            .one_or_none()
        )
        
        if existing:
            # same key but different payload => conflict
            if existing.request_hash != req_hash:
                raise HTTPException(
                    status_code=409,
                    detail="Idempotency-Key already used with a different request body."
                )
                
            patient = db.get(Patient, existing.resource_id)
            if not patient:
                # shouldn't happen unless DB was manually edited
                raise HTTPException(status_code=500, detail="Idempotency record is corrupted.")
            return patient
    
    patient = Patient(**payload_dict)
    db.add(patient)
    db.flush()  # get patient.id without committing yet
    
    # Store idempotency record(if header present)
    if idempotency_key:
        record = IdempotencyKey(
            key=idempotency_key,
            request_hash=req_hash,
            resource_type="patient",
            resource_id=patient.id,
        )
        db.add(record)
        
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

