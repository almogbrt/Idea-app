resource "google_artifact_registry_repository" "docker" {
  repository_id = "idea-os"
  location      = var.region
  format        = "DOCKER"
  description   = "IDEA OS / Edith container images"

  depends_on = [google_project_service.apis]
}
