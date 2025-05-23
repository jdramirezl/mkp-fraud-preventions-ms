from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.models.fraud_prevention import RiskLevel


class FraudPreventionBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda x: "".join(
            word.capitalize() if i else word for i, word in enumerate(x.split("_"))
        ),
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
        },
    )

    transaction_id: str = Field(
        ...,
        max_length=255,
        alias="transactionId",
        description="Unique identifier for the transaction",
    )
    user_ip: str = Field(
        ..., max_length=100, alias="userIp", description="IP address of the user"
    )
    device_id: Optional[str] = Field(
        None,
        max_length=255,
        alias="deviceId",
        description="Unique identifier for the user's device",
    )
    user_id: str = Field(
        ...,
        max_length=255,
        alias="userId",
        description="Unique identifier for the user",
    )
    additional_data: Optional[Dict[str, Any]] = Field(
        None,
        alias="additionalData",
        description="Additional transaction data like amount, currency, etc.",
    )


class FraudPreventionCreate(FraudPreventionBase):
    pass


class FraudPreventionUpdate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda x: "".join(
            word.capitalize() if i else word for i, word in enumerate(x.split("_"))
        ),
    )

    risk_level: Optional[RiskLevel] = Field(None, alias="riskLevel")
    is_blocked: Optional[bool] = Field(None, alias="isBlocked")
    block_reason: Optional[str] = Field(None, alias="blockReason")
    attempt_count: Optional[int] = Field(None, alias="attemptCount")


class FraudPreventionResponse(FraudPreventionBase):
    id: str
    risk_level: RiskLevel = Field(..., alias="riskLevel")
    is_blocked: bool = Field(..., alias="isBlocked")
    block_reason: Optional[str] = Field(None, alias="blockReason")
    attempt_count: int = Field(..., alias="attemptCount")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class BlockTransactionRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reason: str = Field(
        ..., min_length=1, description="Reason for blocking the transaction"
    )
