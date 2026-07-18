import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PullRequest
from apps.authentication.models import GitHubAccount
from apps.repositories.models import Repository


# Create your views here.
class PullReqSyncView(APIView):

    def get(self, request):
        print("111111111111111111111")
        github_account = GitHubAccount.objects.first()
        print(github_account, "account")
        if not github_account:
            return Response(
                {
                    "error": "Github accout is not connected"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        repositories = Repository.objects.filter(github_account=github_account)
        print(repositories, "repoooooooooooooooooooooo")

        saved_count = 0
        for repo in repositories:
            print("=" * 50)
            print(f"Repository: {repo.full_name}")

            print(repo.full_name, "Name of reos")
            response = requests.get(
                f"https://api.github.com/repos/{repo.full_name}/pulls",
                headers={
                    "Authorization": f"Bearer {github_account.access_token}",
                    "Accept": "application/vnd.github+json",
                },
                params={
                    "state": "open",
                },
            )
            pull_req = response.json()
            for req in pull_req:
                PullRequest.objects.update_or_create(
                    github_pr_id=req["id"],
                    defaults={
                        "repository": repo,
                        "title":req["title"],
                        "description":req["body"] or "",
                        "state":req["state"],
                        "author":req["user"]["login"],
                        "base_branch":req["base"]["ref"],
                        "head_branch":req["head"]["ref"],
                        "html_url":req["html_url"],
                        "number": req["number"],
                    }
                )
                saved_count+=1

        return Response(
            {
                "messaage": "gocha pulls",
                "saved": saved_count
            }
        )
