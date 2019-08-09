node ('docker-build') {
  def project = 'metagenid'
  def appName = 'compute'
  def instanceType = 'compute'
  def imageTag = "${env.BRANCH_NAME}"
  def appContainerRepo = "432304291388.dkr.ecr.us-east-1.amazonaws.com/${appName}"

  cleanWs()
  checkout scm

  def last_commit = getLastCommit()
  notifyStarted(last_commit)

  sh("dockerlogin")

  if (env.BRANCH_NAME == 'dev' ) {
    imageTag = 'latest'
  }

  echo "Image tag resolved by branch name: ${imageTag}"

  if (env.TAG_NAME) {
    if (env.TAG_NAME ==~ /^release.*/) {
      imageTag = 'master'
    } else
    if (env.TAG_NAME ==~ /^qa.*/) {
        imageTag = 'qa'
    } else
    if (env.TAG_NAME ==~ /^uat.*/) {
        imageTag = 'uat'
    } else
    if (env.TAG_NAME ==~ /^staging.*/) {
        imageTag = 'staging'
    } else {
        imageTag = 'latest'
    }
  }
  echo "Image tag resolved by GIT tag (overwrites branch tag): ${imageTag}"

  stage ("Build image") {
    sh("docker build -t ${appName}:${imageTag} .")
    sh("docker tag ${appName}:${imageTag} ${appContainerRepo}:`git rev-parse --short HEAD`")
    DIGEST = sh(script: "docker images | grep `git rev-parse --short HEAD`", returnStdout: true).split()
    echo "Image digest: ${DIGEST[2]}"
    sh("docker tag ${appName}:${imageTag} ${appContainerRepo}:${imageTag}")
    sh("docker tag ${appName}:${imageTag} ${appContainerRepo}:${env.BRANCH_NAME}")
    sh("docker tag ${appName}:${imageTag} ${appContainerRepo}:${DIGEST[2]}")
  }

  stage ("Running tests") {
    echo "Running linter..."
    try {
      sh("make lint")
    }
    finally {
      archiveArtifacts artifacts: 'lint.log', fingerprint: false
      sh("make clean")
    }

    echo "Running unit tests..."
    try {
      sh("make all")
    }
    catch(all) {
    notifyUnitTestsfailed(last_commit)
    currentBuild.result = 'UNSTABLE'
    }
    finally {
      archiveArtifacts artifacts: 'docker/reports/report.html', fingerprint: false
      junit 'docker/reports/report.xml'
      sh("make clean")
    }
  }

  stage ("Push image to registry") {
    echo "Image tag prior deploy ${imageTag}"
    if (imageTag == 'master' || imageTag == 'qa' || imageTag == 'uat' || imageTag == 'staging' || imageTag == 'latest') {
      sh("docker push ${appContainerRepo}:`git rev-parse --short HEAD`")
      sh("docker push ${appContainerRepo}:${imageTag}")
      sh("docker push ${appContainerRepo}:${env.BRANCH_NAME}")
      sh("docker push ${appContainerRepo}:${DIGEST[2]}")
    } else {
        echo 'Branch name was not set within appropriate scope! Will not push anything to Registry'
    }
  }

  stage ("Deploy Application") {
    switch (imageTag) {
      // Roll out to qa
      case ~/^qa.*/:
          def environment = "qa"
          echo "Deploying image: ${appContainerRepo}:${imageTag}"
          sh("ansible 'tag_Environment_dev:&tag_Name_*compute*' -m service -a 'name=compute-qa state=restarted' -b")
          sh("ansible 'tag_Environment_dev:&tag_Name_*compute*' -m service -a 'name=compute16s-qa state=restarted' -b")
          sh("ansible 'tag_Environment_dev:&tag_Name_*compute*' -m service -a 'name=compute-kepler-qa state=restarted' -b")
          sh("ansible 'tag_Environment_qa:&tag_Name_*base*' -m service -a 'name=analysis_service state=restarted' -b")
          sh("ansible 'tag_Environment_qa:&tag_Name_*base*' -m service -a 'name=comparative_worker state=restarted' -b")
          notifyBuildDeployed(last_commit)
          break

      // Roll out to uat
      case ~/^uat.*/:
          def environment = "uat"
          echo "Deploying image: ${appContainerRepo}:${imageTag}"
          sh("ansible 'tag_Environment_dev:&tag_Name_*compute*' -m service -a 'name=compute-uat state=restarted' -b")
          sh("ansible 'tag_Environment_dev:&tag_Name_*compute*' -m service -a 'name=compute16s-uat state=restarted' -b")
          sh("ansible 'tag_Environment_dev:&tag_Name_*compute*' -m service -a 'name=compute-kepler-uat state=restarted' -b")
          sh("ansible 'tag_Environment_uat:&tag_Name_*base*' -m service -a 'name=analysis_service state=restarted' -b")
          sh("ansible 'tag_Environment_uat:&tag_Name_*base*' -m service -a 'name=comparative_worker state=restarted' -b")
          notifyBuildDeployed(last_commit)
          break

      // Roll out a staging environment
      case ~/^staging.*/:
          def environment = "staging"
          echo "Deploying image: ${appContainerRepo}:${imageTag}"
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*compute*' -m service -a 'name=compute state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*compute*' -m service -a 'name=compute16s state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*compute*' -m service -a 'name=compute-kepler state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*base*' -m service -a 'name=analysis_service state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*base*' -m service -a 'name=comparative_worker state=restarted' -b")
          notifyBuildDeployed(last_commit)
    break

      // Roll out a dev environment
      case ~/^latest.*/:
          def environment = "dev"
          echo "Deploying image: ${appContainerRepo}:${imageTag}"
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*compute*' -m service -a 'name=compute state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*compute*' -m service -a 'name=compute16s state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*compute*' -m service -a 'name=compute-kepler state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*base*' -m service -a 'name=analysis_service state=restarted' -b")
          sh("ansible 'tag_Environment_${environment}:&tag_Name_*base*' -m service -a 'name=comparative_worker state=restarted' -b")
          notifyBuildDeployed(last_commit)
    break

      default:
          echo 'Branch name was not set within appropriate scope! Will not deploy anything'
          notifyWontBeDeployed()
          break
    }
  }

/* Issue with reports directory ownership as ROOT. Unable to clean workspace because of that.
   This is a very ugly hack!!! I will remove it as sson as I find a proper solution to workspace cleaning problem!
*/
  sh("sudo /bin/chmod 777 `pwd`/docker/reports -R")

}

def notifyStarted(String author) {
  // send to Slack
  slackSend (message: "Build started: '${env.JOB_NAME}' ${env.BUILD_URL} \nGit info: ${author}")
}

def notifyUnitTestsfailed(String author) {
  // send to Slack
  slackSend (color: 'danger', message: "Unit Tests step failed: '${env.JOB_NAME}' ${env.BUILD_URL} \nGit info: ${author}")
}

def notifyBuildDeployed(String author) {
  // send to Slack
  slackSend (color: 'good', message: "Build deployed: '${env.JOB_NAME}' ${env.BUILD_URL} \nGit info: ${author}")
}

def notifyWontBeDeployed() {
  // send to Slack
  slackSend (color: 'good', message: "Build completed. Won't be deployed: '${env.JOB_NAME}' ${env.BUILD_URL}")
}

def String getLastCommit(){
  return sh(
    script: "git log -1 --pretty='Last commit. Author - %an; Message: - %B'",
    returnStdout: true
  ).trim()
}