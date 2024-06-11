import json
import os
from datetime import datetime
import sys
import requests

# Turn on for debugging
DEBUG = 0

# Gets the username of the person who owns the gitlab app access token
def get_username(access_token):
    headers = {
        "PRIVATE-TOKEN": access_token
    }
    response = requests.get('https://gitlab.com/api/v4/user', headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info['username']  # 'login' contains the username
    else:
        print(f"Failed to fetch user data: {response.status_code} - {response.text}")
        sys.exit()

# Creating empty jenkins Multibranch pipeline
def create_multibranch_pipeline(
        jenkins_url,
        request_session,
        jenkins_crumb,
        gitlab_username
):
    unique_id_tag = datetime.now().strftime('%d%m%Y%H%M%S%f')[:-3]
    pipeline_name = f"gitlab_{gitlab_username}_{unique_id_tag}"
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
# Works only with https://gitlab.com
# Works only with public repositories
def configure_multibranch_pipeline(
    gitlab_server_name,
    jenkins_url,
    gitlab_repo_url,
    gitlab_username,
    pipeline_name,
    jenkins_crumb,
    request_session
):
    jenkins_url = f"{jenkins_url}/job/{pipeline_name}/configSubmit"
    creation_time = datetime.now()
    pipeline_description = f"Job Automatically created for {gitlab_username} at {creation_time} PKT"
    splitted_string = gitlab_repo_url.split('/')
    project_owner = splitted_string[3]
    project_repo = splitted_string[4][0:-4]
    project_path = f"{project_owner}/{project_repo}"
    payload = {
        'enable': 'true',
        '_.displayNameOrNull': '',
        '_.description': pipeline_description,
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.GitLabSCMSource',
        'id': '',
        '_.serverName': gitlab_server_name,
        'includeUser': 'false',
        '_.credentialsId': '',
        '_.projectOwner': project_owner,
        '_.projectPath': project_path,
        '_.strategyId': '2',
        '_.branchesAlwaysIncludedRegex':'',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.BranchDiscoveryTrait',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.BranchDiscoveryTrait',
        '_.strategyId': '1',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.OriginMergeRequestDiscoveryTrait',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.OriginMergeRequestDiscoveryTrait',
        '_.strategyId': '1',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustEveryone',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustEveryone',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustMembers',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustMembers',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustNobody',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustNobody',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustPermission',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustPermission',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait',
        '_.alwaysBuildMROpen': 'on',
        '_.alwaysBuildMRReOpen': 'on',
        'stapler-class': 'io.jenkins.plugins.gitlabbranchsource.WebhookListenerBuildConditionsTrait',
        '$class': 'io.jenkins.plugins.gitlabbranchsource.WebhookListenerBuildConditionsTrait',
        '_.projectId': '',
        'stapler-class': 'jenkins.branch.DefaultBranchPropertyStrategy',
        '$class': 'jenkins.branch.DefaultBranchPropertyStrategy',
        'stapler-class': 'jenkins.branch.NamedExceptionsBranchPropertyStrategy',
        '$class': 'jenkins.branch.NamedExceptionsBranchPropertyStrategy',
        'stapler-class': 'jenkins.branch.BranchSource',
        'kind': 'jenkins.branch.BranchSource',
        '_.scriptPath': 'cloud-v-pipeline',
        'stapler-class': 'org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory',
        '$class': 'org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory',
        '_.refTrigger': 'on',
        '_.interval': '1d',
        '_.token': '',
        'stapler-class': 'com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy',
        '$class': 'com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy',
        '_.pruneDeadBranches': 'on',
        '_.daysToKeepStr': '',
        '_.numToKeepStr': '',
        'stapler-class': 'com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon',
        '$class': 'com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon',
        'stapler-class': 'jenkins.branch.MetadataActionFolderIcon',
        '$class': 'jenkins.branch.MetadataActionFolderIcon',
        'stapler-class': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritParentStrategy',
        '$class': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritParentStrategy',
        'stapler-class': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritGlobalStrategy',
        '$class': 'org.jenkinsci.plugins.matrixauth.inheritance.InheritGlobalStrategy',
        'stapler-class': 'org.jenkinsci.plugins.matrixauth.inheritance.NonInheritingStrategy',
        '$class': 'org.jenkinsci.plugins.matrixauth.inheritance.NonInheritingStrategy',
        'core:apply': 'true',
        'Jenkins-Crumb': jenkins_crumb,
        'json': '{"enable":true,"displayNameOrNull":"","description":"'+pipeline_description+'","":["","0","1"],"sources":{"source":{"stapler-class":"io.jenkins.plugins.gitlabbranchsource.GitLabSCMSource","id":"","serverName":"'+gitlab_server_name+'","includeUser":"false","credentialsId":"","projectOwner":"'+project_owner+'","projectPath":"'+project_path+'","traits":[{"strategyId":"2","branchesAlwaysIncludedRegex":"","stapler-class":"io.jenkins.plugins.gitlabbranchsource.BranchDiscoveryTrait","$class":"io.jenkins.plugins.gitlabbranchsource.BranchDiscoveryTrait"},{"strategyId":"1","stapler-class":"io.jenkins.plugins.gitlabbranchsource.OriginMergeRequestDiscoveryTrait","$class":"io.jenkins.plugins.gitlabbranchsource.OriginMergeRequestDiscoveryTrait"},{"strategyId":"1","":"0","trust":{"stapler-class":"io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustEveryone","$class":"io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustEveryone"},"buildMRForksNotMirror":false,"stapler-class":"io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait","$class":"io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait"},{"alwaysBuildMROpen":true,"alwaysBuildMRReOpen":true,"alwaysIgnoreMRApproval":false,"alwaysIgnoreMRUnApproval":false,"alwaysIgnoreMRApproved":false,"alwaysIgnoreMRUnApproved":false,"alwaysIgnoreNonCodeRelatedUpdates":false,"alwaysIgnoreMRWorkInProgress":false,"stapler-class":"io.jenkins.plugins.gitlabbranchsource.WebhookListenerBuildConditionsTrait","$class":"io.jenkins.plugins.gitlabbranchsource.WebhookListenerBuildConditionsTrait"}],"projectId":""},"":"0","strategy":{"stapler-class":"jenkins.branch.DefaultBranchPropertyStrategy","$class":"jenkins.branch.DefaultBranchPropertyStrategy"},"stapler-class":"jenkins.branch.BranchSource","kind":"jenkins.branch.BranchSource"},"projectFactory":{"scriptPath":"cloud-v-pipeline","stapler-class":"org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory","$class":"org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory"},"orphanedItemStrategy":{"stapler-class":"com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy","$class":"com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy","abortBuilds":false,"pruneDeadBranches":true,"daysToKeepStr":"","numToKeepStr":""},"icon":{"stapler-class":"jenkins.branch.MetadataActionFolderIcon","$class":"jenkins.branch.MetadataActionFolderIcon"},"com-cloudbees-hudson-plugins-folder-properties-AuthorizationMatrixProperty":{},"Submit":"","core:apply":"true","Jenkins-Crumb":"'+jenkins_crumb+'"}'
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


def adding_gitlabPAT_credentials(
    jenkins_crumb,
    request_session,
    gitlab_username,
    gitlab_pat,
):

    description = f"GitLab personal access token added by {gitlab_username}"
    unique_id = datetime.now().strftime('%d%m%Y%H%M%S%f')[:-3] # Setting unique ID with time in milliseconds for a unique combination

    jenkins_url = json_data["jenkins_url"]+"/manage/credentials/store/system/domain/_/createCredentials"



    # Payload for adding username and password
    payload = {
        '_.scope': 'GLOBAL',
        '_.username': '',
        '_.password': '',
        '_.id': '',
        '_.description':'',
        'stapler-class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        '$class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        'stapler-class': 'com.atlassian.bitbucket.jenkins.internal.config.BitbucketTokenCredentialsImpl',
        '$class': 'com.atlassian.bitbucket.jenkins.internal.config.BitbucketTokenCredentialsImpl',
        'stapler-class': 'org.jenkinsci.plugins.gitlab_branch_source.GitHubAppCredentials',
        '$class': 'org.jenkinsci.plugins.gitlab_branch_source.GitHubAppCredentials',
        'stapler-class': 'com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl',
        '$class': 'com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl',
        '_.scope': 'GLOBAL',
        '_.token': gitlab_pat,
        '_.id': unique_id,
        '_.description': description,
        'stapler-class': 'io.jenkins.plugins.gitlabserverconfig.credentials.PersonalAccessTokenImpl',
        '$class': 'io.jenkins.plugins.gitlabserverconfig.credentials.PersonalAccessTokenImpl',
        'stapler-class': 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey',
        '$class': 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey',
        'stapler-class': 'org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl',
        '$class': 'org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl',
        'stapler-class': 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl',
        '$class': 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl',
        'stapler-class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl',
        '$class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl',
        'Submit': '',
        'Jenkins-Crumb': jenkins_crumb,
        'json': '{"":"4","credentials":{"scope":"GLOBAL","token":"'+gitlab_pat+'","$redact":"token","id":"'+unique_id+'","description":"'+description+'","stapler-class":"io.jenkins.plugins.gitlabserverconfig.credentials.  PersonalAccessTokenImpl","$class":"io.jenkins.plugins.gitlabserverconfig.credentials.PersonalAccessTokenImpl"},"Submit":"","Jenkins-Crumb":"'+jenkins_crumb+'"}'
    }



    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Jenkins-Crumb": jenkins_crumb,
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }



    r = request_session.post(url=jenkins_url, data=payload, headers=headers)
    if DEBUG == 1:
        print(r.status_code)
        print(r.text)
    return unique_id

def create_gitlab_server(
    gitlab_credentials_id,
    gitlab_username,
    jenkins_url,
    session,
    jenkins_crumb
):
    unique_id = datetime.now().strftime('%d%m%Y%H%M%S%f')[:-3] # Setting unique ID with time in milliseconds for a unique
    gitlab_server_name = f"{gitlab_username}_{unique_id}"
    gitlab_server_url = "https://gitlab.com"

    # Jenkins script endpoint
    script_endpoint = f'{jenkins_url}/manage/script'

    # Request headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Jenkins-Crumb": jenkins_crumb
    }
    # Groovy script to be executed
    groovy_script = f"""
import io.jenkins.plugins.gitlabserverconfig.servers.GitLabServers
import io.jenkins.plugins.gitlabserverconfig.servers.GitLabServer
import jenkins.model.Jenkins

def gitlabServerName = '{gitlab_server_name}'
def gitlabServerUrl = '{gitlab_server_url}'
def credentialsId = '{gitlab_credentials_id}'

def gitLabServers = GitLabServers.get()
def existingServer = gitLabServers.findServer(gitlabServerName)

if (existingServer) {{
    println "GitLab server {gitlab_server_name} already exists."
}} else {{
    def newServer = new GitLabServer(gitlabServerUrl, gitlabServerName, credentialsId)
    newServer.setManageWebHooks(true)
    newServer.setManageSystemHooks(true)
    newServer.setImmediateHookTrigger(true)

    gitLabServers.addServer(newServer)
    Jenkins.instance.save()
    println "GitLab server {gitlab_server_name} added successfully."
}}
"""
    # Data payload
    data = {
        'script': groovy_script,
        'Submit': '',
        'Jenkins-Crumb': jenkins_crumb
    }

    # Make the POST request
    response = session.post(script_endpoint, headers=headers, data=data)

    # Check the response
    if response.status_code == 200:
        if DEBUG == 1:
            print("Script executed successfully")
            print(response.status_code)
        return gitlab_server_name
    else:
        print(f"Failed to execute script. Status code: {response.status_code}")
        print(response.text)
        print(response.status_code)
        sys.exit()

if __name__ == "__main__":
    # Setting up variables
    working_directory = os.path.dirname(os.path.realpath(__file__))
    gitlab_pat = sys.argv[1] # Getting secret text from parent process
    gitlab_username = get_username(gitlab_pat) # Getting gitlab username from gitlab app access token
    gitlab_repo_name = sys.argv[2] 

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
    credentials_id = adding_gitlabPAT_credentials(
        crumb_value, 
        session, 
        gitlab_username, 
        gitlab_pat
    )

    # Creating empty multibranch pipeline
    pipeline_name = create_multibranch_pipeline(
        json_data["jenkins_url"],
        session, 
        crumb_value, 
        gitlab_username
    )

    # Creating Gitlab Server in global configuration
    gitlab_server_name = create_gitlab_server(
        credentials_id,
        gitlab_username,
        json_data["jenkins_url"],
        session,
        crumb_value
    )

    # Configure multibranch pipeline
    configure_multibranch_pipeline(
        gitlab_server_name,
        json_data["jenkins_url"],
        gitlab_repo_name,
        gitlab_username,
        pipeline_name,
        crumb_value,
        session
    )
    print(json_data["jenkins_url"]+f"/job/{pipeline_name}")
