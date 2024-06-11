# -*- coding: utf-8 -*-
{
    'name': "Cloud-V GitHub App Integration",
    'summary': "This module is used to generate token for Cloud-V GitHub app",
    'description': "This module is built for Github app authentication so that we may know that we were redirected from github and not from any other site",
    'author': "Cloud-V",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'views/cloud_v_app_template.xml',
        'views/cloud_v_app_template_no_token.xml',
        'views/github_repo_ask.xml',
        'views/gitlab_integration_thanks.xml',
        'views/gitlab_token_ask.xml',
        'views/gitlab_integration_no_token.xml'
        ],
    'demo': [],
    'installable': True,
}
