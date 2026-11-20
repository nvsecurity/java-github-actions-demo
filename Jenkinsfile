pipeline {
    agent any

    environment {
        NIGHTVISION_TOKEN   = credentials('nightvision-token')
        NIGHTVISION_TARGET  = 'javaspringvulny-api'
        NIGHTVISION_PROJECT = 'my-project'
        NIGHTVISION_AUTH    = 'javaspringvulny-api'
    }

    stages {
        stage('Check out the code') {
            steps {
                checkout scm
            }
        }

        stage('Install the NightVision CLI') {
            steps {
                sh 'curl -L https://downloads.nightvision.net/binaries/latest/nightvision_latest_linux_amd64.tar.gz -q | tar -xz'
            }
        }

        stage('Extract the API specification') {
            steps {
                sh './nightvision openapi extract . --target "$NIGHTVISION_TARGET" --project "$NIGHTVISION_PROJECT" --lang java'
            }
        }

        stage('Start the application') {
            steps {
                sh 'docker compose up -d; sleep 15'
            }
        }

        stage('Scan the API') {
            steps {
                sh '''
                    ./nightvision scan "$NIGHTVISION_TARGET" --project "$NIGHTVISION_PROJECT" --auth "$NIGHTVISION_AUTH" > scan-results.txt
                    ./nightvision export sarif -s "$(head -n 1 scan-results.txt)" --openapi-file openapi-spec.yml
                '''
            }
        }

        stage('Publish the findings') {
            steps {
                recordIssues tool: sarif(pattern: 'results.sarif')
            }
        }
    }

    post {
        always {
            sh 'docker compose down'
        }
    }
}
