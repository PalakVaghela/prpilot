from django.urls import path
from .views import RepositorySyncView
from .views import RepositoryListView


urlpatterns = [
    path(
        "sync/", RepositorySyncView.as_view(), name="repository-sync",
    ),
    path(
        "", RepositoryListView.as_view(),name="repository-list",
    ),
]
