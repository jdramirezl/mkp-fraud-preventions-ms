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
        "transactionId": "test-tx-123",
        "userIp": "192.168.1.1",
        "deviceId": "test-device-123",
        "userId": "test-user-123",
        "additionalData": {"amount": 100, "currency": "USD"},
    }

    response = client.post("/api/fraud-preventions", json=test_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["transactionId"] == test_data["transactionId"]
    assert data["userIp"] == test_data["userIp"]
    assert data["riskLevel"] == "low"  # First transaction should be low risk
    assert not data["isBlocked"]
    assert "createdAt" in data
    assert "updatedAt" in data
    assert data["attemptCount"] == 0
    assert data["blockReason"] is None


def test_get_nonexistent_fraud_prevention(client):
    """Test getting a non-existent fraud prevention record."""
    random_id = str(uuid.uuid4())
    response = client.get(f"/api/fraud-preventions/{random_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_block_transaction(client):
    """Test blocking a transaction."""
    # First create a transaction
    test_data = {
        "transactionId": "test-tx-block",
        "userIp": "192.168.1.1",
        "deviceId": "test-device-123",
        "userId": "test-user-123",
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
    assert blocked_data["isBlocked"]
    assert blocked_data["blockReason"] == block_data["reason"]
    assert blocked_data["riskLevel"] == "critical"
    assert blocked_data["attemptCount"] == 1


def test_risk_level_escalation(client):
    """Test that risk level increases with multiple transactions."""
    test_user = "risk-test-user"

    # Create multiple transactions for the same user
    for i in range(6):  # Should escalate to HIGH risk
        test_data = {
            "transactionId": f"test-tx-risk-{i}",
            "userIp": "192.168.1.1",
            "userId": test_user,
        }
        response = client.post("/api/fraud-preventions", json=test_data)
        assert response.status_code == status.HTTP_200_OK

    # Get all transactions for the user
    response = client.get(f"/api/fraud-preventions/user/{test_user}")
    assert response.status_code == status.HTTP_200_OK
    transactions = response.json()

    # The last transaction should have high risk due to multiple attempts
    assert transactions[0]["riskLevel"] == "high"


def test_get_all_fraud_preventions(client):
    """Test getting all fraud prevention records with pagination."""
    # Create a few records
    for i in range(3):
        test_data = {
            "transactionId": f"test-tx-list-{i}",
            "userIp": "192.168.1.1",
            "userId": "test-user-list",
        }
        response = client.post("/api/fraud-preventions", json=test_data)
        assert response.status_code == status.HTTP_200_OK

    # Test pagination
    response = client.get("/api/fraud-preventions?page=1&limit=2")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "pages" in data

    # Check data structure
    assert len(data["data"]) <= 2  # Respects the limit
    assert data["page"] == 1
    assert data["total"] >= 3  # At least our 3 records

    # Check record structure
    record = data["data"][0]
    assert "transactionId" in record
    assert "userIp" in record
    assert "userId" in record
    assert "riskLevel" in record
    assert "isBlocked" in record
    assert "createdAt" in record
    assert "updatedAt" in record
