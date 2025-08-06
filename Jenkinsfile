pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT ="airy-semiotics-465715-j3"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning github repo to jenkins'){
            steps{
                script{
                    echo 'cloning Github repo to Jenkins........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/rxhit17/hotel-booking-prediction-using-MLflow.git']])
                }
            }
        }

        
        stage('setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'setting up our Virtual Environment and Installing dependancies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip 
                    pip install -e .
                    '''
                }
            }
        }


        stage('Bulding and pushing docker image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo'Bulding and pushing docker image to GCR..................'
                        sh'''
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
        
    }
}