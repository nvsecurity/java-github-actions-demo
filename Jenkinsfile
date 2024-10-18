pipeline {
    agent any

    environment {
        NIGHTVISION_TOKEN = credentials('nightvision-token')
        NIGHTVISION_TARGET = 'javaspringvulny-api'
        NIGHTVISION_AUTH = 'javaspringvulny-api'
    }

    stages {
        stage('Clone Code') {
            steps {
                checkout scm
            }
        }

        stage('Install NightVision') {
            steps {
                script {
                    sh 'wget -c https://downloads.nightvision.net/binaries/latest/nightvision_latest_linux_amd64.tar.gz -O - | tar -xz'
                    
                    sh 'python3 -m pip install --break-system-packages semgrep'
                }
            }
        }

        stage('Extract API Documentation from Code') {
            steps {
                script {
                    sh """
                   
                    ./nightvision swagger extract . -t "${env.NIGHTVISION_TARGET}" --lang spring || true
                    if [ ! -e openapi-spec.yml ]; then
                        cp backup-openapi-spec.yml openapi-spec.yml
                    fi
                    """
                }
            }
        }



        stage('Start the App') {
            steps {
                script {
                    sh 'docker compose up -d; sleep 10'
                }
            }
        }

        stage('Scan the API') {
            steps {
                script {
                    sh """
                    
                    ./nightvision scan "${env.NIGHTVISION_TARGET}" --auth "${env.NIGHTVISION_AUTH}" > scan-results.txt
                    ./nightvision export sarif -s \$(head -n 1 scan-results.txt) --swagger-file openapi-spec.yml > results.sarif
                    """

                }
            }
        }

        stage('Upload SARIF file to Jenkins using Warnings Plugin') {
            steps {
                script {
                    // ensure the file exists and then publish it using the Warnings Next Generation Plugin
                    sh 'test -f results.sarif'
                    recordIssues tool: sarif(pattern: 'results.sarif')
                }
            }
        }
    }

    post {
        always {
            // cleanup
            sh 'docker compose down'
        }
    }
}
