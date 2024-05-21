import json
import os
from datetime import datetime
import sys
import requests

# Turn on for debugging
DEBUG = 0

# Gets the username of the person who owns the github app access token
def get_username(access_token):
    headers = {
        'Authorization': f'token {access_token}'
    }
    response = requests.get('https://api.github.com/user', headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('login')  # 'login' contains the username
    else:
        print(f"Failed to fetch user data: {response.status_code} - {response.text}")
        sys.exit()
        return None

# Creating empty jenkins Multibranch pipeline
def create_multibranch_pipeline(
        jenkins_url,
        request_session,
        jenkins_crumb,
        github_username
):
    unique_id_tag = datetime.now().time().strftime("%H%M%S%f")
    pipeline_name = f"github_app_{github_username}_{unique_id_tag}"
    jenkins_url = f"{jenkins_url}/view/all/createItem"
    payload = {
        'name': pipeline_name,
        'mode': 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject',
        'from': '',
        'Jenkins-Crumb': jenkins_crumb,
        'json': '{"name":"'+pipeline_name+'","mode":"org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject","from":"","Jenkins-Crumb":"'+jenkins_crumb+'"}'
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Jenkins-Crumb": jenkins_crumb,
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    r = request_session.post(jenkins_url, data = payload, headers = headers)
    if DEBUG == 1:
        print("\n\n <<< CREATING MULTIBRANCH PIPELINE >>> \n\n")
        print("\n\nResponse Text:\n", r.text)
        print("Response code: ", r.status_code)
    return pipeline_name

# Configuring an already created empty multibranch pipeline
def configure_multibranch_pipeline(
    jenkins_url,
    github_repo_url,
    github_username,
    pipeline_name,
    github_credentials_id,
    jenkins_crumb,
    request_session
):
    jenkins_url = f"{jenkins_url}/job/{pipeline_name}/configSubmit"
    creation_time = datetime.now()
    pipeline_description = f"Job Automatically created for {github_username} at {creation_time} PKT"
    payload = {
        'enable': 'true',
        '_.displayNameOrNull': '',
        '_.description': pipeline_description,
        'stapler-class': 'org.jenkinsci.plugins.github_branch_source.GitHubSCMSource',
        'id': '',
        'includeUser': 'false',
        '_.credentialsId': github_credentials_id,
        'configuredByUrl': 'true',
        'removeme0_configuredByUrlRadio': 'true',
        '_.repositoryUrl': github_repo_url,
        '_.repoOwner': github_username,
        '_.strategyId': '2',
        'stapler-class_1': 'org.jenkinsci.plugins.github_branch_source.BranchDiscoveryTrait',
        '$class_1': 'org.jenkinsci.plugins.github_branch_source.BranchDiscoveryTrait',
        '_.strategyId_1': '2',
        'stapler-class_2': 'org.jenkinsci.plugins.github_branch_source.OriginPullRequestDiscoveryTrait',
        '$class_2': 'org.jenkinsci.plugins.github_branch_source.OriginPullRequestDiscoveryTrait',
        '_.strategyId_2': '2',
        'stapler-class_3': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustContributors',
        '$class_3': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustContributors',
        'stapler-class_4': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustEveryone',
        '$class_4': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustEveryone',
        'stapler-class_5': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustPermission',
        '$class_5': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustPermission',
        'stapler-class_6': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustNobody',
        '$class_6': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustNobody',
        'stapler-class_7': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait',
        '$class_7': 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait',
        'stapler-class_8': 'jenkins.branch.DefaultBranchPropertyStrategy',
        '$class_8': 'jenkins.branch.DefaultBranchPropertyStrategy',
        'stapler-class_9': 'jenkins.branch.NamedExceptionsBranchPropertyStrategy',
        '$class_9': 'jenkins.branch.NamedExceptionsBranchPropertyStrategy',
        'stapler-class_10': 'jenkins.branch.BranchSource',
        'kind': 'jenkins.branch.BranchSource',
        '_.scriptPath': 'cloud-v-pipeline',
        'stapler-class_11': 'org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory',
        '$class_11': 'org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory',
        '_.refTrigger': 'on',
        '_.interval': '1d',
        '_.token': '',
        'stapler-class_12': 'com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy',
        '$class_12': 'com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy',
        '_.pruneDeadBranches': 'on',
        '_.daysToKeepStr': '',
        '_.numToKeepStr': '',
        'stapler-class_13': 'com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon',
        '$class_13': 'com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon',
        'stapler-class_14': 'jenkins.branch.MetadataActionFolderIcon',
        '$class_14': 'jenkins.branch.MetadataActionFolderIcon',
        'stapler-class_15': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritParentStrategy',
        '$class_15': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritParentStrategy',
        'stapler-class_16': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritGlobalStrategy',
        '$class_16': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritGlobalStrategy',
        'stapler-class_17': 'org.jenkinsci.plugins.matrixauth.inheritance.NonInheritingStrategy',
        '$class_17': 'org.jenkinsci.plugins.matrixauth.inheritance.NonInheritingStrategy',
        'core:apply': 'true',
        'Jenkins-Crumb': jenkins_crumb,
        'json': '{"enable":"true","displayNameOrNull":"","description":"'+pipeline_description+'","":["","0","1"],"sources":{"source":{"stapler-class":"org.jenkinsci.plugins.github_branch_source.GitHubSCMSource","id":"","includeUser":"false","credentialsId":"'+github_credentials_id+'","configuredByUrl":"true","configuredByUrlRadio":"true","repositoryUrl":"'+github_repo_url+'","repoOwner":"'+github_username+'","repository":"","traits":[{"strategyId":"2","stapler-class":"org.jenkinsci.plugins.github_branch_source.BranchDiscoveryTrait","$class":"org.jenkinsci.plugins.github_branch_source.BranchDiscoveryTrait"},{"strategyId":"2","stapler-class":"org.jenkinsci.plugins.github_branch_source.OriginPullRequestDiscoveryTrait","$class":"org.jenkinsci.plugins.github_branch_source.OriginPullRequestDiscoveryTrait"},{"strategyId":"2","":"1","trust":{"stapler-class":"org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustEveryone","$class":"org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustEveryone"},"stapler-class":"org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait","$class":"org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait"}]},"":"0","strategy":{"stapler-class":"jenkins.branch.DefaultBranchPropertyStrategy","$class":"jenkins.branch.DefaultBranchPropertyStrategy"},"stapler-class":"jenkins.branch.BranchSource","kind":"jenkins.branch.BranchSource"},"projectFactory":{"scriptPath":"cloud-v-pipeline","stapler-class":"org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory","$class":"org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory"},"orphanedItemStrategy":{"stapler-class":"com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy","$class":"com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy","abortBuilds":"false","pruneDeadBranches":"true","daysToKeepStr":"","numToKeepStr":""},"icon":{"stapler-class":"jenkins.branch.MetadataActionFolderIcon","$class":"jenkins.branch.MetadataActionFolderIcon"},"com-cloudbees-hudson-plugins-folder-properties-AuthorizationMatrixProperty":{},"Submit":"","core:apply":"true","Jenkins-Crumb":"'+jenkins_crumb+'"}'
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Jenkins-Crumb": jenkins_crumb,
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    r = request_session.post(url=jenkins_url, data=payload, headers=headers)

    if DEBUG == 1:
        print("\n\n <<< CONFIGURING MULTIBRANCH PIPELINE >>> \n\n")
        print("\n\n Response Text: \n", r.text)
        print("Response code: ", r.status_code)


def adding_github_app_credentials(
    jenkins_crumb,
    request_session,
    github_username,
    github_secret,
):

    description = f"GitHub app token added by {github_username}"
    unique_id = datetime.now().time().strftime("%H%M%S%f") # Setting unique ID with time in milliseconds for a unique combination

    jenkins_url = json_data["jenkins_url"]+"/manage/credentials/store/system/domain/_/createCredentials"



    # Payload for adding username and password
    payload = {
        '_.scope': 'GLOBAL',
        '_.username': github_username,
        '_.usernameSecret': 'on',
        '_.password': github_secret,
        '_.id': '15072024',
        '_.description': description,
        'stapler-class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        '$class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        'stapler-class': 'com.atlassian.bitbucket.jenkins.internal.config.BitbucketTokenCredentialsImpl',
        '$class': 'com.atlassian.bitbucket.jenkins.internal.config.BitbucketTokenCredentialsImpl',
        'stapler-class': 'org.jenkinsci.plugins.github_branch_source.GitHubAppCredentials',
        '$class': 'org.jenkinsci.plugins.github_branch_source.GitHubAppCredentials',
        'stapler-class': 'com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl',
        '$class': 'com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl',
        'stapler-class': 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey',
        '$class': 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey',
        'stapler-class': 'org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl',
        '$class': 'org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl',
        'stapler-class': 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl',
        '$class': 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl',
        'stapler-class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl',
        '$class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl',
        'Submit':'',
        'Jenkins-Crumb': jenkins_crumb,
        'json': '{"":"0","credentials":{"scope":"GLOBAL","username":"'+github_username+'","usernameSecret":"true","password":"'+github_secret+'","$redact":"password","id":"'+unique_id+'","description":"'+description+'","stapler-class":"com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl","$class":"com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"},"Submit":"","Jenkins-Crumb":"'+jenkins_crumb+'"}'
    }



    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Jenkins-Crumb": crumb_value,
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }



    r = request_session.post(url=jenkins_url, data=payload, headers=headers)
    if DEBUG == 1:
        print(r.status_code)
        print(r.text)
    return unique_id


# Setting up variables
working_directory = os.path.dirname(os.path.realpath(__file__))
secret_text = sys.argv[1] # Getting secret text from parent process
github_username = get_username(secret_text) # Getting github username from github app access token
github_repo_url = sys.argv[2]

# Reading json file

json_file = open(f"{working_directory}/userinfo.json")
json_data = json.load(json_file)

# Creating a single session for all the python requests
session = requests.Session()
session.auth = (json_data["jenkins_username"], json_data["jenkins_password"])

# Getting crumb from jenkins
crumb_json = (session.get(json_data["jenkins_url"]+"/crumbIssuer/api/json")).json()
crumb_value=crumb_json.get('crumb')

# Adding credentials in jenkins credentials database
credentials_id = adding_github_app_credentials(
    crumb_value, 
    session, 
    github_username, 
    secret_text
)

# Creating empty multibranch pipeline
pipeline_name = create_multibranch_pipeline(
    json_data["jenkins_url"],
    session, 
    crumb_value, 
    github_username
)

# Configure multibranch pipeline
configure_multibranch_pipeline(
    json_data["jenkins_url"],
    github_repo_url,
    github_username,
    pipeline_name,
    credentials_id,
    crumb_value,
    session
)
print(abcd)
print(json_data["jenkins_url"]+f"/job/{pipeline_name}")


