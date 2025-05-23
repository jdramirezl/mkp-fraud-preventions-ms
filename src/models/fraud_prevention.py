from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String

from src.database.database import Base


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FraudPrevention(Base):
    __tablename__ = "fraud_prevention"

    id = Column(String(36), primary_key=True)
    transaction_id = Column(String(255), nullable=False)
    user_ip = Column(String(100), nullable=False)
    device_id = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=False)
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.LOW)
    additional_data = Column(JSON, nullable=True)
    is_blocked = Column(Boolean, default=False)
    block_reason = Column(String, nullable=True)
    attempt_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
