gcloud scheduler jobs create http upload-job \
  --schedule "0 0 * * *" \
  --http-method POST \
  --uri "https://us-west1-development-platform-440808.cloudfunctions.net/xerate_exchange" \
  --oidc-service-account-email scheduler-invoker@development-platform-440808.iam.gserviceaccount.com \
  --oidc-token-audience "https://us-west1-development-platform-440808.cloudfunctions.net/xerate_exchange" \
  --time-zone "Asia/Singapore" \
  --location asia-southeast1


