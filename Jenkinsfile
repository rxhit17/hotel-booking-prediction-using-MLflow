pipeline {
    agent any
    environment {
        PROJECT_ID = 'your-gcp-project-id'
        IMAGE_NAME = 'ml-training-app'
        REGION = 'us-central1'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
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
                            docker run --rm \
                                -v \${GOOGLE_APPLICATION_CREDENTIALS}:/tmp/gcp-key.json \
                                -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
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
                        docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:latest
                    """
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                script {
                    sh """
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
