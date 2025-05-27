import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

# Set testing environment before importing the app
os.environ["TESTING"] = "true"

from src.database.database import Base, get_db, setup_database
from src.main import app

# Initialize test database
engine, SessionLocal = setup_database()
Base.metadata.create_all(bind=engine)


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


@pytest.fixture(autouse=True)
def mock_cloud_monitoring():
    """Mock Cloud Monitoring metrics for all tests."""
    with patch(
        "opentelemetry.exporter.cloud_monitoring.CloudMonitoringMetricsExporter",
        autospec=True,
    ) as mock_exporter:
        # Create a mock exporter instance
        mock_instance = MagicMock()
        mock_exporter.return_value = mock_instance
        yield mock_instance


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
