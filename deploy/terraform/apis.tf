# Every API the stack touches. Enabling these can take a minute or two on a
# brand-new project — Terraform waits for it before creating dependent resources.
locals {
  required_apis = [
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "redis.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "vpcaccess.googleapis.com",
    "servicenetworking.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "drive.googleapis.com",
    "gmail.googleapis.com",
    "calendar-json.googleapis.com",
    "sheets.googleapis.com",
  ]
}

resource "google_project_service" "apis" {
  for_each = toset(local.required_apis)

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}
