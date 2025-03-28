gcloud builds submit --tag gcr.io/development-platform-440808/backend backend

docker build -t backend backend
docker tag backend gcr.io/development-platform-440808/backend
docker push gcr.io/development-platform-440808/backend

