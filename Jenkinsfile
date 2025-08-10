pipeline {
    agent any
    environment {
        PROJECT_ID = 'your-gcp-project-id'  // Apna GCP Project ID dal
        IMAGE_NAME = 'ml-training-app'
        REGION = 'us-central1'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        echo "Building Docker image..."
                        docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME:latest .
                    """
                }
            }
        }

        stage('Train Model in Docker Container') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        sh """
                            echo "Running training pipeline inside container..."
                            docker run --rm \
                                -v \${GOOGLE_APPLICATION_CREDENTIALS}:/tmp/gcp-key.json \
                                -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                                -e PYTHONPATH=/app \
                                gcr.io/$PROJECT_ID/$IMAGE_NAME:latest \
                                python pipeline/training_pipeline.py
                        """
                    }
                }
            }
        }

        stage('Push to GCR') {
            steps {
                script {
                    sh """
                        echo "Pushing Docker image to Google Container Registry..."
                        gcloud auth configure-docker --quiet
                        docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:latest
                    """
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        sh """
                            echo "Activating GCP service account..."
                            gcloud auth activate-service-account --key-file=\${GOOGLE_APPLICATION_CREDENTIALS}

                            echo "Deploying to Cloud Run..."
                            gcloud run deploy $IMAGE_NAME \
                                --image gcr.io/$PROJECT_ID/$IMAGE_NAME:latest \
                                --region $REGION \
                                --platform managed \
                                --allow-unauthenticated
                        """
                    }
                }
            }
        }
    }
}
