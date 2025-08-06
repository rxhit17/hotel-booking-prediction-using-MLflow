pipeline{
    agent any

    stages{
        stage('Cloning github repo to jenkins'){
            steps{
                script{
                    echo 'cloning Github repo to Jenkins........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/rxhit17/hotel-booking-prediction-using-MLflow.git']])
                }
            }
        }
        
    }
}