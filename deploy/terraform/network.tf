# Cloud SQL is reached via the Cloud Run built-in Cloud SQL Auth Proxy
# (the `cloudsql-instances` annotation, Unix socket — no VPC needed for that).
# Memorystore Redis only supports private IP though, so Cloud Run needs a
# Serverless VPC Access connector into the same network Redis sits in.

resource "google_compute_network" "vpc" {
  name                    = "${var.service_name}-vpc"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.apis]
}

# Memorystore (DIRECT_PEERING, below) attaches to the VPC itself, and the
# connector below carves out its own dedicated /28 — neither needs a
# general-purpose subnet, so there isn't one here.

resource "google_vpc_access_connector" "connector" {
  name          = "${var.service_name}-conn"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.10.1.0/28"
  min_instances = 2
  max_instances = 3
}
