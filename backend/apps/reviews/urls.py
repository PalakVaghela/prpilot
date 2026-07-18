from django.urls import path
from .views import PullReqSyncView

urlpatterns = [
    path(
        "sync/", PullReqSyncView.as_view(), name="pull-req-sync",
    )
]
