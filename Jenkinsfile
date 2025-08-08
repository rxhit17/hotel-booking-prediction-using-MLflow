stage('Build and push Docker image to GCR') {
    steps {
        withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
            script {
                echo 'Building and pushing docker image to GCR..................'

                // Copy the credentials file into the workspace (so Docker can COPY it)
                sh '''
                cp ${GOOGLE_APPLICATION_CREDENTIALS} gcp-key.json
                '''

                sh '''
                export PATH=$PATH:${GCLOUD_PATH}

                gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                gcloud config set project ${GCP_PROJECT}
                gcloud auth configure-docker --quiet

                docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                '''
            }
        }
    }
}
