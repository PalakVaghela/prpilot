from django.db import models
from apps.repositories.models import Repository

from apps.common.models import TimeStampedModel

# Create your models here.
class PullRequests(TimeStampedModel):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="pull_request")
    github_pr_id = models.BigIntegerField(unique=True)
    number = models.IntegerField()
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=20)
    author = models.CharField(max_length=255)
    base_branch = models.CharField(max_length=255)
    head_branch = models.CharField(max_length=255)
    html_url = models.URLField()

    class Meta:
        db_table = 'pull_requests'

    def __str__(self):
        return f"PR #{self.number}"


class AiReviews(TimeStampedModel):
    pull_request = models.OneToOneField(PullRequests, on_delete=models.CASCADE, related_name="ai_review")
    summary = models.TextField()
    strengths = models.JSONField(default=list)
    issues = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    scores = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default="completed")
    model_name = models.CharField(max_length=100, default="gpt_5.5")

    class Meta:
        db_table = 'ai_reviews'

    def __str__(self):
         return f"Review - PR {self.pull_request.number}"
