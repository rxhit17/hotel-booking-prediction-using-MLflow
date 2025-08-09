# syntax=docker/dockerfile:1.4
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

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -e .

# Use BuildKit secret for credentials during training
RUN --mount=type=secret,id=gcp-key,target=/tmp/gcp-key.json \
    GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
    python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]
