# Hourly check for due task/client reminders. The Cloud Run service is
# deployed publicly reachable (service_accounts.tf / deploy.sh grant
# `roles/run.invoker` to `allUsers` — auth happens inside the app, not via
# Cloud Run IAM), so this hits the internal endpoint over plain HTTPS with a
# shared-secret header rather than an OIDC token.
#
# Gated on `cloud_run_service_url` being set: on the very first `terraform
# apply` the Cloud Run service doesn't exist yet (deploy.sh creates it), so
# this resource is skipped until a second apply once the URL is known.
resource "google_cloud_scheduler_job" "check_reminders" {
  count = var.cloud_run_service_url != "" ? 1 : 0

  name      = "${var.service_name}-check-reminders"
  project   = var.project_id
  region    = var.region
  schedule  = "0 * * * *"
  time_zone = "Etc/UTC"

  http_target {
    uri         = "${var.cloud_run_service_url}/api/v1/internal/reminders/run"
    http_method = "POST"
    headers = {
      "X-Scheduler-Secret" = random_password.scheduler_shared_secret.result
    }
  }

  depends_on = [google_project_service.apis]
}
