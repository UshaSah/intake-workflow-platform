import enum
import uuid
from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SexEnum(str, enum.Enum):
    female = "female"
    male = "male"
    other = "other"
    unknown = "unknown"


class ContactPreferenceEnum(str, enum.Enum):
    sms = "sms"
    email = "email"
    voice = "voice"


class PatientStatusEnum(str, enum.Enum):
    new = "new"
    in_screening = "in_screening"
    matched = "matched"
    disqualified = "disqualified"
    enrolled = "enrolled"
    inactive = "inactive"


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    dob: Mapped[date | None] = mapped_column(Date, nullable=True)

    sex: Mapped[SexEnum] = mapped_column(
        Enum(SexEnum, name="sex_enum"),
        default=SexEnum.unknown,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    zip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    preferred_language: Mapped[str | None] = mapped_column(String(50), nullable=True)

    contact_preference: Mapped[ContactPreferenceEnum | None] = mapped_column(
        Enum(ContactPreferenceEnum, name="contact_pref_enum"),
        nullable=True,
    )

    status: Mapped[PatientStatusEnum] = mapped_column(
        Enum(PatientStatusEnum, name="patient_status_enum"),
        default=PatientStatusEnum.new,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
