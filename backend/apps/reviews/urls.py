from django.urls import path
from .views import PullReqSyncView, AiReviewView, PullRequestListView

urlpatterns = [
    path("sync/", PullReqSyncView.as_view(), name="pull-req-sync"),
    path("<int:pr_id>/ai-review/", AiReviewView.as_view(), name="ai-review"),
    path("repository/<int:repository_id>/", PullRequestListView.as_view() ,name="pull-request-list"),
]
