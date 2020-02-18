# cloud-dataflow-demo

This repository is a Cloud Dataflow demo.

## setup GCP

```sh
# TODO: PROJECT_ID="<project_id>"
gcloud projects create ${PROJECT_ID}

# gcloud beta billing accounts list
# TODO: BILLING_ACCOUNT_ID="<billing_account_id>"
gcloud beta billing projects link ${PROJECT_ID} --billing-account=${BILLING_ACCOUNT_ID}

ENABLED_APIS=`gcloud services list --available | grep -e dataflow -e "Dataflow API" -e "Compute Engine API" -e "Stackdriver Logging API" -e "Cloud Storage" -e "Cloud Storage JSON" -e "BigQuery API" -e "Cloud Pub/Sub" -e "Cloud Datastore" -e "Cloud Resource Manager" | awk -v 'OFS= ' '{print $1}'`
# bigquery.googleapis.com cloudresourcemanager.googleapis.com compute.googleapis.com dataflow.googleapis.com datastore.googleapis.com logging.googleapis.com pubsub.googleapis.com storage-api.googleapis.com storage-component.googleapis.com

# not working
# gcloud services enable ${ENABLED_APIS}
gcloud services enable bigquery.googleapis.com cloudresourcemanager.googleapis.com compute.googleapis.com dataflow.googleapis.com datastore.googleapis.com logging.googleapis.com pubsub.googleapis.com storage-api.googleapis.com storage-component.googleapis.com

# TODO: SERVICE_ACCOUNT_NAME="<service_account_name>"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} --display-name=${SERVICE_ACCOUNT_NAME}
SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" --role='roles/owner'
gcloud iam service-accounts keys create --iam-account ${SERVICE_ACCOUNT_EMAIL} gcp_key.json
# TODO: export GOOGLE_APPLICATION_CREDENTIALS="<google_application_credentials>"

# TODO: BUCKET_NAME="<bucket_name>"
BUCKET_URI="gs://${BUCKET_NAME}"
gsutil mb -l asia ${BUCKET_URI}
```

## install Apache Beam SDK

```sh
pipenv install --python 3.7
pipenv install 'apache-beam[gcp]'
```

## execute WordCount on local machine

```sh
pipenv run python -m apache_beam.examples.wordcount --output outputs
```

## execute WordCount on Cloud Dataflow

```sh
pipenv run python -m apache_beam.examples.wordcount \
  --input gs://dataflow-samples/shakespeare/kinglear.txt \
  --output gs://${BUCKET_NAME}/wordcount/outputs \
  --runner DataflowRunner \
  --project ${PROJECT_ID} \
  --temp_location gs://${BUCKET_NAME}/tmp/
```

## show result using GCP

```sh
# show file list
gsutil ls -lh "gs://${BUCKET_NAME}/wordcount/outputs*"

# show file content
gsutil cat "gs://${BUCKET_NAME}/wordcount/outputs*"
```

## modify pipeline code

```sh
wget https://raw.githubusercontent.com/apache/beam/master/sdks/python/apache_beam/examples/wordcount.py

# modify wordcount.py

pipenv run python wordcount.py --output outputs
```
