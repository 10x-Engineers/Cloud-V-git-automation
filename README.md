# Cloud-V Version Control Automation

This is a light-weight odoo application/module containing source code for automatically creating multibranch pipeline for following version control systems.  
- GitHub (Using GitHub App)
- GitLab 

![Project components](<assets/Cloud-V Version control automation.drawio.png>)

## What does this application do

This application does the following steps:

### GitHub

- Upon authorizing the GitHub app and selecting the reposiotories to integrate with Cloud-V, users are redirected to  Cloud-V website
- The website asks for a repository url to integrate with Jenkins multibranch pipeline (this repository should be one of the repositories which user selected to authorize in previous step)
- Once the user enters repository url and clicks on submit, this redirects to final page where users will get a link to their multibranch pipeline which is already configured with all the webhooks and github access token of the app

### GitLab

- Users will have to enter the personal access token and GitLab repository clone URL (ending with .git).
- Once provided the above information, a mutlibranch CI pipeline is created and users are redirected to the page where they can get the link to their pipeline

## Requirements for running this application

Anyone who needs to use this application needs to add their respective info to `/controllers/userinfo.json`. `github_app_client_id` and `github_app_client_secret` can be obtained from the github application settings whereas jenkins-related fields are known by jenkins administrator.

Once added, users need to paste this application as is in their `addons` folder of Odoo.

For installing this application in Odoo, users have to enable developer mode with assets and then install this application from the store by searching it.

Users must have the pages in their app as mentioned in the python files for this module to work.
