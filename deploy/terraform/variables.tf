variable "project_id" {
  description = "GCP project ID (the string ID, not the numeric project number)."
  type        = string
}

variable "region" {
  description = "GCP region for all resources."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Base name for the Cloud Run service and related resources."
  type        = string
  default     = "idea-os-edith"
}

variable "owner_email" {
  description = "The single Google account allowed to authenticate into Edith."
  type        = string
}

variable "anthropic_api_key" {
  description = "Anthropic API key (Intent Router)."
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key (embeddings for long-term memory)."
  type        = string
  sensitive   = true
}

variable "google_oauth_client_id" {
  description = "Google OAuth 2.0 Client ID."
  type        = string
  sensitive   = true
}

variable "google_oauth_client_secret" {
  description = "Google OAuth 2.0 Client Secret."
  type        = string
  sensitive   = true
}

variable "token_encryption_key" {
  description = <<-EOT
    Fernet key used to encrypt stored Google OAuth tokens. Generate with:
      python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  EOT
  type        = string
  sensitive   = true
}

variable "neon_database_url" {
  description = <<-EOT
    Postgres connection string from neon.tech (free tier, pgvector supported).
    Paste it exactly as Neon shows it (postgresql://...?sslmode=require) —
    the +asyncpg driver segment is added automatically in secrets.tf.
  EOT
  type        = string
  sensitive   = true
}

variable "upstash_redis_url" {
  description = <<-EOT
    Redis connection string from upstash.com (free tier), TLS form
    (rediss://default:PASSWORD@HOST:PORT) — paste it exactly as shown.
  EOT
  type        = string
  sensitive   = true
}

variable "cloud_run_service_url" {
  description = <<-EOT
    The deployed Cloud Run service's HTTPS URL (e.g.
    https://idea-os-edith-xxxxx.a.run.app), used as the Cloud Scheduler job's
    target for the hourly reminders check. Leave empty on the very first
    `terraform apply` — the service doesn't exist yet. After the first
    `deploy.sh` run, set this (from its printed URL, or
    `gcloud run services describe idea-os-edith --region REGION --format
    'value(status.url)'`) and re-run `terraform apply` to create the
    scheduler job.
  EOT
  type        = string
  default     = ""
}
