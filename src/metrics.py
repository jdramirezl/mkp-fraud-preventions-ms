import os

from opentelemetry import metrics
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

# Create a resource to identify our service
resource = Resource.create(
    {
        "service.name": "fraud-prevention-api",
        "service.namespace": "fraud-prevention",
        "service.instance.id": os.getenv("K_REVISION", "local"),
    }
)

# Initialize the Cloud Monitoring exporter
exporter = CloudMonitoringMetricsExporter(project_id=os.getenv("GOOGLE_CLOUD_PROJECT"))

# Create a metric reader that will periodically export metrics
reader = PeriodicExportingMetricReader(
    exporter, export_interval_millis=60000  # Export every 60 seconds
)

# Create a meter provider with our reader
provider = MeterProvider(metric_readers=[reader], resource=resource)

# Set the global meter provider
metrics.set_meter_provider(provider)

# Create a meter to record metrics
meter = metrics.get_meter("fraud-prevention")

# Define our metrics
fraud_prevention_attempts = meter.create_counter(
    name="fraud_prevention_attempts_total",
    description="Total number of fraud prevention attempts",
    unit="1",
)

fraud_prevention_blocked = meter.create_counter(
    name="fraud_prevention_blocked_total",
    description="Total number of blocked fraud attempts",
    unit="1",
)

fraud_prevention_request_duration = meter.create_histogram(
    name="fraud_prevention_request_duration_seconds",
    description="Duration of fraud prevention requests",
    unit="s",
)


# Helper functions to record metrics
def record_attempt(success: bool, duration: float):
    """Record a fraud prevention attempt with its outcome and duration."""
    fraud_prevention_attempts.add(1, {"success": str(success)})
    fraud_prevention_request_duration.record(duration)


def record_blocked():
    """Record a blocked fraud attempt."""
    fraud_prevention_blocked.add(1)
