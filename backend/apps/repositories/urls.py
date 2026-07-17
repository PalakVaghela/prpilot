from django.urls import path
from .views import RepositorySyncView

urlpatterns = [
    path(
        "sync/", RepositorySyncView.as_view(), name="repository-sync",
    )
]
