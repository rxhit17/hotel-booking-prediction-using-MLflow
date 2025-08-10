FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -e .

# Copy GCP credentials during build
#ARG GOOGLE_APPLICATION_CREDENTIALS_PATH
#COPY ${GOOGLE_APPLICATION_CREDENTIALS_PATH} /tmp/gcp-key.json
#ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json

# Run training pipeline during build
RUN python pipeline/training_pipeline.py

# Set the default command for serving (e.g., Flask API)
CMD ["python", "app.py"]
