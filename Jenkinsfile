/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '54.0',
  platform: 'Windows 10'
]

pipeline {
  agent any
  libraries {
    lib('fxtest@1.6')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  environment {
    VARIABLES = credentials('MOZILLIANS_VARIABLES')
    PYTEST_ADDOPTS =
      "--tb=short " +
      "--color=yes " +
      "--driver=SauceLabs " +
      "--variables=capabilities.json " +
      "--variables=${VARIABLES}"
    PULSE = credentials('PULSE')
    SAUCELABS_API_KEY = credentials('SAUCELABS_API_KEY')
  }
  stages {
    stage('Lint') {
      steps {
        sh "tox -e flake8"
      }
    }
    stage('Test') {
      steps {
        writeCapabilities(capabilities, 'capabilities.json')
        sh "tox -e py27"
      }
      post {
        always {
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          submitToActiveData('results/py27_raw.txt')
          submitToTreeherder('mozillians-tests', 'e2e', 'End-to-end integration tests', 'results/*', 'results/py27_tbpl.txt')
          publishHTML(target: [
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'results',
            reportFiles: "py27.html",
            reportName: 'HTML Report'])
        }
      }
    }
  }
  post {
    failure {
      mail(
        body: "${BUILD_URL}",
        from: "firefox-test-engineering@mozilla.com",
        replyTo: "firefox-test-engineering@mozilla.com",
        subject: "Build failed in Jenkins: ${JOB_NAME} #${BUILD_NUMBER}",
        to: "fte-ci@mozilla.com")
    }
    changed {
      ircNotification()
    }
  }
}
