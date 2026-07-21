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

variable "whatsapp_access_token" {
  description = <<-EOT
    Permanent access token for the WhatsApp Business Platform (Meta Cloud
    API), generated from a System User in Meta Business Settings. Leave
    at the default placeholder until you've finished Meta-side setup — the
    feature stays inert (Secret Manager rejects a truly empty payload, so
    "unset" — not "" — is what keeps this harmless until configured).
  EOT
  type        = string
  sensitive   = true
  default     = "unset"
}

variable "whatsapp_phone_number_id" {
  description = <<-EOT
    The Phone Number ID (not the phone number itself) shown in the
    WhatsApp > API Setup page for your registered business number.
  EOT
  type        = string
  default     = "unset"
}

variable "whatsapp_app_secret" {
  description = "App Secret from the Meta app's Settings > Basic page, used to verify inbound webhook signatures."
  type        = string
  sensitive   = true
  default     = "unset"
}

variable "whatsapp_verify_token" {
  description = <<-EOT
    Arbitrary string you choose and enter twice: once here, once in the
    Meta webhook configuration screen ("Verify token") — Meta echoes it
    back on setup to prove you control the endpoint.
  EOT
  type        = string
  sensitive   = true
  default     = "unset"
}

variable "whatsapp_owner_phone_number" {
  description = <<-EOT
    Your own personal WhatsApp number in E.164 with no leading "+" (e.g.
    972501234567) — inbound messages from this number are routed to Edith
    as chat commands instead of being logged as a client conversation.
  EOT
  type        = string
  default     = "unset"
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
