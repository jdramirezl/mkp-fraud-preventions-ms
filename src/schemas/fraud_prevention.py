from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from src.models.fraud_prevention import RiskLevel


class FraudPreventionBase(BaseModel):
    transaction_id: str = Field(..., max_length=255)
    user_ip: str = Field(..., max_length=100)
    device_id: Optional[str] = Field(None, max_length=255)
    user_id: str = Field(..., max_length=255)
    additional_data: Optional[Dict[str, Any]] = None


class FraudPreventionCreate(FraudPreventionBase):
    pass


class FraudPreventionUpdate(BaseModel):
    risk_level: Optional[RiskLevel] = None
    is_blocked: Optional[bool] = None
    block_reason: Optional[str] = None
    attempt_count: Optional[int] = None


class FraudPreventionResponse(FraudPreventionBase):
    id: str
    risk_level: RiskLevel
    is_blocked: bool
    block_reason: Optional[str]
    attempt_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlockTransactionRequest(BaseModel):
    reason: str = Field(..., min_length=1)
