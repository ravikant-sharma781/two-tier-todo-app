pipeline {
agent any

environment {
    DOCKER_HUB = "ravikants781434"
    IMAGE_TAG = "${BUILD_NUMBER}"
}

stages {

    stage('Build Backend Image') {
        steps {
            sh '''
            docker build -t $DOCKER_HUB/todo-backend:$IMAGE_TAG ./backend
            docker tag $DOCKER_HUB/todo-backend:$IMAGE_TAG $DOCKER_HUB/todo-backend:latest
            '''
        }
    }

    stage('Build Frontend Image') {
        steps {
            sh '''
            docker build -t $DOCKER_HUB/todo-frontend:$IMAGE_TAG ./frontend
            docker tag $DOCKER_HUB/todo-frontend:$IMAGE_TAG $DOCKER_HUB/todo-frontend:latest
            '''
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
            sh '''
            docker push $DOCKER_HUB/todo-backend:$IMAGE_TAG
            docker push $DOCKER_HUB/todo-backend:latest

            docker push $DOCKER_HUB/todo-frontend:$IMAGE_TAG
            docker push $DOCKER_HUB/todo-frontend:latest
            '''
        }
    }

stage('Deploy') {
    steps {
        sh '''
        docker-compose down || true
        docker-compose pull
        IMAGE_TAG=$BUILD_NUMBER docker-compose up -d
        '''
    }
}
    stage('Cleanup') {
        steps {
            sh 'docker image prune -f'
        }
    }
}


}

