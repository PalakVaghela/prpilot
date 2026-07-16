import os
import requests
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

from .models import GitHubAccount

User = get_user_model()


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


class GitHubCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response(
                {"error": "Github did not return any authentication code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={
                "Accept": "application/json",
            },
            data={
                "client_id": os.getenv("GITHUB_CLIENT_ID"),
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return Response(
                {"error": "Github did not return access token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
        github_user = user_response.json()
        user, created = User.objects.update_or_create(
        username=github_user["login"],
        defaults={
            "email": github_user.get("email") or f"{github_user['login']}@github.local",
            "first_name": github_user.get("name") or "",
        },
    )
        # some github user has a secret gmail so we have to use a any other name that's why local one is useed.
        print(created, "creteddddddddddddddddddddddddd")
        GitHubAccount.objects.update_or_create(
        github_id=github_user["id"],
        defaults={
            "user": user,
            "username": github_user["login"],
            "name": github_user.get("name") or "",
            "email": github_user.get("email") or "",
            "avatar_url": github_user.get("avatar_url") or "",
            "profile_url": github_user.get("html_url") or "",
            "access_token": access_token,
            "is_active": True,
        },
    )
        return Response(
            {
                "message": "GitHub account connected successfully!",
                "new_user": created,
                "username": user.username,
            }
        )

# we send req to github, insted of giving access token that may be stolen if it send, so that it sends a token, which is code here like code=abc123.
# it will retun this code then we will req. github that this is user's client id and this is secreat key and this is code can you share me accesstoke, 
# github check that yess this use comes from real auth flow and give the accesstoken.
