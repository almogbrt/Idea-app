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

variable "db_tier" {
  description = "Cloud SQL machine tier. db-f1-micro is enough for a single-owner system."
  type        = string
  default     = "db-f1-micro"
}

variable "redis_memory_size_gb" {
  description = "Memorystore Redis instance size in GB (1 is the minimum)."
  type        = number
  default     = 1
}
