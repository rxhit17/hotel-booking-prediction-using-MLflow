# Use a base image with more libs for faster installs
FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps for LightGBM + kiwisolver speed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Pass in GCP credentials during build
ARG GOOGLE_APPLICATION_CREDENTIALS_PATH
COPY ${GOOGLE_APPLICATION_CREDENTIALS_PATH} /tmp/gcp-key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json

# Install Python dependencies with prefer-binary for kiwisolver
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -e .

# Train the model during build (credentials available)
RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]
