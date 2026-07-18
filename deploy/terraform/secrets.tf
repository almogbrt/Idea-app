# Secret names match exactly what deploy/cloudrun-service.yaml references via
# secretKeyRef. DATABASE_URL, REDIS_URL, and JWT_SIGNING_KEY are fully derived
# here — nothing to type in for those. The rest come from Terraform variables
# (terraform.tfvars, gitignored — see terraform.tfvars.example).

resource "random_password" "jwt_signing_key" {
  length  = 64
  special = false
}

locals {
  redis_url = "redis://${google_redis_instance.cache.host}:${google_redis_instance.cache.port}/0"

  secret_values = {
    "idea-os-database-url"               = local.database_url
    "idea-os-database-url-migrate"       = local.migrate_database_url
    "idea-os-redis-url"                  = local.redis_url
    "idea-os-token-encryption-key"       = var.token_encryption_key
    "idea-os-jwt-signing-key"            = random_password.jwt_signing_key.result
    "idea-os-anthropic-api-key"          = var.anthropic_api_key
    "idea-os-openai-api-key"             = var.openai_api_key
    "idea-os-google-oauth-client-id"     = var.google_oauth_client_id
    "idea-os-google-oauth-client-secret" = var.google_oauth_client_secret
    "idea-os-owner-email"                = var.owner_email
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
