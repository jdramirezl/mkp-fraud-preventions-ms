import uuid

from fastapi import status


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_create_fraud_prevention(client):
    """Test creating a new fraud prevention record."""
    test_data = {
        "transaction_id": "test-tx-123",
        "user_ip": "192.168.1.1",
        "device_id": "test-device-123",
        "user_id": "test-user-123",
        "additional_data": {"amount": 100, "currency": "USD"},
    }

    response = client.post("/api/fraud-preventions", json=test_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["transaction_id"] == test_data["transaction_id"]
    assert data["user_ip"] == test_data["user_ip"]
    assert data["risk_level"] == "low"  # First transaction should be low risk
    assert not data["is_blocked"]


def test_get_nonexistent_fraud_prevention(client):
    """Test getting a non-existent fraud prevention record."""
    random_id = str(uuid.uuid4())
    response = client.get(f"/api/fraud-preventions/{random_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_block_transaction(client):
    """Test blocking a transaction."""
    # First create a transaction
    test_data = {
        "transaction_id": "test-tx-block",
        "user_ip": "192.168.1.1",
        "device_id": "test-device-123",
        "user_id": "test-user-123",
    }

    create_response = client.post("/api/fraud-preventions", json=test_data)
    assert create_response.status_code == status.HTTP_200_OK
    fraud_id = create_response.json()["id"]

    # Now block the transaction
    block_data = {"reason": "Test blocking transaction"}
    block_response = client.post(
        f"/api/fraud-preventions/{fraud_id}/block", json=block_data
    )

    assert block_response.status_code == status.HTTP_200_OK
    blocked_data = block_response.json()
    assert blocked_data["is_blocked"]
    assert blocked_data["block_reason"] == block_data["reason"]
    assert blocked_data["risk_level"] == "critical"


def test_risk_level_escalation(client):
    """Test that risk level increases with multiple transactions."""
    test_user = "risk-test-user"

    # Create multiple transactions for the same user
    for i in range(6):  # Should escalate to HIGH risk
        test_data = {
            "transaction_id": f"test-tx-risk-{i}",
            "user_ip": "192.168.1.1",
            "user_id": test_user,
        }
        response = client.post("/api/fraud-preventions", json=test_data)
        assert response.status_code == status.HTTP_200_OK

    # Get all transactions for the user
    response = client.get(f"/api/fraud-preventions/user/{test_user}")
    assert response.status_code == status.HTTP_200_OK
    transactions = response.json()

    # The last transaction should have high risk due to multiple attempts
    assert transactions[0]["risk_level"] == "high"
