#!/usr/bin/env bash
# The whole cloud side, in the order you'd actually run it.
#
# ⚠️ NOT EXECUTED. Written against current Google Cloud docs but never run —
# there was no billing account available. Do a dry run before you present,
# and expect at least one flag to have moved.
#
#   ./cloud/deploy.sh YOUR_PROJECT_ID

set -euo pipefail

PROJECT="${1:?usage: deploy.sh PROJECT_ID}"
REGION="${REGION:-asia-south1}"
REPO="cosmos"
IMAGE="$REGION-docker.pkg.dev/$PROJECT/$REPO/cosmos:latest"

gcloud config set project "$PROJECT"

echo "── 1. APIs ──────────────────────────────────────────────"
gcloud services enable \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  bigquery.googleapis.com

echo "── 2. The API key goes in Secret Manager, not the image ──"
# Lesson: never bake a key into a container or an env var in source control.
printf '%s' "${GEMINI_API_KEY:?export GEMINI_API_KEY first}" \
  | gcloud secrets create gemini-api-key --data-file=- 2>/dev/null \
  || printf '%s' "$GEMINI_API_KEY" \
     | gcloud secrets versions add gemini-api-key --data-file=-

echo "── 3. BigQuery ──────────────────────────────────────────"
bq --location="$REGION" mk --dataset --force "$PROJECT:cosmos" || true
bq query --use_legacy_sql=false --project_id="$PROJECT" < cloud/schema.sql || true

echo "── 4. Build the image ───────────────────────────────────"
gcloud artifacts repositories create "$REPO" \
  --repository-format=docker --location="$REGION" 2>/dev/null || true
gcloud builds submit --tag "$IMAGE" .

echo "── 5. The batch search: 500 stars, in parallel ──────────"
# Each task reads CLOUD_RUN_TASK_INDEX and takes its own slice.
gcloud run jobs deploy cosmos-search \
  --image "$IMAGE" \
  --region "$REGION" \
  --tasks 500 \
  --parallelism 100 \
  --task-timeout 30m \
  --max-retries 2 \
  --memory 2Gi \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT,BQ_DATASET=cosmos"

echo "   run it:  gcloud run jobs execute cosmos-search --region $REGION"

echo "── 6. The morning report: a service, not a job ──────────"
gcloud run deploy sky-report \
  --image "$IMAGE" \
  --region "$REGION" \
  --command python \
  --args demo/sky_report.py \
  --set-secrets "GEMINI_API_KEY=gemini-api-key:latest" \
  --no-allow-unauthenticated

URL="$(gcloud run services describe sky-report --region "$REGION" --format='value(status.url)')"

echo "── 7. Poke it every morning at 06:00 ────────────────────"
gcloud scheduler jobs create http sky-report-daily \
  --location "$REGION" \
  --schedule "0 6 * * *" \
  --time-zone "Asia/Kolkata" \
  --uri "$URL" \
  --oidc-service-account-email "$(gcloud config get-value account)" \
  2>/dev/null || echo "   (scheduler job already exists)"

echo
echo "done. the scoreboard:"
echo "  bq query --use_legacy_sql=false < cloud/schema.sql"
