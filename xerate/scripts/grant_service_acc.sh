gcloud functions add-iam-policy-binding xerate_exchange \
  --region us-west1 \
  --member "serviceAccount:scheduler-invoker@development-platform-440808.iam.gserviceaccount.com" \
  --role roles/cloudfunctions.invoker

