# Example for Python image
FROM python:3.9-slim

# Install gcloud
RUN apt-get update && apt-get install -y curl gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
       | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
       | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y google-cloud-sdk

# Install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
