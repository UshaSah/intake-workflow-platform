import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Enum, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class RuleTypeEnum(str, enum.Enum):
    age_min = "age_min"
    age_max = "age_max"
    sex = "sex"
    bmi_min = "bmi_min",
    bmi_max = "bmi_max"
    diagnosis_includes = "diagnosis_includes"
    lab_value_min = "lab_value_min"
    lab_value_max = "lab_value_max"
    medication_excludes = "medication_excludes"
    
class OpEnum(str, enum.Enum):
    gte = ">="
    lte = "<="
    eq = "=="
    in_ = "in"
    not_in = "not_in"
    contains = "contains"

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    trial_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trials.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    rule_type: Mapped[RuleTypeEnum] = mapped_column(
        Enum(RuleTypeEnum, name="rule_type_enum"),
        nullable=False,
    )
    
    field: Mapped[str] = mapped_column(String(64), nullable=False)
    
    op: Mapped[OpEnum] = mapped_column(
        Enum(OpEnum, name="rule_op_num"),
        nullable=False,
    )
    
    #flexible values: number/string/list/object
    value_Json: Mapped[any] = mapped_column(JSONB, nullable=False)
    
    is_inclusion: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    # ORM relationship back to Trial
    trial = relationship("Trial", back_populates="eligibility_rules")