import requests

from apps.authentication.models import GitHubAccount


def get_pr_files(pull_request):
    github_account = GitHubAccount.objects.first()
    if not github_account:
        raise Exception("Github account is not connected")
    response = requests.get(
        f"https://api.github.com/repos/"
        f"{pull_request.repository.full_name}/pulls/"
        f"{pull_request.number}/files",
        headers={
            "Authorization": f"Bearer {github_account.access_token}",
            "Accept": "application/vnd.github+json",
        }
    )
    response.raise_for_status()
    return response.json()
