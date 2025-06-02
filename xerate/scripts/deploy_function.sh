gcloud functions deploy xerate_exchange \
  --runtime python312 \
  --trigger-http \
  --entry-point run_upload \
  --no-allow-unauthenticated \
  --region=us-west1

