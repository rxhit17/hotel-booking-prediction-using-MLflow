# Use an official Python base image
FROM python:slim

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json

# Set workdir
WORKDIR /app

# Copy project files to container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -e .

# Copy credentials file separately (see Jenkins stage below)
COPY gcp-key.json /app/gcp-key.json

# Authenticate with GCP and run training
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://sdk.cloud.google.com | bash && \
    /bin/bash -c "source $HOME/google-cloud-sdk/path.bash.inc && \
    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS && \
    python pipeline/training_pipeline.py"
