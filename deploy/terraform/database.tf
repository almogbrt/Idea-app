resource "random_password" "db_password" {
  length  = 32
  special = false
}

resource "random_password" "db_superuser_password" {
  length  = 32
  special = false
}

resource "google_sql_database_instance" "postgres" {
  name             = "${var.service_name}-postgres"
  region           = var.region
  database_version = "POSTGRES_16"

  settings {
    tier              = var.db_tier
    availability_type = "ZONAL"
    disk_autoresize   = true

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
  }

  deletion_protection = true

  depends_on = [google_project_service.apis]
}

resource "google_sql_database" "app_db" {
  name     = "idea_os"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "app_user" {
  name     = "idea_os"
  instance = google_sql_database_instance.postgres.name
  password = random_password.db_password.result
}

# `postgres` is Cloud SQL's built-in superuser role. `idea_os` (an ordinary
# user, no cloudsqlsuperuser) cannot run `CREATE EXTENSION vector` — Alembic
# migration 0001 needs it — so the one-off migration Cloud Run Job connects
# as `postgres` (see `migrate_database_url` below and deploy.sh), while the
# running app always uses the least-privilege `idea_os` DATABASE_URL.
resource "google_sql_user" "superuser" {
  name     = "postgres"
  instance = google_sql_database_instance.postgres.name
  password = random_password.db_superuser_password.result
}

locals {
  # Cloud SQL Auth Proxy (Unix socket) connection string, matching the
  # `cloudsql-instances` annotation in deploy/cloudrun-service.yaml.
  database_url = "postgresql+asyncpg://${google_sql_user.app_user.name}:${random_password.db_password.result}@/${google_sql_database.app_db.name}?host=/cloudsql/${google_sql_database_instance.postgres.connection_name}"

  migrate_database_url = "postgresql+asyncpg://${google_sql_user.superuser.name}:${random_password.db_superuser_password.result}@/${google_sql_database.app_db.name}?host=/cloudsql/${google_sql_database_instance.postgres.connection_name}"
}
