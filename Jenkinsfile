#!/usr/bin/env groovy

def branch = env.BRANCH_NAME ?: 'master'

/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '65.0',
  platform: 'Windows 10'
]

pipeline {
  agent any
  libraries {
    lib('fxtest@1.10')
  }
  triggers {
    pollSCM(branch == 'master' ? 'H/5 * * * *' : '')
    cron(branch == 'master' ? 'H H * * *' : '')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  stages {
    stage('Lint') {
      agent {
        dockerfile true
      }
      steps {
        sh "flake8"
      }
    }
    stage('Test') {
      agent {
        dockerfile true
      }
      environment {
        VARIABLES = credentials('MOZILLIANS_VARIABLES')
        PYTEST_PROCESSES = "${PYTEST_PROCESSES ?: "auto"}"
        PULSE = credentials('PULSE')
        SAUCELABS = credentials('SAUCELABS')
      }
      steps {
        writeCapabilities(capabilities, 'capabilities.json')
        sh "pytest " +
          "-n=${PYTEST_PROCESSES} " +
          "--tb=short " +
          "--color=yes " +
          "--driver=SauceLabs " +
          "--variables=capabilities.json " +
          "--variables=${VARIABLES} " +
          "--junit-xml=results/junit.xml " +
          "--html=results/index.html " +
          "--self-contained-html " +
          "--log-raw=results/raw.txt " +
          "--log-tbpl=results/tbpl.txt"
      }
      post {
        always {
          stash includes: 'results/*', name: 'results'
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          submitToActiveData('results/raw.txt')
          submitToTreeherder('mozillians-tests', 'e2e', 'End-to-end integration tests', 'results/*', 'results/tbpl.txt')
        }
      }
    }
  }
  post {
    always {
      unstash 'results'
      publishHTML(target: [
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'results',
        reportFiles: 'index.html',
        reportName: 'HTML Report'])
    }
    changed {
      ircNotification()
    }
    failure {
      emailext(
        attachLog: true,
        attachmentsPattern: 'results/index.html',
        body: '$BUILD_URL\n\n$FAILED_TESTS',
        replyTo: '$DEFAULT_REPLYTO',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS')
    }
  }
}
