from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FraudPrevention(Base):
    __tablename__ = "fraud_prevention"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_ip: Mapped[str] = mapped_column(String(100), nullable=False)
    device_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(
        SQLEnum(RiskLevel), default=RiskLevel.LOW
    )
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    block_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
