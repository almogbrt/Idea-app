resource "google_redis_instance" "cache" {
  name           = "${var.service_name}-redis"
  region         = var.region
  tier           = "BASIC"
  memory_size_gb = var.redis_memory_size_gb

  # DIRECT_PEERING needs no extra Private Service Access setup — simplest
  # option for a single-instance, single-owner deployment.
  authorized_network = google_compute_network.vpc.id
  connect_mode       = "DIRECT_PEERING"
  redis_version      = "REDIS_7_0"

  depends_on = [google_project_service.apis]
}
