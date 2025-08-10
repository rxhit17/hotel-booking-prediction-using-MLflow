pipeline {
    agent any
    environment {
        PROJECT_ID = 'My First Project'       // Replace with your GCP project ID
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
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        sh """
                            echo "Running training pipeline inside container..."
                            docker run --rm \
                                -v ${PWD}/keys/gcp-key.json :/tmp/gcp-key.json:ro \
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
                        echo "Pushing Docker image to GCR..."
                        docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:latest
                    """
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                script {
                    sh """
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
