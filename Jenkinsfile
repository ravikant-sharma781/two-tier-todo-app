pipeline {
agent any

environment {
    DOCKER_HUB = "ravikants781434"
}

stages {

    stage('Clone Code') {
        steps {
            git 'https://github.com/ravikant-sharma781/two-tier-todo-app.git'
        }
    }

    stage('Build Backend Image') {
        steps {
            sh 'docker build -t $DOCKER_HUB/todo-backend ./backend'
        }
    }

    stage('Build Frontend Image') {
        steps {
            sh 'docker build -t $DOCKER_HUB/todo-frontend ./frontend'
        }
    }

    stage('Login to Docker Hub') {
        steps {
            withCredentials([usernamePassword(
                credentialsId: 'dockerhub-creds',
                usernameVariable: 'USERNAME',
                passwordVariable: 'PASSWORD'
            )]) {
                sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
            }
        }
    }

    stage('Push Images') {
        steps {
            sh 'docker push $DOCKER_HUB/todo-backend'
            sh 'docker push $DOCKER_HUB/todo-frontend'
        }
    }

    stage('Deploy') {
        steps {
            sh 'docker-compose down || true'
            sh 'docker-compose up -d'
        }
    }
}

}

