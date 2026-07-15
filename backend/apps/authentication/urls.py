from django.urls import path

from .views import GitHubLoginView

urlpatterns = [
    path("github/login/", GitHubLoginView.as_view(), name="github-login"),
]
