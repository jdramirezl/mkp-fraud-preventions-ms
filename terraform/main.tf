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
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "servicenetworking.googleapis.com"
  ])
  
  service = each.key
  disable_on_destroy = false
}

# Reserve IP range for Service Networking
resource "google_compute_global_address" "private_ip_address" {
  name          = "fraud-prevention-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network.id
}

# Create VPC peering connection
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.private_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# Cloud SQL Instance
resource "google_sql_database_instance" "instance" {
  name             = "fraud-prevention-db"
  database_version = "MYSQL_8_0"
  region           = var.region
  
  settings {
    tier              = "db-f1-micro"  # Cheapest tier
    disk_size         = 10  # Minimum size in GB
    availability_type = "ZONAL"  # Cheaper than regional
    
    backup_configuration {
      enabled    = true
      start_time = "23:00"  # Late night backup
      # Minimum backup settings to stay within free tier
      backup_retention_settings {
        retained_backups = 3
        retention_unit   = "COUNT"
      }
    }
    
    ip_configuration {
      ipv4_enabled    = false  # Disable public IP
      private_network = google_compute_network.private_network.id
    }

    # Prevent automatic storage increases
    disk_autoresize = false
    
    # Database flags for optimization
    database_flags {
      name  = "max_connections"
      value = "100"  # Limit concurrent connections
    }
  }

  deletion_protection = true  # Prevent accidental deletion
  
  depends_on = [
    google_project_service.required_apis,
    google_service_networking_connection.private_vpc_connection
  ]
}

# Database
resource "google_sql_database" "database" {
  name     = "fraud_prevention_db"
  instance = google_sql_database_instance.instance.name
}

# Database user
resource "google_sql_user" "user" {
  name     = var.db_user
  instance = google_sql_database_instance.instance.name
  password = var.db_password
}

# VPC network for private connectivity
resource "google_compute_network" "private_network" {
  name                    = "fraud-prevention-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "private_subnetwork" {
  name          = "fraud-prevention-subnetwork"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.private_network.id
  region        = var.region
}

# Cloud Run service
resource "google_cloud_run_service" "fraud_prevention" {
  name     = "fraud-prevention-ms"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/fraud-prevention/fraud-prevention-api:latest"
        
        resources {
          limits = {
            cpu    = "1000m"     # 1 CPU
            memory = "512Mi"     # Minimum viable for Node.js
          }
        }

        env {
          name  = "NODE_ENV"
          value = "production"
        }
        
        env {
          name  = "INSTANCE_CONNECTION_NAME"
          value = google_sql_database_instance.instance.connection_name
        }
        
        env {
          name  = "DB_NAME"
          value = google_sql_database.database.name
        }
        
        env {
          name = "DB_USER"
          value = google_sql_user.user.name
        }
        
        env {
          name = "DB_PASSWORD"
          value = var.db_password
        }
      }

      # Limit concurrent requests
      container_concurrency = 80
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale"      = "2"  # Maximum 2 instances
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.instance.connection_name
        "run.googleapis.com/client-name"        = "cloud-run-microservice"
        "run.googleapis.com/execution-environment" = "gen2"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.required_apis]
}

# Allow unauthenticated access
resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.fraud_prevention.name
  location = google_cloud_run_service.fraud_prevention.location
  role     = "roles/run.invoker"
  member   = "allUsers"
} 