import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PullRequest
from apps.authentication.models import GitHubAccount
from apps.repositories.models import Repository
from apps.ai.services.ai_review import review_pull_request


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


class AiReviewView(APIView):

    def post(self, req, pr_id):
        print("PR ID:", pr_id)
        try:
            pull_request = PullRequest.objects.get(id=pr_id)
            print("Django ID:", pull_request.id)
            print("GitHub PR number:", pull_request.number)
            print("Title:", pull_request.title)
            review = review_pull_request(pull_request)
            return Response({
                "message": "AI review completed",
                "review": {
                    "id": review.id,
                    "summary": review.summary,
                    "strengths": review.strengths,
                    "issues": review.issues,
                    "suggestions": review.suggestions,
                    "score": float(review.score),
                    "status": review.status,
                    "model_name": review.model_name,
                }
            })
        except PullRequest.DoesNotExist:
            return Response(
                {"error": "Pull request not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class PullRequestListView(APIView):

    def get(self, request, repository_id):
        github_account = GitHubAccount.objects.first()
        if not github_account:
            return Response(
                {"error": "Github account is not connected"},
                status=status.HTTP_404_NOT_FOUND
            )
        repository = Repository.objects.get(id=repository_id)
        response = requests.get(
            f"https://api.github.com/repos/{repository.full_name}/pulls",
            headers={
                "Authorization": f"Bearer {github_account.access_token}",
                "Accept": "application/vnd.github+json",
            },
            params={
                "state": "open",
            },
        )
        response.raise_for_status()
        pull_requests = response.json()
        for req in pull_requests:
            PullRequest.objects.update_or_create(
                github_pr_id=req["id"],
                defaults={
                    "repository": repository,
                    "title": req["title"],
                    "description": req["body"] or "",
                    "state": req["state"],
                    "author": req["user"]["login"],
                    "base_branch": req["base"]["ref"],
                    "head_branch": req["head"]["ref"],
                    "html_url": req["html_url"],
                    "number": req["number"],
                }
            )
        saved_pull_requests = PullRequest.objects.filter(
            repository=repository
        ).order_by("-number")
        data = []
        for pr in saved_pull_requests:
            data.append({
                "id": pr.id,
                "number": pr.number,
                "title": pr.title,
                "description": pr.description,
                "state": pr.state,
                "author": pr.author,
                "base_branch": pr.base_branch,
                "head_branch": pr.head_branch,
                "html_url": pr.html_url,
            })
        return Response(data)
