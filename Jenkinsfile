pipeline {
    agent any

    environment {
        GCP_PROJECT_ID = 'my-first-project'
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
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        sh '''
                            echo "Checking GCP key file..."
                            if [ ! -f "$GCP_KEY_FILE" ]; then
                                echo "ERROR: GCP_KEY_FILE is not a file"
                                exit 1
                            fi
                            echo "Key file looks good:"
                            head -n 3 "$GCP_KEY_FILE"
                        '''

                        echo "Running training pipeline inside Docker..."
                        sh '''
                            docker run --rm \
                              -v "$GCP_KEY_FILE":/tmp/gcp-key.json:ro \
                              -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                              -e PYTHONPATH=/app \
                              ${IMAGE_URI} \
                              python pipeline/training_pipeline.py
                        '''
                    }
                }
            }
        }

        stage('Push to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        echo "Pushing image to Google Container Registry..."
                        sh '''
                            gcloud auth activate-service-account --key-file="$GCP_KEY_FILE"
                            gcloud auth configure-docker gcr.io --quiet
                            docker push ${IMAGE_URI}
                        '''
                    }
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        echo "Deploying to Cloud Run..."
                        sh '''
                            gcloud auth activate-service-account --key-file="$GCP_KEY_FILE"
                            gcloud run deploy ${IMAGE_NAME} \
                              --image ${IMAGE_URI} \
                              --platform managed \
                              --region asia-south1 \
                              --allow-unauthenticated \
                              --project ${GCP_PROJECT_ID}
                        '''
                    }
                }
            }
        }
    }
}
