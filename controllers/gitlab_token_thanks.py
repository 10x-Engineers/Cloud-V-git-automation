"""
 * Thank you page after getting gitlab personal access token and gitlab repository url
 * Gets the name of the username given the GitLab Personal access token
 * Runs subprocess as python script for: creating GitLab server, creating credentials, creating a multibranch pipeline, returns the link to it
 * Prints the link to the created multibranch pipeline job on the rendered page
"""
import os
from odoo import http
import requests
import subprocess
import json
import logging
logger = logging.getLogger(__name__)

class save_gitlab_info(http.Controller):
    @http.route('/cloud-v-gitlab-integration', auth='public', website=True, csrf=False)
    def handle_post_request(self, **post):
        logger.info('Starting save_github_repo_url function')

        # Setting present working directory
        working_directory = os.path.dirname(os.path.realpath(__file__))

        # Receiving the github repository URL and token via post request
        gitlab_pat = post.get('gitlab_access_token')
        gitlab_repo_url = post.get('gitlab_repo_url')
        if gitlab_pat!=None and gitlab_repo_url!=None:
            command = ['python3', f"{working_directory}/new_gitlab_multibranch_pipeline.py", gitlab_pat, gitlab_repo_url]
            proc=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            pipeline_link = proc.communicate()
            proc.wait()
            return http.request.render('cloud_v_app.gitlab_integration_thanks',
                {
                    'completed_process': pipeline_link[0]
                }
            )

        else:
            access_token="No access token Recieved from GitLab!"
            logger.info("Status Code: ")
            logger.info(response.status_code)
            logger.info("--- Response Content ---")
            logger.info(response.text)
            return http.request.render('cloud_v_app.gitlab_integration_no_token')