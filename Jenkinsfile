pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "airy-semiotics-465715-j3"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/rxhit17/hotel-booking-prediction-using-MLflow.git'
                        ]]
                    )
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setting up Virtual Environment and installing dependencies...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Build and Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing Docker image to GCR...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        # Authenticate with GCP
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        # Build Docker image (no key copied inside)
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        # Push to GCR
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }

        stage('Train Model in Docker Container') {
            steps {
                script {
                    echo 'Training the model inside Docker container...'
                    sh '''
                    docker run --rm \
                        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json \
                        -v ${GOOGLE_APPLICATION_CREDENTIALS}:/tmp/gcp-key.json:ro \
                        gcr.io/${GCP_PROJECT}/ml-project:latest \
                        python train.py
                    '''
                }
            }
        }

    }
}
