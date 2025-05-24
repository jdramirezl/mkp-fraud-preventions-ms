variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
  default     = "us-central1"  # Free tier region
}

variable "container_image" {
  description = "The container image to deploy (from GHCR)"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_user" {
  description = "Database user name"
  type        = string
}

variable "db_password" {
  description = "Database user password"
  type        = string
  sensitive   = true
} 

variable "cloud_sql_instance_name" {
  description = "The name of the Cloud SQL instance"
  type        = string
}

variable "home_ip" {
  description = "The IP address to whitelist for the database"
  type        = string
}

variable "alert_email_address" {
  description = "Email address to receive monitoring alerts"
  type        = string
}