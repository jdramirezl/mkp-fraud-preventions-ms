output "cloud_run_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.default.status[0].url
}

output "db_connection_name" {
  description = "The connection name of the Cloud SQL instance"
  value       = google_sql_database_instance.main.connection_name
}

output "db_instance_name" {
  description = "The name of the Cloud SQL instance"
  value       = google_sql_database_instance.main.name
}

output "cloud_sql_public_ip" {
  description = "The public IP address of the Cloud SQL instance"
  value       = google_sql_database_instance.main.public_ip_address
}

