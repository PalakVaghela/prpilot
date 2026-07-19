from django.db import models
from apps.repositories.models import Repository

from apps.common.models import TimeStampedModel

# Create your models here.
class PullRequest(TimeStampedModel):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="pull_requests")
    github_pr_id = models.BigIntegerField(unique=True)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=20)
    author = models.CharField(max_length=255)
    base_branch = models.CharField(max_length=255)
    head_branch = models.CharField(max_length=255)
    html_url = models.URLField()

    class Meta:
        db_table = 'pull_requests'
        ordering = ["-number"]

    def __str__(self):
        return f"PR #{self.number} - {self.title}"
