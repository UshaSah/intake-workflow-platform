from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr

from app.models.patient import SexEnum, ContactPreferenceEnum, PatientStatusEnum


class PatientCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    dob: date | None = None
    sex: SexEnum = SexEnum.unknown
    phone: str | None = None
    email: EmailStr | None = None
    zip: str | None = None
    preferred_language: str | None = None
    contact_preference: ContactPreferenceEnum | None = None


class PatientOut(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None
    dob: date | None
    sex: SexEnum
    phone: str | None
    email: EmailStr | None
    zip: str | None
    preferred_language: str | None
    contact_preference: ContactPreferenceEnum | None
    status: PatientStatusEnum

    class Config:
        from_attributes = True
