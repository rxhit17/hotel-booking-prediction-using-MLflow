pipeline {
    agent any

    environment {
        PROJECT_ID = "airy-semiotics-465715-j3"
        IMAGE_NAME = "ml-training-app"
        IMAGE_TAG  = "latest"
        IMAGE_URI  = "gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}"
        SERVICE_NAME = "ml-training-service"
        REGION = "us-central1"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_URI}")
                }
            }
        }

        stage('Push to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    sh """
                        gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
                        gcloud auth configure-docker gcr.io --quiet
                        docker push ${IMAGE_URI}
                    """
                }
            }
        }

        stage('Run Training Pipeline') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    sh """
                        docker run --rm \
                            -v ${GCP_KEY_FILE}:/tmp/gcp-key.json:ro \
                            -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                            -e PYTHONPATH=/app \
                            ${IMAGE_URI} \
                            sh -c "gcloud auth activate-service-account --key-file=/tmp/gcp-key.json && python pipeline/training_pipeline.py"
                    """
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    sh """
                        gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
                        gcloud config set project ${PROJECT_ID}
                        gcloud run deploy ${SERVICE_NAME} \
                            --image ${IMAGE_URI} \
                            --region ${REGION} \
                            --platform managed \
                            --allow-unauthenticated
                    """
                }
            }
        }
    }
}
