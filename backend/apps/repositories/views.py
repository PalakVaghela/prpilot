import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import GitHubAccount
from .models import Repository

# Create your views here.
class RepositorySyncView(APIView):

    def get(self, request):
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
        saved_count = 0
        for repo in repositories:
            Repository.objects.update_or_create(
                github_id=repo["id"],
                defaults= {
                    "github_account":github_account,
                    "name":repo["name"],
                    "full_name":repo["full_name"],
                    "description":repo["description"] or "",
                    "language":repo["language"] or "",
                    "default_branch":repo["default_branch"],
                    "private":repo["private"],
                    "stars":repo["stargazers_count"],
                    "forks":repo["forks"],
                    "open_issues":repo["open_issues"],
                    "html_url":repo["html_url"]
                }
            )
            saved_count+=1

        return Response(
            {
                "message": "Repos synced successful",
                "repositories": saved_count
            }
            # here repositories is just key name and not field or anything
        )
