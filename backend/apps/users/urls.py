from django.urls import path
from .views import UserMeView

urlpatterns = [
    path("me/", UserMeView.as_view(), name="user-me")
]

# we use as_view() with UserMeView, because UserMeView is a class