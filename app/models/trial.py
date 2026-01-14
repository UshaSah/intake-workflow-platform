import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class TrialStatusEnum(str, enum.Enum):
    recruiting = "recruiting"
    active = "active"
    closed = "closed"

class Trial(Base):
    __tablename__ = "trials"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    nct_id: Mapped[str | None] = mapped_column(String(50), unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Can store multiple condiitons as an array of text
    condition: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    
    phase: Mapped[str | None] = mapped_column(String(50))
    
    status: Mapped[TrialStatusEnum] = mapped_column(
        Enum(TrialStatusEnum, name="trial_status_enum"),
        default=TrialStatusEnum.recruiting,
        nullable=False,       
    )
    
    sponsor: Mapped[str | None] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(String)
    
    eligibility_rules = relationship(
        "EligibilityRule",
        back_populates="trial",
        cascade="all, delete-orphan",
)   
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    