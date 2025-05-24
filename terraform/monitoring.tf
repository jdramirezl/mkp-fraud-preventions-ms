# Enable Cloud Monitoring API
resource "google_project_service" "monitoring" {
  service = "monitoring.googleapis.com"
  disable_dependent_services = true
}

# Create a monitoring notification channel (email)
resource "google_monitoring_notification_channel" "email" {
  display_name = "Fraud Prevention Email Alerts"
  type         = "email"
  labels = {
    email_address = var.alert_email_address
  }
  depends_on = [google_project_service.monitoring]
}

# Alert policy for high risk transactions
resource "google_monitoring_alert_policy" "high_risk_transactions" {
  display_name = "High Risk Transactions Alert"
  combiner     = "OR"
  conditions {
    display_name = "High Risk Transaction Rate"
    condition_threshold {
      filter          = "metric.type=\"custom.googleapis.com/fraud_prevention_attempts_total\" AND metric.labels.risk_level=\"HIGH\""
      duration        = "300s"
      comparison     = "COMPARISON_GT"
      threshold_value = 10
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.name]
  depends_on = [google_project_service.monitoring]
}

# Alert for blocked transactions
resource "google_monitoring_alert_policy" "blocked_transactions" {
  display_name = "Blocked Transactions Alert"
  combiner     = "OR"
  conditions {
    display_name = "Blocked Transaction Rate"
    condition_threshold {
      filter          = "metric.type=\"custom.googleapis.com/fraud_prevention_blocked_total\""
      duration        = "300s"
      comparison     = "COMPARISON_GT"
      threshold_value = 5
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.name]
  depends_on = [google_project_service.monitoring]
}

# Alert for high latency
resource "google_monitoring_alert_policy" "high_latency" {
  display_name = "High API Latency Alert"
  combiner     = "OR"
  conditions {
    display_name = "API Latency"
    condition_threshold {
      filter          = "metric.type=\"custom.googleapis.com/fraud_prevention_request_duration_seconds\""
      duration        = "300s"
      comparison     = "COMPARISON_GT"
      threshold_value = 2
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_PERCENTILE_99"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.name]
  depends_on = [google_project_service.monitoring]
}

# Dashboard for fraud prevention metrics
resource "google_monitoring_dashboard" "fraud_prevention" {
  dashboard_json = jsonencode({
    displayName = "Fraud Prevention Dashboard"
    gridLayout = {
      columns = "2"
      widgets = [
        {
          title = "Fraud Prevention Attempts by Risk Level"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"custom.googleapis.com/fraud_prevention_attempts_total\""
                  aggregation = {
                    alignmentPeriod = "60s"
                    perSeriesAligner = "ALIGN_RATE"
                    crossSeriesReducer = "REDUCE_SUM"
                    groupByFields = ["metric.labels.risk_level"]
                  }
                }
              }
            }]
          }
        },
        {
          title = "Blocked Transactions"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"custom.googleapis.com/fraud_prevention_blocked_total\""
                  aggregation = {
                    alignmentPeriod = "60s"
                    perSeriesAligner = "ALIGN_RATE"
                    crossSeriesReducer = "REDUCE_SUM"
                    groupByFields = ["metric.labels.reason"]
                  }
                }
              }
            }]
          }
        },
        {
          title = "API Latency (p99)"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"custom.googleapis.com/fraud_prevention_request_duration_seconds\""
                  aggregation = {
                    alignmentPeriod = "60s"
                    perSeriesAligner = "ALIGN_PERCENTILE_99"
                    crossSeriesReducer = "REDUCE_MEAN"
                    groupByFields = ["metric.labels.endpoint"]
                  }
                }
              }
            }]
          }
        }
      ]
    }
  })
  depends_on = [google_project_service.monitoring]
} 