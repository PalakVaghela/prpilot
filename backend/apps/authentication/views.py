import os
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from rest_framework.views import APIView


class GitHubLoginView(APIView):
    def get(self, request):
        params = {
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
            "scope": "repo read:user user:email",
        }

        github_url = (
            "https://github.com/login/oauth/authorize?"
            + urlencode(params)
        )

        return HttpResponseRedirect(github_url)
