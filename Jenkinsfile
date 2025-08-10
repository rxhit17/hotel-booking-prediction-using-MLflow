pipeline {
    agent any

    environment {
        PROJECT_ID = "airy-semiotics-465715-j3" // your GCP project ID
        IMAGE_NAME = "ml-training-app"
        IMAGE_TAG = "latest"
        REGION = "us-central1" // your Cloud Run region
    }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Run Training Pipeline') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        sh """
                            docker run --rm \
                            -e PYTHONPATH=/app \
                            -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                            gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} \
                            sh -c 'mkdir -p /tmp && cp ${GCP_KEY_FILE} /tmp/gcp-key.json && python pipeline/training_pipeline.py'
                        """
                    }
                }
            }
        }

        stage('Push to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        sh """
                            gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
                            gcloud auth configure-docker gcr.io --quiet
                            docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        sh """
                            gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
                            gcloud run deploy ${IMAGE_NAME} \
                                --image gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} \
                                --region ${REGION} \
                                --platform managed \
                                --allow-unauthenticated
                        """
                    }
                }
            }
        }
    }
}
