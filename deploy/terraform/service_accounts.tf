# Two identities, two purposes:
#   runtime  — attached to the Cloud Run service itself, needs only what the
#              running app needs (read its own secrets — Postgres/Redis are
#              external Neon/Upstash endpoints, no GCP-side DB permission
#              needed).
#   deployer — used by CI (deploy/deploy.sh via GitHub Actions) to build/push
#              images, run the migration job, and update the Cloud Run service.
#              Terraform creates the identity and grants it roles; the actual
#              key file is generated out-of-band (see outputs.tf) so a
#              long-lived credential never sits in Terraform state.

resource "google_service_account" "runtime" {
  account_id   = "${var.service_name}-runtime"
  display_name = "IDEA OS Edith — Cloud Run runtime identity"
}

resource "google_service_account" "deployer" {
  account_id   = "${var.service_name}-deployer"
  display_name = "IDEA OS Edith — CI/CD deploy identity"
}

locals {
  runtime_roles = [
    "roles/secretmanager.secretAccessor",
  ]

  deployer_roles = [
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.writer",
    "roles/secretmanager.secretAccessor",
  ]
}

resource "google_project_iam_member" "runtime_roles" {
  for_each = toset(local.runtime_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.runtime.email}"
}

resource "google_project_iam_member" "deployer_roles" {
  for_each = toset(local.deployer_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.deployer.email}"
}
