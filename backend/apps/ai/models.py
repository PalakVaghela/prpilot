from django.db import models

from apps.common.models import TimeStampedModel
from apps.reviews.models import PullRequest

class AIReview(TimeStampedModel):
    pull_request = models.OneToOneField(PullRequest, on_delete=models.CASCADE, related_name="ai_review")
    summary = models.TextField()
    strengths = models.JSONField(default=list)
    issues = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default="completed")
    model_name = models.CharField(max_length=100, default="gpt_5.5")

    class Meta:
        db_table = 'ai_reviews'

    def __str__(self):
         return f"Review - PR {self.pull_request.number}"



class AIFileReview(TimeStampedModel):
    ai_review = models.ForeignKey(
        AIReview,
        on_delete=models.CASCADE,
        related_name="file_reviews"
    )
    file_path = models.CharField(max_length=500)
    file_status = models.CharField(
        max_length=20,
        choices=[
            ("added", "Added"),
            ("modified", "Modified"),
            ("deleted", "Deleted"),
        ]
    )
    summary = models.TextField(blank=True)
    strengths = models.JSONField(default=list)
    issues = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
