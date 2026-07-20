# Secret names match exactly what deploy/cloudrun-service.yaml references via
# secretKeyRef. JWT_SIGNING_KEY is generated here — nothing to type in for
# that. The rest come from Terraform variables (terraform.tfvars, gitignored
# — see terraform.tfvars.example).

resource "random_password" "jwt_signing_key" {
  length  = 64
  special = false
}

# Cloud Scheduler calls the internal reminders endpoint with this in a
# header — there's no logged-in user in that context, so it substitutes for
# a session JWT. Generated here, never typed in by hand.
resource "random_password" "scheduler_shared_secret" {
  length  = 48
  special = false
}

locals {
  # Neon gives you a plain `postgresql://...?sslmode=require` URL. Two fixups
  # for SQLAlchemy+asyncpg: (1) the asyncpg driver needs to be named
  # explicitly in the scheme, (2) asyncpg's connect() only recognizes an
  # `ssl=` kwarg, not the libpq-style `sslmode=` Neon uses — passing
  # `sslmode` through raises `TypeError: connect() got an unexpected keyword
  # argument 'sslmode'`. Neon's default role already has the privileges to
  # `CREATE EXTENSION vector`, so unlike Cloud SQL there's no separate
  # superuser/migrate URL to manage — one secret covers both the app and the
  # one-off migration job.
  database_url = replace(
    replace(var.neon_database_url, "postgresql://", "postgresql+asyncpg://"),
    "sslmode=",
    "ssl="
  )

  secret_values = {
    "idea-os-database-url"               = local.database_url
    "idea-os-redis-url"                  = var.upstash_redis_url
    "idea-os-token-encryption-key"       = var.token_encryption_key
    "idea-os-jwt-signing-key"            = random_password.jwt_signing_key.result
    "idea-os-anthropic-api-key"          = var.anthropic_api_key
    "idea-os-openai-api-key"             = var.openai_api_key
    "idea-os-google-oauth-client-id"     = var.google_oauth_client_id
    "idea-os-google-oauth-client-secret" = var.google_oauth_client_secret
    "idea-os-owner-email"                = var.owner_email
    "idea-os-scheduler-shared-secret"    = random_password.scheduler_shared_secret.result
    "idea-os-whatsapp-access-token"      = var.whatsapp_access_token
    "idea-os-whatsapp-phone-number-id"   = var.whatsapp_phone_number_id
    "idea-os-whatsapp-app-secret"        = var.whatsapp_app_secret
    "idea-os-whatsapp-verify-token"      = var.whatsapp_verify_token
    "idea-os-whatsapp-owner-phone-number" = var.whatsapp_owner_phone_number
  }
}

resource "google_secret_manager_secret" "secret" {
  for_each  = local.secret_values
  secret_id = each.key

  replication {
    auto {}
  }

  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_version" "secret_version" {
  for_each    = local.secret_values
  secret      = google_secret_manager_secret.secret[each.key].id
  secret_data = each.value
}

resource "google_secret_manager_secret_iam_member" "runtime_access" {
  for_each  = local.secret_values
  secret_id = google_secret_manager_secret.secret[each.key].id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}
