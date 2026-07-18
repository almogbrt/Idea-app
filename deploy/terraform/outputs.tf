output "artifact_registry_repo" {
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.docker.repository_id}"
  description = "Docker repo prefix — matches REPO_NAME in deploy/deploy.sh."
}

output "runtime_service_account_email" {
  value = google_service_account.runtime.email
}

output "deployer_service_account_email" {
  value = google_service_account.deployer.email
}

output "next_step_generate_deployer_key" {
  value = <<-EOT
    Terraform does not export a downloadable key (long-lived credentials
    shouldn't live in state). Generate one and add it to GitHub Actions:

      gcloud iam service-accounts keys create idea-os-deployer-key.json \
        --iam-account=${google_service_account.deployer.email}

    Then: GitHub repo → Settings → Secrets and variables → Actions →
    New repository secret, name GCP_SA_KEY, paste the file contents.
    Delete the local key file afterwards.
  EOT
}
