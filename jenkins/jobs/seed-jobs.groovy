// Job DSL: Seed Jobs for Automated CI/CD Pipelines
pipelineJob('qe-platform-pipeline-local') {
    description('Continuous Integration and HA Verification on Local / Kind / LocalStack')
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/adarsha89/highly-available-qe-setup.git')
                    }
                    branches('*/main')
                }
            }
            scriptPath('jenkins/pipelines/Jenkinsfile.ha-qe-pipeline')
        }
    }
}

pipelineJob('qe-failover-resilience-drill') {
    description('Automated Chaos & Failover Verification against Kubernetes HA & Jenkins controller')
    triggers {
        cron('H H(1-5) * * *') // Run daily resilience verification
    }
    definition {
        cps {
            script('''
                pipeline {
                    agent { label 'qe-agent' }
                    stages {
                        stage('Pre-flight Health Check') {
                            steps {
                                sh 'kubectl get nodes'
                                sh 'curl -f http://qe-monitoring-prometheus:9090/-/healthy'
                            }
                        }
                        stage('Run Resilience Test Suite') {
                            steps {
                                sh 'pytest tests/failover/ tests/kubernetes-ha/ -v'
                            }
                        }
                    }
                }
            ''')
            sandbox()
        }
    }
}
