import json
import logging
import sys
import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import MetricServiceClient
from prometheus_client import generate_latest
from starlette.responses import Response

from src.database.database import Base, setup_database
from src.metrics import REQUEST_LATENCY
from src.routes.fraud_prevention import router as fraud_prevention_router


# Configure logging for GCP
class GCPJsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        if record.exc_info:
            log_entry["error"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


# Set up root logger
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(GCPJsonFormatter())
logger.handlers = [handler]
logger.setLevel(logging.INFO)

# Initialize database
engine, _ = setup_database()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fraud Prevention API",
    description="API for fraud prevention and risk assessment",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
        self._client = None

    @property
    def client(self) -> MetricServiceClient:
        if self._client is None:
            self._client = monitoring_v3.MetricServiceClient()
        return self._client

    async def __call__(self, request: Request, call_next):
        path = request.url.path

        # Skip metrics endpoint itself
        if path == "/metrics":
            return await call_next(request)

        # Time the request
        with REQUEST_LATENCY.labels(endpoint=path).time():
            response = await call_next(request)

        return response


app.add_middleware(MetricsMiddleware)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(
        "Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_host": request.client.host if request.client else None,
        },
    )

    response = await call_next(request)

    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
        },
    )

    return response


# Include routers
app.include_router(fraud_prevention_router)


# Health check endpoint
@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


# Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
