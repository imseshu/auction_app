pipeline {
    agent any
    environment {
        EC2_DNS = "${SERVER_IP}"
        SSH_KEY = credentials('ec2-user')
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/imseshu/auction_app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sshagent(['ec2-user']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ec2-user@$EC2_DNS << EOF
                    sudo yum update
                    sudo yum install git python3-pip python3 nginx tmux -y
                    pip3 install flask pandas xlsxwriter openpyxl gunicorn
                    mkdir -p auction_app
                    exit
                    EOF
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    sshagent(['ec2-user']) {
                        sh '''
                        scp -o StrictHostKeyChecking=no -r * ec2-user@$EC2_DNS:~/auction_app/
                        ssh -o StrictHostKeyChecking=no ec2-user@$EC2_DNS << EOF
                        cd ~/auction_app
                        nohup python3 app.py > app.log 2>&1 &
                        exit
                        EOF
                        '''
                    }
                }
            }
        }
    }
}
