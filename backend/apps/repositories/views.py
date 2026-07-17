import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import GitHubAccount
from .models import Repository

# Create your views here.
class RepositorySyncView(APIView):

    def post(self, request):
        github_account = GitHubAccount.objects.first()
        if not github_account:
            return Response(
                {
                    "error": "Github account is not connected"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        response = requests.get(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {github_account.access_token}",
                "Accept": "application/vnd.github+json",
            },
        )
        # with req we sends a header so that we can access that specific user's reps.
        repositories = response.json()
        return Response(repositories)
