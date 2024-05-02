import os
from odoo import http
import requests
import subprocess
import json
import logging
logger = logging.getLogger(__name__)

class save_github_repo_url(http.Controller):
    @http.route('/cloud-v-github-integration', auth='public', website=True, csrf=False)
    def handle_post_request(self, **post):
        logger.info('Starting save_github_repo_url function')
        # Setting present working directory
        working_directory = os.path.dirname(os.path.realpath(__file__))

        # Receiving the github repository URL and token via pull request
        github_repo_url = post.get('github_url')
        code = post.get('github_code')

        token_url = "https://github.com/login/oauth/access_token"
        
        # Opening JSON file including client secret and client id
        payload_file = open(f"{working_directory}/userinfo.json")
        payload_data = json.load(payload_file)

        payload = {
                    "client_id": payload_data["github_app_client_id"],
                    "client_secret": payload_data["github_app_client_secret"],
                    "code": code
        }
        headers = {"Accept": "application/json"}
        response = requests.post(token_url, data=payload, headers=headers)
        response_json = response.json()

        access_token = None
        validity_duration = None
        access_token =  response_json.get("access_token")
        validity_duration = response_json.get("expires_in")
        
        # Check if the response was successful (status code 200)
        if response.status_code == 200:
            if access_token!=None:
                command = ['python3', f"{working_directory}/new_job.py", access_token, github_repo_url]
                completed_process = subprocess.run(command, capture_output=True, text=True, check=True)
                pipeline_link = completed_process.stdout
                return http.request.render('cloud_v_app.cloud_v_app_template',
                    {
                        'access_token':access_token, 
                        'validity_duration':validity_duration, 
                        'github_repo_url':github_repo_url, 
                        'completed_process': pipeline_link
                    }
                )
            else:
                access_token="No access token Recieved from GitHub!"
                return http.request.render('cloud_v_app.cloud_v_app_template_no_token',{'access_token':access_token})
