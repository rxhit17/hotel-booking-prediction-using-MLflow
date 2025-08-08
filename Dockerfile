# Updated Dockerfile
FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy all files to the container
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

# Set Google Application Credentials ENV variable (will be overridden in Jenkins)
ENV GOOGLE_APPLICATION_CREDENTIALS="/tmp/gcp-key.json"

# Run the training pipeline
#RUN python pipeline/training_pipeline.py

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "application.py"]
