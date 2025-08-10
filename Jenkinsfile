pipeline {
    agent any

    environment {
        PROJECT_ID = "airy-semiotics-465715-j3"
        IMAGE_NAME = "ml-training-app"
        IMAGE_TAG = "latest"
        REGION = "us-central1"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Run Training Pipeline') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    sh '''
                        docker run --rm \
                        -v "$GCP_KEY_FILE":/tmp/gcp-key.json:ro \
                        -e PYTHONPATH=/app \
                        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                        gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG \
                        python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Push to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    sh '''
                        gcloud auth activate-service-account --key-file="$GCP_KEY_FILE"
                        gcloud auth configure-docker gcr.io --quiet
                        docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    sh '''
                        gcloud auth activate-service-account --key-file="$GCP_KEY_FILE"
                        gcloud run deploy $IMAGE_NAME \
                            --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG \
                            --region $REGION \
                            --platform managed \
                            --allow-unauthenticated
                    '''
                }
            }
        }
    }
}
