import pytest

from src.models.fraud_prevention import RiskLevel
from src.schemas.fraud_prevention import FraudPreventionCreate
from src.services.fraud_prevention import FraudPreventionService


def test_create_fraud_prevention(db_session):
    """Test creating a fraud prevention record through the service."""
    service = FraudPreventionService(db_session)

    # Create test data
    fraud_data = FraudPreventionCreate(
        transaction_id="test-service-tx",
        user_ip="192.168.1.1",
        device_id="test-device",
        user_id="test-service-user",
        additional_data={"test": "data"},
    )

    # Create record
    result = service.create(fraud_data)

    # Verify result
    assert result.transaction_id == fraud_data.transaction_id
    assert result.user_ip == fraud_data.user_ip
    assert result.risk_level == RiskLevel.LOW
    assert not result.is_blocked


def test_get_by_transaction_id(db_session):
    """Test retrieving a fraud prevention record by transaction ID."""
    service = FraudPreventionService(db_session)

    # Create test data
    fraud_data = FraudPreventionCreate(
        transaction_id="test-get-tx", user_ip="192.168.1.1", user_id="test-user"
    )

    # Create record
    created = service.create(fraud_data)

    # Retrieve record
    result = service.get_by_transaction_id(fraud_data.transaction_id)

    # Verify result
    assert result is not None
    assert result.id == created.id
    assert result.transaction_id == fraud_data.transaction_id


def test_block_transaction(db_session):
    """Test blocking a transaction through the service."""
    service = FraudPreventionService(db_session)

    # Create test data
    fraud_data = FraudPreventionCreate(
        transaction_id="test-block-tx", user_ip="192.168.1.1", user_id="test-user"
    )

    # Create and block record
    created = service.create(fraud_data)
    blocked = service.block_transaction(created.id, "Test block reason")

    # Verify result
    assert blocked.is_blocked
    assert blocked.block_reason == "Test block reason"
    assert blocked.risk_level == RiskLevel.CRITICAL


def test_risk_assessment(db_session):
    """Test risk level assessment logic."""
    service = FraudPreventionService(db_session)

    # Create multiple transactions for the same user
    user_id = "risk-assessment-user"

    # First transaction should be LOW risk
    fraud_data = FraudPreventionCreate(
        transaction_id="risk-tx-1", user_ip="192.168.1.1", user_id=user_id
    )
    result = service.create(fraud_data)
    assert result.risk_level == RiskLevel.LOW

    # Create more transactions to increase risk
    for i in range(5):  # Total 6 transactions
        fraud_data = FraudPreventionCreate(
            transaction_id=f"risk-tx-{i+2}", user_ip="192.168.1.1", user_id=user_id
        )
        result = service.create(fraud_data)

    # After 6 transactions, risk should be HIGH
    assert result.risk_level == RiskLevel.HIGH
