# cloud-v-github-integration

This is a very light-weight odoo application/module containing source code for getting the access token from github and using it to automatically create a multibranch pipeline on a jenkins instance.

This module assumes following keypoints:

- You have a jenkins instance already running
- Your website is hosted on odoo framework
- You have a public github application

## What does this application do

This application does the following steps:

- Once you have a public github application and someone installs/authorizes it for their repository, it will redirect them to the website
- The website asks for a repository url to integrate with jenkins multibranch pipeline (this repository should be one of the repositories which user selected to authorize in previous step)
- Once the user enters repository url and clicks on submit, this redirects to final page where users will get a link to their multibranch pipeline which is already configured with all the webhooks and github access token of the app

## Requirements for running this application

Anyone who needs to use this application needs to add their respective info to `/controllers/userinfo.json`. `github_app_client_id` and `github_app_client_secret` can be obtained from the github application settings whereas jenkins-related fields are known by jenkins administrator.

Once added, users need to paste this application as is in their `addons` folder of Odoo.

For installing this application in Odoo, users have to enable developer mode with assets and then install this application from the store by searching it.

Users must have the pages in their app as mentioned in the python files for this module to work.
