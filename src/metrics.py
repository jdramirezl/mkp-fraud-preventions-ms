from prometheus_client import Counter, Histogram

# Initialize metrics
FRAUD_ATTEMPTS = Counter(
    "fraud_prevention_attempts_total",
    "Total number of fraud prevention checks",
    ["risk_level"],
)

BLOCKED_TRANSACTIONS = Counter(
    "fraud_prevention_blocked_total", "Total number of blocked transactions", ["reason"]
)

REQUEST_LATENCY = Histogram(
    "fraud_prevention_request_duration_seconds",
    "Request latency in seconds",
    ["endpoint"],
)
