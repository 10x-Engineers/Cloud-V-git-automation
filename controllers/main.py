import os
from odoo import http
import requests

class url_detect(http.Controller):
    @http.route('/github-app-repo', auth='public', website=True)
    def render_github_repo_page(self, **post):
        working_directory = os.path.dirname(os.path.realpath(__file__))

        code = http.request.params.get('code') # Getting the code from the github URL
        
        return http.request.render('cloud_v_app.github_repo_ask',
                    {
                        'github_code':code
                    }
        )
