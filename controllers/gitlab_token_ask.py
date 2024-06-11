# This script renders a page for getting GitLab personal access token and GitLab repository URL

import os
from odoo import http
import requests

class url_detect(http.Controller):
    @http.route('/gitlab-token-ask', auth='public', website=True)
    def render_github_repo_page(self, **post):
        return http.request.render('cloud_v_app.gitlab_token_ask')
