import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

# Set testing environment before importing the app
os.environ["TESTING"] = "true"

# Mock the metrics functions before importing the app
mock_record_attempt = MagicMock()
mock_record_blocked = MagicMock()

with patch("src.services.fraud_prevention.record_attempt", mock_record_attempt), patch(
    "src.services.fraud_prevention.record_blocked", mock_record_blocked
):
    from src.database.database import Base, get_db, setup_database
    from src.main import app

# Initialize test database
engine, SessionLocal = setup_database()
Base.metadata.create_all(bind=engine)


@pytest.fixture
def metrics_mocks():
    """Return the metric mock functions for assertions in tests."""
    return {
        "record_attempt": mock_record_attempt,
        "record_blocked": mock_record_blocked,
    }


@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with a test database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
