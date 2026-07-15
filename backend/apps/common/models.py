from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# we know that in common we make what we are gonna use the common.
# here we have craeted a timestamp abstratct module because we can use it in all other module which require a craete and update date
