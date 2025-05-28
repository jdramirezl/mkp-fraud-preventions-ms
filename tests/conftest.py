import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

# Set testing environment before importing the app
os.environ["TESTING"] = "true"

# Create mock for Cloud Monitoring
mock_exporter = MagicMock()
mock_metrics = MagicMock()
mock_metrics.record_attempt = MagicMock()
mock_metrics.record_blocked = MagicMock()

# Patch both the exporter and the metrics module
with patch(
    "opentelemetry.exporter.cloud_monitoring.CloudMonitoringMetricsExporter",
    return_value=mock_exporter,
), patch("src.metrics.record_attempt", mock_metrics.record_attempt), patch(
    "src.metrics.record_blocked", mock_metrics.record_blocked
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
        "record_attempt": mock_metrics.record_attempt,
        "record_blocked": mock_metrics.record_blocked,
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
