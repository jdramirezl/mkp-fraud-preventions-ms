import uuid
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from src.metrics import increment_blocked_transactions, increment_fraud_attempts
from src.models.fraud_prevention import FraudPrevention, RiskLevel
from src.schemas.fraud_prevention import FraudPreventionCreate, FraudPreventionUpdate


class FraudPreventionService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, fraud_data: FraudPreventionCreate) -> FraudPrevention:
        risk_level = self._assess_risk(fraud_data.user_id)
        db_fraud = FraudPrevention(
            id=str(uuid.uuid4()),
            transaction_id=fraud_data.transaction_id,
            user_ip=fraud_data.user_ip,
            device_id=fraud_data.device_id,
            user_id=fraud_data.user_id,
            risk_level=risk_level,
            additional_data=fraud_data.additional_data,
            attempt_count=0,
            is_blocked=False,
        )

        # Track fraud attempt
        increment_fraud_attempts(risk_level.value)

        self.db.add(db_fraud)
        self.db.commit()
        self.db.refresh(db_fraud)
        return db_fraud

    def get_all(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[List[FraudPrevention], int]:
        total = self.db.query(FraudPrevention).count()
        frauds = (
            self.db.query(FraudPrevention)
            .order_by(FraudPrevention.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return frauds, total

    def get_by_id(self, fraud_id: str) -> Optional[FraudPrevention]:
        return (
            self.db.query(FraudPrevention)
            .filter(FraudPrevention.id == fraud_id)
            .first()
        )

    def get_by_transaction_id(self, transaction_id: str) -> Optional[FraudPrevention]:
        return (
            self.db.query(FraudPrevention)
            .filter(FraudPrevention.transaction_id == transaction_id)
            .first()
        )

    def get_by_user_id(self, user_id: str) -> List[FraudPrevention]:
        return (
            self.db.query(FraudPrevention)
            .filter(FraudPrevention.user_id == user_id)
            .order_by(FraudPrevention.created_at.desc())
            .all()
        )

    def update(
        self, fraud_id: str, fraud_data: FraudPreventionUpdate
    ) -> Optional[FraudPrevention]:
        db_fraud = self.get_by_id(fraud_id)
        if not db_fraud:
            return None

        update_data = fraud_data.model_dump(exclude_unset=True)
        if "risk_level" in update_data:
            new_risk_level = RiskLevel(update_data["risk_level"])
            update_data["risk_level"] = new_risk_level
            # Track risk level change
            increment_fraud_attempts(new_risk_level.value)

        for key, value in update_data.items():
            setattr(db_fraud, key, value)

        self.db.commit()
        self.db.refresh(db_fraud)
        return db_fraud

    def block_transaction(
        self, fraud_id: str, reason: str
    ) -> Optional[FraudPrevention]:
        db_fraud = self.get_by_id(fraud_id)
        if not db_fraud:
            return None

        db_fraud.is_blocked = True
        db_fraud.block_reason = reason
        db_fraud.risk_level = RiskLevel.CRITICAL
        db_fraud.attempt_count += 1

        # Track blocked transaction
        increment_blocked_transactions(reason)
        increment_fraud_attempts(RiskLevel.CRITICAL.value)

        self.db.commit()
        self.db.refresh(db_fraud)
        return db_fraud

    def _assess_risk(self, user_id: str) -> RiskLevel:
        # Count recent attempts by this user
        recent_attempts = (
            self.db.query(FraudPrevention)
            .filter(FraudPrevention.user_id == user_id)
            .count()
        )

        if recent_attempts >= 10:
            return RiskLevel.CRITICAL
        elif recent_attempts >= 5:
            return RiskLevel.HIGH
        elif recent_attempts >= 3:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
