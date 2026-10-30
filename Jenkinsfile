def run(String cmd) { if (isUnix()) { sh cmd } else { bat cmd } }
def py() { return isUnix() ? 'venv/bin/python' : 'venv\\Scripts\\python' }
/*pipline code */
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
                    if (!fileExists('venv')) {
                        run("${basePy()} -m venv venv")
                    } else {
                        echo 'venv already exists - skipping creation'
                    }
                    if (!fileExists('venv/.deps_installed')) {
                        run("${py()} -m pip install -r requirements.txt")
                        writeFile file: 'venv/.deps_installed', text: 'ok'
                    } else {
                        echo 'Packages already installed - skipping pip install'
                    }
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