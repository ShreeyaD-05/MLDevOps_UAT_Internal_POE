def run(String cmd) { if (isUnix()) { sh cmd } else { bat cmd } }
def py() { return isUnix() ? 'venv/bin/python' : 'venv\\Scripts\\python' }

pipeline {
    agent any
    options { timestamps() }
    stages {
        stage('Checkout from GitHub') {
            steps { checkout scm }
        }
        stage('Setup Python venv') {
            steps {
                script {
                    run(isUnix() ? 'python3 -m venv venv' : 'python -m venv venv')
                    run("${py()} -m pip install --upgrade pip")
                    run("${py()} -m pip install -r requirements.txt")
                }
            }
        }
        stage('Run hello.py') {
            steps { script { run("${py()} hello.py") } }
        }
        stage('Pytest') {
            steps { script { run("${py()} -m pytest -v") } }
        }
        stage('Docker Build') {
            steps { script { run('docker build -t hello-mlops-internal-poe:latest .') } }
        }
        stage('Docker Run') {
            steps { script { run('docker run --rm hello-mlops-internal-poe:latest') } }
        }
        stage('Evidently Monitor') {
            steps { script { run("${py()} monitor.py") } }
        }
        stage('Archive Report') {
            steps { archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true }
        }
    }
    post {
        success { echo 'UAT dry run: PASS' }
        failure { echo 'UAT dry run: FAIL' }
    }
}