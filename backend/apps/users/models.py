from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    github_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    github_username = models.CharField(max_length=250, unique=True, null=True, blank=True)
    avatar_url = models.URLField(blank=True)
    profile_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
