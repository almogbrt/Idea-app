#!/usr/bin/env bash
# Builds the image, pushes it to Artifact Registry, and deploys/updates the
# Cloud Run service. Requires: gcloud CLI authenticated, an Artifact Registry
# repo, and the secrets referenced in cloudrun-service.yaml already created
# in Secret Manager (see README.md "Deploying to Cloud Run").
#
# Usage:
#   PROJECT_ID=my-project REGION=us-central1 ./deploy/deploy.sh

set -euo pipefail

PROJECT_ID="${PROJECT_ID:?Set PROJECT_ID}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-idea-os-edith}"
REPO_NAME="${REPO_NAME:-idea-os}"
IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:$(git rev-parse --short HEAD)"

echo "==> Building image ${IMAGE_TAG}"
docker build -t "${IMAGE_TAG}" .

echo "==> Pushing image"
docker push "${IMAGE_TAG}"

echo "==> Running database migrations against Cloud SQL"
gcloud run jobs deploy "${SERVICE_NAME}-migrate" \
  --image "${IMAGE_TAG}" \
  --region "${REGION}" \
  --project "${PROJECT_ID}" \
  --set-cloudsql-instances "${PROJECT_ID}:${REGION}:idea-os-postgres" \
  --set-secrets "DATABASE_URL=idea-os-database-url:latest" \
  --command "alembic" \
  --args "upgrade,head" \
  --max-retries 1

gcloud run jobs execute "${SERVICE_NAME}-migrate" --region "${REGION}" --project "${PROJECT_ID}" --wait

echo "==> Rendering Cloud Run service manifest"
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
  --region "${REGION}" --project "${PROJECT_ID}" \
  --format="value(status.url)" 2>/dev/null | sed 's#https://##' || echo "PLACEHOLDER_UNTIL_FIRST_DEPLOY")

RENDERED_MANIFEST="$(mktemp)"
sed \
  -e "s#PROJECT_ID#${PROJECT_ID}#g" \
  -e "s#REGION#${REGION}#g" \
  -e "s#IMAGE_TAG#${IMAGE_TAG}#g" \
  -e "s#SERVICE_URL#${SERVICE_URL}#g" \
  deploy/cloudrun-service.yaml > "${RENDERED_MANIFEST}"

echo "==> Deploying to Cloud Run"
gcloud run services replace "${RENDERED_MANIFEST}" --region "${REGION}" --project "${PROJECT_ID}"

gcloud run services add-iam-policy-binding "${SERVICE_NAME}" \
  --region "${REGION}" --project "${PROJECT_ID}" \
  --member="allUsers" --role="roles/run.invoker" || true

echo "==> Done. Service URL:"
gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --project "${PROJECT_ID}" --format="value(status.url)"
