pipeline {
	agent any
	environment {
        DOCKERHUB_CREDENTIAL_ID = 'cicd-jenkins-test-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'akmalzakia/iris-cicd-test'
    }
	stages {
		stage('Clone Repository') {
			steps {
				script {
					echo 'Cloning Repository'
					checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'iris-cicd-test-cred', url: 'https://github.com/akmalzakia/model_iris_cicd_test']])
				}
			}
		}
		stage('Lint Code') {
			steps {
				script {
					echo 'Linting Python Code...'
					sh "python -m pip install --break-system-packages -r requirements.txt"
					sh "pylint app.py train.py --output=pylint-report.txt --exit-zero"
					sh "flake8 app.py train.py --ignore=E501,E302 --output-file=flake8-report.txt"
					sh "black app.py train.py"
				}
			}
		}
		stage('Trivy FS Scan') {
			steps {
				script {
					echo 'Scannning Filesystem with Trivy...'
					sh "trivy fs --format table -o trivy-fs-report.html"
				}
			}
		}
		stage('Build Docker Image') {
			steps {
				script {
					echo 'Building Docker Image...'
					dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest") 
				}
			}
		}
		stage('Trivy Docker Image Scan') {
			steps {
				script {
					echo 'Scanning Docker Image with Trivy...'
					sh "trivy image --format table -o trivy-image-report.html ${DOCKERHUB_REPOSITORY}:latest"
				}
			}
		}
		stage('Push Docker Image') {
			steps {
				script {
					echo 'Pushing Docker Image to DockerHub...'
					docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}"){
						dockerImage.push('latest')
					}
				}
			}
		}
	}
}