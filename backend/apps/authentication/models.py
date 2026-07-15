from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel

# Create your models here.
class GitHubAccount(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="github_account",
    )
    github_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    profile_url = models.URLField()
    access_token = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'github_accounts'

    def __str__(self):
        return self.username

# we use __str_ because without str it will return a objacts like object(1), obj(2) like that so we cannot identify each.
# so that this will print a string of username so we can read it.
# __str__() is just "How should this object look when printed?"

# without meta it will create a table name like = app_name + model_name, so using meta we can rename the table. meta is like settings of the models.
# Meta describes how Django should treat the model. so it don;t have juts db_name but have many more.
# if there is one2one relationship then we use a o2o fileds if there is one to many or relationship then we use a foregin key. and for many to many relationship we use m2m field.

