from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.schemas.fraud_prevention import (
    BlockTransactionRequest,
    FraudPreventionCreate,
    FraudPreventionResponse,
    FraudPreventionUpdate,
)
from src.services.fraud_prevention import FraudPreventionService

router = APIRouter(prefix="/api/fraud-preventions", tags=["fraud-prevention"])


@router.post("", response_model=FraudPreventionResponse)
def create_fraud_prevention(
    fraud_prevention: FraudPreventionCreate,
    db: Session = Depends(get_db),
):
    service = FraudPreventionService(db)
    return service.create(fraud_prevention)


@router.get("", response_model=Dict[str, Any])
def get_all_fraud_preventions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = FraudPreventionService(db)
    skip = (page - 1) * limit
    frauds, total = service.get_all(skip=skip, limit=limit)

    return {
        "data": [FraudPreventionResponse.model_validate(fraud) for fraud in frauds],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/{fraud_id}", response_model=FraudPreventionResponse)
def get_fraud_prevention(fraud_id: str, db: Session = Depends(get_db)):
    service = FraudPreventionService(db)
    fraud = service.get_by_id(fraud_id)
    if not fraud:
        raise HTTPException(status_code=404, detail="Fraud prevention record not found")
    return fraud


@router.get("/transaction/{transaction_id}", response_model=FraudPreventionResponse)
def get_by_transaction_id(transaction_id: str, db: Session = Depends(get_db)):
    service = FraudPreventionService(db)
    fraud = service.get_by_transaction_id(transaction_id)
    if not fraud:
        raise HTTPException(status_code=404, detail="Fraud prevention record not found")
    return fraud


@router.get("/user/{user_id}", response_model=List[FraudPreventionResponse])
def get_by_user_id(user_id: str, db: Session = Depends(get_db)):
    service = FraudPreventionService(db)
    frauds = service.get_by_user_id(user_id)
    return [FraudPreventionResponse.model_validate(fraud) for fraud in frauds]


@router.patch("/{fraud_id}", response_model=FraudPreventionResponse)
def update_fraud_prevention(
    fraud_id: str, fraud_data: FraudPreventionUpdate, db: Session = Depends(get_db)
):
    service = FraudPreventionService(db)
    fraud = service.update(fraud_id, fraud_data)
    if not fraud:
        raise HTTPException(status_code=404, detail="Fraud prevention record not found")
    return fraud


@router.post("/{fraud_id}/block", response_model=FraudPreventionResponse)
def block_transaction(
    fraud_id: str, block_data: BlockTransactionRequest, db: Session = Depends(get_db)
):
    service = FraudPreventionService(db)
    fraud = service.block_transaction(fraud_id, block_data.reason)
    if not fraud:
        raise HTTPException(status_code=404, detail="Fraud prevention record not found")
    return fraud
