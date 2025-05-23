def remote = [:]
def git_url = "git@github.com:chesnokov70/bookshop.git"

pipeline {
  agent any

  parameters {
    gitParameter(name: 'revision', type: 'PT_BRANCH')
  }

  environment {
    EC2_USER = "ubuntu"
    REGISTRY = "chesnokov70/bookshop"
    HOST = '54.92.169.46'
    SSH_KEY = credentials('ssh_instance_key')       // EC2 key
    TOKEN = credentials('hub_token')                // Docker Hub token
  }

  stages {

    stage('Configure SSH Remote') {
      steps {
        withCredentials([sshUserPrivateKey(credentialsId: 'ssh_instance_key', keyFileVariable: 'private_key', usernameVariable: 'username')]) {
          script {
            remote.name = "EC2"
            remote.host = "${HOST}"
            remote.user = "${username}"
            remote.identity = readFile("${private_key}")
            remote.allowAnyHosts = true
          }
        }
      }
    }

    stage('Get Git Revision') {
      steps {
        script {
          def revision = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          echo "Current Git revision: ${revision}"
        }
      }
    }

    stage('Checkout Code') {
      steps {
        checkout([$class: 'GitSCM',
                  branches: [[name: "${params.revision}"]],
                  userRemoteConfigs: [[credentialsId: 'ssh_github_access_key', url: "${git_url}"]]
        ])
      }
    }

    stage ('Build and push') {
      steps {
        script {
         sh """ 
         docker login -u chesnokov70 -p $TOKEN
         docker build -t "${env.REGISTRY}:${env.BUILD_ID}" .
         docker push "${env.REGISTRY}:${env.BUILD_ID}"
         """
        }
      }
    }

    stage('Copy Files to EC2') {
      steps {
        sshagent(credentials: ['ssh_instance_key']) {
          sh """
         mkdir -p /var/lib/jenkins/.ssh
         ssh-keyscan -H ${HOST} >> /var/lib/jenkins/.ssh/known_hosts
         chmod 600 /var/lib/jenkins/.ssh/known_hosts        

         scp /var/lib/jenkins/workspace/My_Lessons_Folder/bookshop/docker-compose.tmpl ${EC2_USER}@${HOST}:/home/ubuntu/
         scp /var/lib/jenkins/workspace/My_Lessons_Folder/bookshop/promtail-config.yaml ${EC2_USER}@${HOST}:/home/ubuntu/
         scp -r /var/lib/jenkins/workspace/My_Lessons_Folder/bookshop/nginx ${EC2_USER}@${HOST}:/home/ubuntu/ 
         ssh ${EC2_USER}@${HOST} 'sudo mkdir -p /opt/nginx'
         ssh ${EC2_USER}@${HOST} sudo cp /home/ubuntu/nginx/nginx.conf /opt/nginx/       
         ssh ${EC2_USER}@${HOST} 'sudo mv /home/ubuntu/docker-compose.tmpl /opt/docker-compose.tmpl'
         ssh ${EC2_USER}@${HOST} 'sudo mv /home/ubuntu/promtail-config.yaml /opt/promtail-config.yaml'    
         """
        }
      }
    }    

    stage('Install Docker and Compose') {
      steps {
        script {
          sshCommand remote: remote, command: '''
            set -e

            if ! command -v docker &> /dev/null
            then
              echo "[INFO] Installing Docker..."

              sudo apt-get update
              sudo apt-get install -y ca-certificates curl gnupg lsb-release

              sudo mkdir -p /etc/apt/keyrings
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

              echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
              https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
              sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

              sudo apt-get update
              sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

              sudo usermod -aG docker $USER
            else
              echo "[INFO] Docker already installed"
            fi

            docker --version
            docker compose version
          '''
        }
      }
    }

    stage ('Deploy node-app') {
      steps {
        script {
          sshCommand remote: remote, command: """
          export APP_IMG="${env.REGISTRY}:${env.BUILD_ID}"
          cd /opt
          envsubst < docker-compose.tmpl | sudo tee docker-compose.yaml         
          docker compose up -d
          """
        }
      }
    }
  }
}
