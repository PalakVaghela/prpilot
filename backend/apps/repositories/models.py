from django.db import models
from apps.authentication.models import GitHubAccount
from apps.common.models import TimeStampedModel

# Create your models here.
class Repository(TimeStampedModel):
    github_account = models.ForeignKey(GitHubAccount, on_delete=models.CASCADE, related_name="repositories")
    github_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=100, blank=True)
    default_branch = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    html_url = models.URLField()

    class Meta:
        db_table = 'repositories'

    def __str__(self):
        return self.full_name
