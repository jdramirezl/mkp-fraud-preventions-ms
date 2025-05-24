terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }

  backend "gcs" {
    # Will be provided via -backend-config during terraform init
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "cloud_sql" {
  service                    = "sqladmin.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "cloud_run" {
  service                    = "run.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "monitoring" {
  service                    = "monitoring.googleapis.com"
  disable_dependent_services = true
}

# Create cloud sql instance
resource "google_sql_database_instance" "main" {
  name             = var.cloud_sql_instance_name
  database_version = "POSTGRES_15"
  root_password    = var.db_password
  depends_on       = [google_project_service.cloud_sql]

  settings {
    tier = "db-custom-2-3840"

    # Ip whitelisting
    ip_configuration {
      authorized_networks {
        name  = "home"
        value = var.home_ip
      }
    }
  }

  deletion_protection = false
}

# Create database
resource "google_sql_database" "database" {
  name     = var.db_name
  instance = google_sql_database_instance.main.name
}

# Create database user
resource "google_sql_user" "user" {
  name     = var.db_user
  instance = google_sql_database_instance.main.name
  password = var.db_password
}

# Create service account for Cloud Run
resource "google_service_account" "fraud_prevention" {
  account_id   = "fraud-prevention-sa"
  display_name = "Fraud Prevention Service Account"
}

# Grant Cloud SQL Client role to the service account
resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.fraud_prevention.email}"
}

# Create cloud run service
resource "google_cloud_run_service" "default" {
  name       = "fraud-prevention-api"
  depends_on = [google_sql_database_instance.main, google_sql_database.database, google_sql_user.user]
  location   = var.region

  template {
    spec {
      service_account_name = google_service_account.fraud_prevention.email
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/fraud-prevention/fraud-prevention-api:latest"

        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }

        env {
          name  = "DB_URL"
          value = "postgresql://${var.db_user}:${var.db_password}@/${var.db_name}?host=/cloudsql/${google_sql_database_instance.main.connection_name}"
        }

        env {
          name  = "ENVIRONMENT"
          value = "production"
        }
        
        env {
          name  = "DB_USER"
          value = var.db_user
        }

        env {
          name  = "DB_PASSWORD"
          value = var.db_password
        }

        env {
          name  = "DB_NAME"
          value = var.db_name
        }

        env {
          name  = "DB_HOST"
          value = "/cloudsql/${google_sql_database_instance.main.connection_name}"
        }

        env {
          name  = "DB_PORT"
          value = "5432"
        }
      }
    }

    metadata {
      annotations = {
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.main.connection_name
      }
    }
  }
}

# Make the service public
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.default.location
  project     = var.project_id
  service     = google_cloud_run_service.default.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
