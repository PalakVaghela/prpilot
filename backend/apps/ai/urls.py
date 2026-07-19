from django.urls import path

from .views import AIReviewView

urlpatterns = [
    path("review/<int:pr_id>/", AIReviewView.as_view(), name="ai-review")
]
