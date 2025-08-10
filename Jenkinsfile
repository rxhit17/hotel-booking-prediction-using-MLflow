pipeline {
    agent any

    environment {
        // Change this to your actual GCP project ID from Google Cloud Console
        GCP_PROJECT_ID = 'my-first-project'

        // Path to your local GCP credentials JSON (use forward slashes)
        GCP_KEY_FILE = 'C:/Users/HP/Downloads/airy-semiotics-465715-j3-8b0b30f13e6f.json'

        IMAGE_NAME = "ml-training-app"
        IMAGE_TAG = "latest"
        IMAGE_URI = "gcr.io/${GCP_PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-token',
                    url: 'https://github.com/rxhit17/hotel-booking-prediction-using-MLflow.git',
                    branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_URI}"
                    sh "docker build -t ${IMAGE_URI} ."
                }
            }
        }

        stage('Train Model in Docker Container') {
            steps {
                script {
                    echo "Running training pipeline inside Docker..."
                    sh """
                        docker run --rm \
                          -v "${GCP_KEY_FILE}:/tmp/gcp-key.json:ro" \
                          -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                          -e PYTHONPATH=/app \
                          ${IMAGE_URI} \
                          python pipeline/training_pipeline.py
                    """
                }
            }
        }

        stage('Push to GCR') {
            steps {
                script {
                    echo "Pushing image to Google Container Registry..."
                    sh "gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}"
                    sh "gcloud auth configure-docker gcr.io --quiet"
                    sh "docker push ${IMAGE_URI}"
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                script {
                    echo "Deploying to Cloud Run..."
                    sh """
                        gcloud run deploy ${IMAGE_NAME} \
                          --image ${IMAGE_URI} \
                          --platform managed \
                          --region asia-south1 \
                          --allow-unauthenticated \
                          --project ${GCP_PROJECT_ID}
                    """
                }
            }
        }
    }
}
