# Every-5-minutes check for due task/client reminders (needs to be tighter
# than hourly so the "task ending in 10 minutes" email actually lands with
# some lead time — worst case with a 5-minute sweep is ~5 minutes' notice,
# not 10). The Cloud Run service is deployed publicly reachable
# (service_accounts.tf / deploy.sh grant `roles/run.invoker` to `allUsers` —
# auth happens inside the app, not via Cloud Run IAM), so this hits the
# internal endpoint over plain HTTPS with a shared-secret header rather than
# an OIDC token.
#
# Gated on `cloud_run_service_url` being set: on the very first `terraform
# apply` the Cloud Run service doesn't exist yet (deploy.sh creates it), so
# this resource is skipped until a second apply once the URL is known.
resource "google_cloud_scheduler_job" "check_reminders" {
  count = var.cloud_run_service_url != "" ? 1 : 0

  name      = "${var.service_name}-check-reminders"
  project   = var.project_id
  region    = var.region
  schedule  = "*/5 * * * *"
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

# Once-daily accountability review at 21:00 Israel Daylight Time (UTC+3, the
# current offset) — reports which of today's Tasks actually got done vs not,
# plus today's calendar events as a plain FYI list. Fixed UTC cron, same as
# the reminders job above: it will drift by an hour across DST changes
# (roughly late March / late October) rather than tracking Israel time
# exactly — acceptable for a nudge email, not worth a timezone-aware
# scheduler for a single-user app.
resource "google_cloud_scheduler_job" "send_daily_review" {
  count = var.cloud_run_service_url != "" ? 1 : 0

  name      = "${var.service_name}-send-daily-review"
  project   = var.project_id
  region    = var.region
  schedule  = "0 18 * * *"
  time_zone = "Etc/UTC"

  http_target {
    uri         = "${var.cloud_run_service_url}/api/v1/internal/daily-review/run"
    http_method = "POST"
    headers = {
      "X-Scheduler-Secret" = random_password.scheduler_shared_secret.result
    }
  }

  depends_on = [google_project_service.apis]
}
