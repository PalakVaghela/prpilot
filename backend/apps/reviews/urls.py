from django.urls import path
from .views import PullReqSyncView, AiReviewView

urlpatterns = [
    path("sync/", PullReqSyncView.as_view(), name="pull-req-sync"),
    path("<int:pr_id>/ai-review/", AiReviewView.as_view(), name="ai-review"),
]
