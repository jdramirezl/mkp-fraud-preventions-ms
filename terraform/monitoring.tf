# Create monitoring dashboard
resource "google_monitoring_dashboard" "fraud_prevention" {
  dashboard_json = jsonencode({
    displayName = "Fraud Prevention Dashboard"
    gridLayout = {
      columns = 2
      widgets = [
        {
          title = "Fraud Prevention Attempts (Total)"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type = \"custom.googleapis.com/fraud_prevention_attempts_total\""
                  aggregation = {
                    alignmentPeriod   = "60s"
                    perSeriesAligner  = "ALIGN_RATE"
                    crossSeriesReducer = "REDUCE_SUM"
                    groupByFields = ["metric.label.success"]
                  }
                }
              }
            }]
            timeshiftDuration = "0s"
            yAxis = {
              label = "Attempts per second"
              scale = "LINEAR"
            }
          }
        },
        {
          title = "Blocked Transactions"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type = \"custom.googleapis.com/fraud_prevention_blocked_total\""
                  aggregation = {
                    alignmentPeriod   = "60s"
                    perSeriesAligner  = "ALIGN_RATE"
                    crossSeriesReducer = "REDUCE_SUM"
                  }
                }
              }
            }]
            timeshiftDuration = "0s"
            yAxis = {
              label = "Blocks per second"
              scale = "LINEAR"
            }
          }
        },
        {
          title = "Request Duration Distribution"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type = \"custom.googleapis.com/fraud_prevention_request_duration_seconds\""
                  aggregation = {
                    alignmentPeriod   = "60s"
                    perSeriesAligner  = "ALIGN_PERCENTILE_99"
                  }
                }
              }
            }]
            timeshiftDuration = "0s"
            yAxis = {
              label = "Duration (seconds)"
              scale = "LINEAR"
            }
          }
        },
        {
          title = "Success Rate"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type = \"custom.googleapis.com/fraud_prevention_attempts_total\" AND metric.label.success = \"true\""
                  aggregation = {
                    alignmentPeriod   = "60s"
                    perSeriesAligner  = "ALIGN_RATE"
                    crossSeriesReducer = "REDUCE_SUM"
                  }
                }
              }
            }]
            timeshiftDuration = "0s"
            yAxis = {
              label = "Success rate"
              scale = "LINEAR"
            }
          }
        }
      ]
    }
  })
}


# resource "google_monitoring_alert_policy" "high_latency" {
#   display_name = "High Request Latency"
#   combiner     = "OR"
#   conditions {
#     display_name = "P99 latency > 2 seconds"
#     condition_threshold {
#       filter          = "metric.type = \"custom.googleapis.com/fraud_prevention_request_duration_seconds\" AND resource.type = \"cloud_run_revision\""
#       duration        = "60s"
#       comparison     = "COMPARISON_GT"
#       threshold_value = 2
#       aggregations {
#         alignment_period   = "60s"
#         per_series_aligner = "ALIGN_PERCENTILE_99"
#       }
#     }
#   }

#   notification_channels = []  # Add notification channels if needed
#   alert_strategy {
#     auto_close = "3600s"
#   }
# } 