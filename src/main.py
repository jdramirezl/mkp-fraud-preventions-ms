import json
import logging
import sys
import time
import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import metrics
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from src.database.database import Base, setup_database
from src.metrics import meter, record_request_duration
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

# Initialize OpenTelemetry instrumentation
FastAPIInstrumentor.instrument_app(app)


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

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    # Record request duration
    record_request_duration(duration, str(request.url.path))

    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
        },
    )

    return response


app.include_router(fraud_prevention_router)


# Health check endpoint
@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


# Add metrics endpoint
@app.get("/metrics")
async def get_metrics():
    return {"message": "Metrics are being exported to Google Cloud Monitoring"}
