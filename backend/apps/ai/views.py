import requests
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.authentication.models import GitHubAccount
from apps.reviews.models import PullRequest


# Create your views here.
class AIReviewView(APIView):

    def post(self, request, pr_id):
        github_account = GitHubAccount.objects.first()
        if not github_account:
            return Response(
                {
                    "error": "Github account not connected"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            print("11111111111111111")
            pull_request = PullRequest.objects.select_related("repository").get(id=pr_id)
            print("2222222222")
        except PullRequest.DoesNotExist:
            return Response(
                {
                    "error": "Pull Request not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        response = requests.get(
            f"https://api.github.com/repos/{pull_request.repository.full_name}/pulls/{pull_request.number}/files",
            headers={
                "Authorization": f"Bearer {github_account.access_token}",
                "Accept": "application/vnd.github+json",
            },
        )
        if response.status_code != 200:
            return Response(
                {
                    "error": "Failed to fetch the PR fiels",
                    "github_resopnse": response.json()
                },
                status=response.status_code
            )
        files = response.json()
        code_diff = ""
        for file in files:
            code_diff += f"""
            File: {file['filename']}

            Status: {file['status']}

            Patch:
            {file.get('patch', 'No patch available')}

            {'=' * 80}
            """
        return Response(
            {
                "status_code": response.status_code,
                "diff": code_diff,
            }
        )
